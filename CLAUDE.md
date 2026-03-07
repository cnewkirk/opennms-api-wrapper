# CLAUDE.md — opennms-api-wrapper

This file gives Claude Code the context needed to work on this project
without prior conversation history.

## Project purpose

A thin, synchronous Python 3 wrapper for the OpenNMS REST API (Horizon 35).
Users `import opennms_api_wrapper as opennms` and get a single `OpenNMS`
client class with one method per API endpoint.

## Repository layout

```
opennms_api_wrapper/    # installable package
    __init__.py         # exports OpenNMS, __version__
    client.py           # OpenNMS class (combines all mixins)
    _base.py            # _OpenNMSBase: HTTP helpers (_get/_post/_put/_delete/_parse)
    _alarms.py          # AlarmsMixin
    _alarm_stats.py     # AlarmStatsMixin
    _alarm_history.py   # AlarmHistoryMixin
    _events.py          # EventsMixin
    _nodes.py           # NodesMixin  (largest: nodes + sub-resources)
    _outages.py         # OutagesMixin
    _notifications.py   # NotificationsMixin
    _acks.py            # AcksMixin
    _requisitions.py    # RequisitionsMixin
    _foreign_sources.py # ForeignSourcesMixin
    _snmp_config.py     # SnmpConfigMixin
    _groups.py          # GroupsMixin
    _users.py           # UsersMixin
    _categories.py      # CategoriesMixin
    _sched_outages.py   # SchedOutagesMixin
    _ksc_reports.py     # KscReportsMixin
    _resources.py       # ResourcesMixin
    _measurements.py    # MeasurementsMixin
    _heatmap.py         # HeatmapMixin
    _maps.py            # MapsMixin
    _graphs.py          # GraphsMixin
    _flows.py           # FlowsMixin
    _device_config.py   # DeviceConfigMixin
    _situations.py      # SituationsMixin  (v2)
    _business_services.py  # BusinessServicesMixin  (v2)
    _metadata.py        # MetadataMixin  (v2, largest: node/iface/service metadata)
    _info.py            # InfoMixin
    _discovery.py       # DiscoveryMixin  (v2)
    _ipinterfaces_v2.py    # IpInterfacesV2Mixin
    _snmpinterfaces_v2.py  # SnmpInterfacesV2Mixin

tests/
    conftest.py         # client fixture, V1/V2 URL constants, qs() helper
    fixtures.py         # all accurate OpenNMS Horizon 35 response shapes
    test_*.py           # one file per mixin (30 files, 290 tests total)

dist/                   # built artifacts (gitignored)
pyproject.toml          # build config + project metadata
smoke_test.py           # live-server smoke test (read-only + --write mode)
ARCHITECTURE.md         # architecture decision records (ADRs)
MERMAID.md              # Mermaid architecture diagrams
CHANGELOG.md
README.md
CONTRIBUTING.md
```

## Architecture decisions (do not change without good reason)

- **Mixin pattern**: each resource group lives in its own `_<name>.py` mixin.
  `client.py` combines them all via multiple inheritance into `OpenNMS`.
- **JSON only**: all request bodies are JSON. No XML anywhere.
  The one exception: `POST /rest/acks` uses `application/x-www-form-urlencoded`
  because the OpenNMS API requires it — handled via `form_data=` in `_post`.
- **Synchronous only**: no async. `requests.Session` is used throughout.
  One runtime dependency: `requests>=2.28`.
- **v1 vs v2**: v1 endpoints live at `/opennms/rest/`, v2 at
  `/opennms/api/v2/`. Every `_get/_post/_put/_delete` accepts `v2=True`.
- **`_parse()`** handles three response types:
  - `application/json` → `resp.json()`
  - `text/plain` → `int(text)` if possible, else `str`
  - empty body (204 No Content) → `None`
- **Timeout**: `_OpenNMSBase.__init__` accepts `timeout=30` (seconds). Passed
  to every `_session.get/post/put/delete` call. `OpenNMS.__init__` exposes it
  as a public parameter.

## Development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"   # installs requests + pytest + responses
pytest tests/ -v          # run full suite (290 tests, ~0.2 s)
```

Always activate the `.venv` before running any commands — never rely on the
system Python or system pip.

## Test conventions

- HTTP mocking: `responses` library with `@responses.activate` decorator.
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

```bash
pip install build
python -m build          # produces dist/*.tar.gz and dist/*.whl
pip install twine
twine upload dist/*      # publish to PyPI
```

The build backend is `setuptools.build_meta` (in `pyproject.toml`).
The older path `setuptools.backends.legacy:build` does not work — do not use it.

## Style

- PEP 8 throughout: 79-character line limit, 4-space indentation.
- Every public method has a Google-style docstring with `Args:` and `Returns:`
  sections where non-trivial — required for autodoc compatibility (Sphinx,
  pdoc, mkdocstrings). Private helpers have at minimum a one-line docstring.
- No inline comments on code that is self-evident.
- No error handling for scenarios that cannot happen.
- No abstractions introduced for one-off operations.
