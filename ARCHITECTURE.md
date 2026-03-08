# Architecture Decision Record — opennms-api-wrapper

This document captures the significant design decisions made in building
`opennms-api-wrapper`, the rationale behind each, and their tradeoffs.  It
is intended to serve both as institutional memory and as a guide for
contributors evaluating future changes.

Format loosely follows [Nygard ADRs](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):
**Context → Decision → Consequences**.

---

## ADR-001 · Mixin-per-resource architecture

### Status
Accepted

### Context
The OpenNMS REST API covers 35+ resource groups (alarms, nodes, flows,
metadata, …) yielding several hundred public methods.  Placing all methods in one
class produces a 5 000-line file that is hard to navigate, hard to test in
isolation, and impossible to maintain incrementally.  The alternatives were:

| Option | Description |
|---|---|
| **Flat module functions** | `opennms.get_alarms(client, ...)` — functional style, no class |
| **One class, one file** | `OpenNMS` with all 250 methods in a single source file |
| **Resource sub-clients** | `client.alarms.get(...)`, `client.nodes.get(...)` |
| **Mixin-per-resource** | One mixin class per resource group, assembled via multiple inheritance into one `OpenNMS` class |

### Decision
Mixin-per-resource.  Each API resource group lives in its own file
(`_alarms.py`, `_nodes.py`, …).  `client.py` assembles them with multiple
inheritance, exposing a single flat namespace to callers.

### Consequences

**Pros**
- Each mixin is 50–230 lines and covers exactly one coherent concern.
- Adding a new resource group is additive: new file, new mixin, one line in
  `client.py`.  No existing code changes.
- Tests map 1-to-1: `test_alarms.py` tests only `AlarmsMixin`.
- The public API is a flat, discoverable namespace: `client.get_alarms()`,
  `client.get_nodes()` — no sub-object navigation required.

**Cons**
- Python's MRO is non-obvious to contributors unfamiliar with multiple
  inheritance.  A name collision between two mixins silently shadows one
  method; there is no compile-time detection.
- The large inheritance chain can confuse IDE introspection and some
  documentation generators (though mkdocstrings handles it correctly via
  `inherited_members: true`).
- Discipline on method naming (`get_alarm_*`, `get_node_*`) is enforced only
  by convention, not the language.

**Mitigations in place**
- Method names are prefixed by resource group, making accidental collision
  very unlikely.
- `CLAUDE.md` documents the convention explicitly for future contributors.

---

## ADR-002 · JSON-only I/O; no XML support

### Status
Accepted

### Context
The OpenNMS v1 REST API historically required XML for many write operations
(create node, create foreign source, create user, …) and returned XML by
default.  The v2 API is JSON-first.  Modern Horizon releases (30+) accept
JSON on all endpoints via `Accept: application/json` /
`Content-Type: application/json`.

### Decision
Set `Accept: application/json` and `Content-Type: application/json` as
session-level defaults.  Emit and parse JSON exclusively.  No XML handling
code anywhere in the library.

### Consequences

**Pros**
- Eliminates an entire class of code (`xml.etree`, `lxml`, schema validation,
  namespace handling).
- Callers work with plain Python dicts and lists — no DOM traversal.
- Tests are straightforward: mock responses return Python dicts; assertions
  compare plain values.
- Keeps the library at one runtime dependency (`requests`).

**Cons**
- Callers on Horizon < 30 may receive HTTP 415 (Unsupported Media Type) on
  certain write endpoints.  This is documented in the affected method
  docstrings with a suggested workaround.
- No fallback path: there is no way to opt into XML without forking the
  library.

**Risk level**
Low.  All Horizon 30+ instances (released 2022) support JSON fully.
Horizon < 30 is end-of-life.

---

## ADR-003 · Single runtime dependency (requests)

### Status
Accepted

### Context
The library needs to make authenticated HTTP calls, parse responses, and
handle redirects and SSL.  Options included:

| Option | Notes |
|---|---|
| `urllib3` / `http.client` | Stdlib-adjacent; verbose; no session/auth helpers |
| `requests` | Mature, ubiquitous, synchronous |
| `httpx` | Modern, supports both sync and async |
| `aiohttp` | Async-only |

### Decision
`requests` only, pinned to `>= 2.28` (2022).

### Consequences

**Pros**
- `requests` is already present in virtually every Python environment.
- No dependency conflicts for callers who also use `requests`.
- Well-understood by contributors; extensive documentation and Stack Overflow
  coverage.
- `requests.Session` provides connection pooling, auth, and default headers
  for free.

**Cons**
- Synchronous only: callers who need concurrency must use
  `ThreadPoolExecutor` or run multiple client instances.
- `httpx` would have enabled async support with minimal additional complexity;
  that door is now harder to open without a breaking API change.
- If the ecosystem migrates to `httpx`-based tooling, this becomes a soft
  incompatibility (two HTTP stacks in one environment).

---

## ADR-004 · Synchronous-only client

### Status
Accepted

### Context
REST API wrappers are commonly available in both sync and async variants.
Async variants add implementation complexity (two code paths or a sync-to-
async bridge like `anyio`) and require callers to run an event loop.

### Decision
Synchronous only.  No `async def`, no `asyncio`, no `anyio`.

### Consequences

**Pros**
- Zero async complexity in the implementation.
- Works in any context: scripts, Django views, Flask routes, Jupyter notebooks,
  CLI tools — without an event loop.
- Easier to test: no `pytest-asyncio`, no `asyncio.run()` boilerplate.

**Cons**
- A caller issuing 50 API calls sequentially pays 50× the round-trip latency.
  The workaround (`ThreadPoolExecutor`) is effective but requires caller
  knowledge.
- Libraries built on `asyncio` (FastAPI background tasks, etc.) cannot
  `await` these calls naturally.

**Intended use case**
Ops scripts, monitoring integrations, and data pipelines — workloads where
sequential simplicity outweighs async throughput.

---

## ADR-005 · Unified response parser (`_parse`)

### Status
Accepted

### Context
OpenNMS endpoints return three distinct response shapes:

1. `application/json` — a dict or list
2. `text/plain` — a plain integer (count endpoints like `/rest/alarms/count`)
3. Empty body with HTTP 204 — write operations that return no content

Without a central handler, each method would need to inspect `Content-Type`
and handle error status codes individually.

### Decision
All HTTP verbs route through a single `_parse(resp)` method on the base
class.  It calls `raise_for_status()`, then branches on `Content-Type` and
body presence.  Callers receive a Python object or `None`; they never see a
`Response` object.

### Consequences

**Pros**
- Error handling (`raise_for_status`) is guaranteed for every call — callers
  cannot accidentally ignore HTTP error status codes.
- Integer parsing (count endpoints) is handled transparently.
- 204 responses return `None` rather than raising or returning an empty
  string; callers can test `if result is not None`.
- The entire parsing contract is tested in one place.

**Cons**
- Callers cannot access response headers, status codes, or raw bytes.  If an
  endpoint needs header inspection (e.g. `Location` on a 201 Created), the
  library cannot surface it without adding a new return path.
- The fallback (`try: resp.json()`) masks cases where a server returns
  unexpected `text/html` error pages with a 200 status; the dict will be
  returned but will look wrong to the caller.

---

## ADR-006 · `**filters` passthrough for Hibernate query parameters

### Status
Accepted

### Context
OpenNMS v1 list endpoints accept an open-ended set of Hibernate property
filters (`severity`, `alarm.uei`, `node.label`, `ipInterface.ipAddress`, …)
plus a `comparator` modifier.  The full set of valid keys is not enumerated
in the API documentation and varies by resource.

### Decision
List methods accept `**filters` and merge them directly into the query
parameter dict without validation.

```python
client.get_alarms(severity="MAJOR", node.label="router01")
```

### Consequences

**Pros**
- No maintenance burden of enumerating and validating filter keys per
  resource — a list that would grow stale with each OpenNMS release.
- Any filter key OpenNMS accepts works immediately without a library update.
- Callers with deep OpenNMS knowledge can use advanced filters
  (`comparator=ilike`) that the library author may not have anticipated.

**Cons**
- Typos are silently swallowed.  `get_alarms(severiy="MAJOR")` returns all
  alarms with no error.
- IDE auto-complete cannot suggest valid filter keys.
- The `**filters` signature communicates *nothing* about what filters exist;
  callers must consult OpenNMS documentation.

**Mitigations in place**
- Docstrings list the most common filter keys for each resource group.
- The smoke test exercises real servers and will surface bad filters
  implicitly (wrong result counts).

---

## ADR-007 · v1/v2 API routing via `v2=True` flag

### Status
Accepted

### Context
OpenNMS exposes two API generations at different base paths:
- v1: `/opennms/rest/`
- v2: `/opennms/api/v2/`

Several resources appear in both (alarms, IP interfaces, SNMP interfaces);
a few are v2-only (situations, business services, discovery, metadata).

### Decision
A single `_OpenNMSBase` instance holds both base URLs.  All private HTTP
helpers (`_get`, `_post`, …) accept an optional `v2: bool = False` parameter
that selects the base URL.  v2-specific methods call their helper with
`v2=True`; the caller never sees the URL.

### Consequences

**Pros**
- One client object serves the entire API surface; callers do not need to
  instantiate two clients.
- URL construction is centralised in `_url()`; changing the path structure
  requires editing one method.
- v2 methods are clearly identified in the source by their `v2=True` call
  and by the `_v2` suffix in their names (`get_alarms_v2`,
  `get_alarm_v2`).

**Cons**
- The `v2` flag leaks an implementation detail into every private method
  signature.
- If a future v3 API emerges, this pattern extends awkwardly (a `v3=True`
  flag alongside `v2=True`).

**Alternative not taken**
Separate `_v1_get` / `_v2_get` helpers were rejected as more verbose with no
meaningful benefit at the current API scale.

---

## ADR-008 · Mocked HTTP unit tests (no live server required)

### Status
Accepted

### Context
Testing an HTTP wrapper requires either a live server, a local stub server
(e.g. WireMock), or an HTTP mocking library.  Each approach has different
tradeoffs for speed, reliability, and setup overhead.

### Decision
Use the `responses` library to intercept `requests` calls at the adapter
level.  Every test registers expected URLs and response bodies; no network
traffic occurs.  Fixture shapes in `tests/fixtures.py` are derived from the
actual OpenNMS Horizon 35 JavaDoc field names.

### Consequences

**Pros**
- Tests run in ~0.2 s with no external dependencies.
- Tests are fully deterministic; they cannot fail due to server state.
- CI requires no OpenNMS instance; any Python environment can run the suite.
- Fixture shapes document the real API response contracts.

**Cons**
- Fixtures can drift from the live API as OpenNMS evolves; the test suite
  will still pass even if a field is renamed upstream.
- Tests verify the library's *request construction* and *response parsing*
  but not whether the server actually accepts those requests.
- There is no contract test: if OpenNMS changes a response shape in a minor
  release, the library breaks silently until a human notices.

**Mitigation**
`smoke_test.py` runs all getters against a real server.  It is intended to
be run against a dev or staging instance before each release.

---

## ADR-009 · HTTP timeout

### Status
Accepted / Implemented in v0.1.0

### Context
`requests` does not set a default socket timeout.  A call to a slow or
unresponsive server will block the calling thread indefinitely.

### Decision
Added a `timeout` parameter to `_OpenNMSBase.__init__` and `OpenNMS.__init__`
defaulting to 30 seconds.  Every `_session.get/post/put/delete` call passes
`timeout=self._timeout`.

```python
def __init__(self, url, username, password, verify_ssl=True, timeout=30):
    ...
    self._timeout = timeout

def _get(self, path, params=None, v2=False):
    resp = self._session.get(self._url(path, v2),
                             params=params, timeout=self._timeout)
    return self._parse(resp)
```

### Consequences

**Pros**
- Threads cannot hang indefinitely on a slow or unresponsive server.
- Callers who need a longer timeout can pass `timeout=N`; `timeout=None`
  restores unbounded behaviour.

**Cons**
- Long-running bulk operations or slow servers may now surface
  `requests.exceptions.Timeout`; callers must set a higher `timeout` if
  needed.

---

## ADR-010 · Retry with exponential backoff

### Status
Accepted — supersedes earlier "No retry" decision

### Context
HTTP clients in production environments commonly need to retry on transient
errors (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable,
504 Gateway Timeout, connection resets).  The OpenNMS REST API occasionally
returns transient 500s under load.  `requests` uses `urllib3` under the hood,
which provides a built-in `Retry` class with exponential backoff — no new
dependencies required.

### Decision
`_OpenNMSBase.__init__` accepts a `retries` parameter (default 3).  When
`retries > 0`, a `urllib3.util.retry.Retry` adapter is mounted on the session
for both `http://` and `https://`.

```python
if retries > 0:
    retry = Retry(
        total=retries,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=None,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    self._session.mount("https://", adapter)
    self._session.mount("http://", adapter)
```

Key parameters:
- `backoff_factor=0.5` → delays of 0.5 s, 1 s, 2 s (3.5 s total max wait).
- `status_forcelist=(500, 502, 503, 504)` → retry on transient server errors.
- `allowed_methods=None` → retry all HTTP methods (OpenNMS REST operations
  are functionally idempotent).
- `raise_on_status=False` → after retries are exhausted, the last response
  is returned so `_parse()` → `raise_for_status()` raises `HTTPError` as
  before (backwards-compatible error behaviour).
- Pass `retries=0` to disable and get the old one-request-per-call behaviour.

### Consequences

**Pros**
- Transient 500s and connection resets are handled transparently — all
  consumers (including the smoke test) benefit automatically.
- No new runtime dependency; `urllib3` ships with `requests`.
- Opt-out is trivial: `retries=0`.

**Cons**
- Non-idempotent side effects (e.g. creating a resource) could in theory
  execute twice if the server processes the request but the response is lost.
  In practice, OpenNMS REST endpoints either return the same result or reject
  duplicates (requisition nodes keyed by foreign-id, acks keyed by alarm-id).
- Adds up to 3.5 s of hidden latency on a truly broken endpoint before the
  caller sees the error.

---

## ADR-011 · `__version__` single-source ownership

### Status
Accepted / Implemented in v0.1.0

### Decision
Removed the hardcoded `__version__` string from `__init__.py`.  Version is
now derived at runtime from installed package metadata:

```python
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("opennms-api-wrapper")
except PackageNotFoundError:
    __version__ = "unknown"   # running directly from source, not installed
```

`pyproject.toml` is the single source of truth.

### Consequences
- One fewer manual step on each release — only `pyproject.toml` needs
  updating.
- `__version__` is always accurate when the package is installed; returns
  `"unknown"` only when running directly from an uninstalled source tree.

---

## Summary matrix

| ADR | Decision | Primary benefit | Primary cost |
|---|---|---|---|
| 001 | Mixin per resource | Incremental, isolated | MRO non-obvious |
| 002 | JSON-only | Eliminates XML complexity | HTTP 415 on old servers |
| 003 | `requests` only | Ubiquitous, zero conflict | No native async |
| 004 | Sync only | Simple, works everywhere | Latency under concurrency |
| 005 | Unified `_parse()` | Consistent error handling | No header/status access |
| 006 | `**filters` passthrough | Future-proof, zero maintenance | Typos are silent |
| 007 | `v2=True` flag | One client, full surface | Flag leaks into every helper |
| 008 | Mocked HTTP tests | Fast, deterministic, portable | Fixtures can drift |
| 009 | `timeout=30` default | Threads cannot hang indefinitely | Long ops may need higher timeout |
| 010 | Retry w/ backoff (default 3) | Transient 500s handled transparently | Up to 3.5 s hidden latency |
| 011 | `importlib.metadata` version | Single source of truth | Returns `unknown` from uninstalled source |
