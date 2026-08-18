# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

A thin, synchronous Python 3 wrapper for the OpenNMS REST API (Horizon 35).
Users `import opennms_api_wrapper as opennms` and get a single `OpenNMS`
client class with one method per API endpoint.

## Development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"        # installs requests + pytest + responses + ruff + mypy
pytest tests/ -v               # run full suite (~0.4 s)
pytest tests/test_alarms.py -v # run a single test file
ruff check .                   # lint
mypy opennms_api_wrapper/      # type-check
mkdocs serve                   # preview docs at http://127.0.0.1:8000
```

Always activate the `.venv` before running any commands — never rely on the
system Python or system pip.

## Repository layout

```
opennms_api_wrapper/    # installable package
    __init__.py         # exports OpenNMS, __version__
    client.py           # OpenNMS class (combines all mixins via multiple inheritance)
    _base.py            # _OpenNMSBase: HTTP helpers (_get/_post/_put/_delete/_patch/_parse)
    _exceptions.py      # Exception hierarchy (see below)
    _pagination.py      # PaginationMixin (client.paginate())
    _<name>.py          # one mixin per resource group (see client.py for the full list)

tests/
    conftest.py         # client fixture, V1/V2 URL constants, qs() helper
    fixtures.py         # accurate OpenNMS Horizon 35 response shapes
    test_*.py           # one file per mixin

docs/                   # MkDocs source (mkdocs-material + mkdocstrings)
pyproject.toml          # build config, project metadata, ruff/mypy/pytest config
smoke_test.py           # live-server smoke test (read-only + --write mode)
ARCHITECTURE.md         # architecture decision records (ADRs)
TODO.md                 # deferred items
```

## Adding a new endpoint group

1. Create `opennms_api_wrapper/_<name>.py` with a `<Name>Mixin` class.
2. Import it in `client.py` and add it to the `OpenNMS` base class list.
3. Add response fixture(s) to `tests/fixtures.py`.
4. Create `tests/test_<name>.py` with `@responses.activate` tests.

## Exception hierarchy

```
OpenNMSError
└── OpenNMSHTTPError          # base for all HTTP errors; has .status_code and .response
    ├── BadRequestError       # 400
    ├── AuthenticationError   # 401
    ├── ForbiddenError        # 403
    ├── NotFoundError         # 404
    ├── ConflictError         # 409
    └── ServerError           # 5xx
```

## Architecture decisions (do not change without good reason)

- **Mixin pattern**: each resource group lives in its own `_<name>.py` mixin.
  `client.py` combines them all via multiple inheritance into `OpenNMS`.
- **JSON first**: request bodies are JSON wherever the server accepts
  it. No XML parsing anywhere. Exceptions the OpenNMS API forces
  (v1 endpoints that reject JSON on every version):
  - `POST /rest/acks` — form-encoded (`form_data=` in `_post`).
  - `POST /rest/groups` and `POST /rest/users` — XML only; the
    mixins build the small XML documents internally, callers still
    pass plain dicts.
  - `PUT /rest/groups/{name}` and `PUT /rest/users/{name}` —
    form-encoded (`form_data=` in `_put`).
  - `/rest/graphml` — GraphML documents pass through as opaque XML
    strings (`_post_text`/`_get_text`).
- **Synchronous only**: no async. `requests.Session` is used throughout.
  One runtime dependency: `requests>=2.28`.
- **v1 vs v2**: v1 endpoints live at `/opennms/rest/`, v2 at
  `/opennms/api/v2/`. Every `_get/_post/_put/_delete` accepts `v2=True`.
- **Accept header**: `application/json, text/plain;q=0.9`. Some OpenNMS
  versions return 406 if the Accept header does not include `text/plain` for
  `/count` endpoints. JSON stays preferred via implicit q=1.0.
- **`_parse()`** handles three response types:
  - `application/json` → `resp.json()`
  - `text/plain` → `int(text)` if possible, else `str`
  - empty body (204 No Content) → `None`
- **Node count via v2**: `get_node_count()` uses `GET /api/v2/nodes?limit=1`
  and extracts `totalCount`. The v1 `/rest/nodes` endpoint does not have a
  `/count` sub-resource — it routes all sub-paths as node criteria.
- **Timeout**: connect timeout is `min(timeout, 10)`, read timeout is the full
  `timeout` value. `OpenNMS.__init__` accepts `timeout=30` (seconds).
- **Retries**: mounts a urllib3 `Retry` adapter when `retries > 0` (default 3).
  Retries on connection errors and HTTP 500/502/503/504 with 0.5s backoff
  factor. Pass `retries=0` to disable.
- **Smoke test warn level**: endpoints that depend on optional plugins or
  heavy server-side queries use `warn()` instead of `run()`. Warnings are
  non-fatal. Only hard `FAIL`s cause a non-zero exit code.
- **Smoke test SSL**: always use `OPENNMS_VERIFY_SSL=true` — the live server
  has a valid certificate. Never disable SSL verification.

## Live validation against a local Horizon container

To test against a real, current OpenNMS instead of mocks, run the
throwaway stack in `tests/live/compose.yaml` **on the local machine**
(never on shared infrastructure):

```bash
colima start --cpu 2 --memory 4     # or any local Docker engine
docker compose -f tests/live/compose.yaml up -d
# ready when this returns 200 (first boot takes a few minutes):
curl -s -o /dev/null -w '%{http_code}' -u admin:admin \
  http://localhost:8980/opennms/rest/info
OPENNMS_URL=http://localhost:8980 OPENNMS_USER=admin \
  OPENNMS_PASSWORD=admin python smoke_test.py
docker compose -f tests/live/compose.yaml down -v   # always tear down
```

The `foundation-2025` image tag tracks the Meridian 2025 foundation
(the docs baseline for `COVERAGE.md`); numbered tags pin Horizon
releases. The throwaway instance uses plain HTTP with admin/admin —
the smoke-test SSL rule above applies to real servers, not this one.

## Test conventions

- HTTP mocking: `responses` library with `@responses.activate` decorator.
- **Request-shape assertions must come from the REST docs or live
  verification, never from the implementation** — a mock that mirrors
  what the wrapper sends proves nothing. For write endpoints whose
  documented Content-Type is not JSON (XML-only creates, form-encoded
  updates), use `add_contract()` from `conftest.py`: it returns 415
  for any other Content-Type, exactly as the server does, so a
  wrapper regression fails mocked tests the same way it fails live.
- Mocked tests verify URL construction, request bodies, and response
  parsing. Server compatibility is only proven by the live smoke test
  against `tests/live/compose.yaml` — run `smoke_test.py` (read) and
  `smoke_test.py --write --yes` (write) there before a release.
- `conftest.py` constants:
  - `V1 = "http://opennms:8980/opennms/rest"`
  - `V2 = "http://opennms:8980/opennms/api/v2"`
  - `qs(url)` parses query params from a URL into a dict of lists.
- Fixture shapes in `tests/fixtures.py` mirror real OpenNMS Horizon 35
  responses (singular resource name as list wrapper key, plus `totalCount`,
  `count`, `offset`).
- **URL encoding gotcha**: `requests` percent-encodes spaces in URL path
  segments as `%20`, not `+`. Mock URLs for paths with spaces must use `%20`
  explicitly, e.g. `Do%20Not%20Persist%20Discovered%20IPs`.
- 204 responses return `None`; plain-text count endpoints return `int`.
- Verify request bodies with `json.loads(responses.calls[0].request.body)`.

## Build / release

PyPI publishing is **automated** via `.github/workflows/publish.yml`. It
triggers on every GitHub release (`on: release: [published]`) and uses OIDC
trusted publishing — no API token or manual `twine upload` needed.

Release checklist:

1. Bump `version` in `pyproject.toml`.
2. Add a changelog entry in `CHANGELOG.md`.
3. Commit, push a branch, open a PR, and merge to `main`.
4. `gh release create vX.Y.Z` — the publish workflow builds and uploads
   to PyPI automatically.

To build locally:

```bash
pip install build
python -m build          # produces dist/*.tar.gz and dist/*.whl
```

The build backend is `setuptools.build_meta`. Do not use
`setuptools.backends.legacy:build`.

## Git workflow

- **Never push directly to `main`.** All changes go through a branch + PR.
- Branch naming: `feature/<topic>`, `fix/<topic>`, `docs/<topic>`, etc.
- Commit on the branch, push, open a PR with `gh pr create`, and merge once
  CI is green.

## Style

- PEP 8 throughout: 79-character line limit, 4-space indentation.
- Every public method has a Google-style docstring with `Args:` and `Returns:`
  sections where non-trivial — required for autodoc compatibility (Sphinx,
  pdoc, mkdocstrings). Private helpers have at minimum a one-line docstring.
- No inline comments on code that is self-evident.
- No error handling for scenarios that cannot happen.
- No abstractions introduced for one-off operations.
