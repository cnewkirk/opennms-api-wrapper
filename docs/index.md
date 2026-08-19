# python-opennms

[![CI](https://github.com/cnewkirk/python-opennms/actions/workflows/ci.yml/badge.svg)](https://github.com/cnewkirk/python-opennms/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/cnewkirk/python-opennms/graph/badge.svg)](https://codecov.io/gh/cnewkirk/python-opennms)
[![PyPI](https://img.shields.io/pypi/v/python-opennms)](https://pypi.org/project/python-opennms/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cnewkirk/python-opennms/blob/main/LICENSE)

An unofficial, dependency-minimal Python 3 client for the [OpenNMS](https://www.opennms.com/) REST API (Horizon 30+ and Meridian).
Covers 100% of the [Meridian 2025 REST API reference](https://docs.opennms.com/meridian/2025/development/rest/rest-api.html) (excluding the three web-UI-internal APIs), smoke-tested read and write against the Meridian 2025 foundation (Horizon 34.0.1). Expected server range: Horizon 30+; eventconf requires Horizon 35+, and the legacy maps API only exists before Horizon 16.

**OpenNMS resources**: [Docs](https://docs.opennms.com/) · [REST API reference](https://docs.opennms.com/horizon/latest/development/rest/rest-api.html) · [Community forum](https://opennms.discourse.group/)

## Installation

```bash
pip install python-opennms
```

**From source** (latest development version):

```bash
git clone https://github.com/cnewkirk/python-opennms.git
cd python-opennms
pip install .
```

## Quick start

```python
import opennms

client = opennms.OpenNMS(
    url="https://opennms.example.com:8443",
    username="admin",
    password="admin",
)

# Server info
info = client.get_info()
print(info["displayVersion"])

# List alarms
alarms = client.get_alarms(limit=25, order_by="lastEventTime", order="desc")
for alarm in alarms["alarm"]:
    print(alarm["id"], alarm["severity"], alarm["nodeLabel"])

# Acknowledge an alarm
client.ack_alarm(alarm_id=42)

# FIQL filter (v2 API)
alarms = client.get_alarms_v2(fiql="severity==MAJOR")
```

## Features

- Covers every v1 (`/opennms/rest/`) and v2 (`/opennms/api/v2/`) endpoint
- JSON everywhere — no XML handling required
- Single runtime dependency: [`requests`](https://docs.python-requests.org/)
- Synchronous and straightforward — no async complexity
- `TypedDict` schemas for all write payloads — field names, types, and docs in your IDE
- Typed exception hierarchy — catch `NotFoundError`, `ForbiddenError`, etc. without importing `requests`
- Pagination helper — `client.paginate()` yields all items from any list endpoint automatically
- Full test suite with mocked HTTP — no live server required

## Authentication

Basic authentication. Pass `verify_ssl=False` for self-signed certs:

```python
client = opennms.OpenNMS(
    url="https://opennms.example.com:8443",
    username="admin",
    password="admin",
    verify_ssl=False,
)
```

## Smoke testing

`smoke_test.py` (included in the source repository) exercises the wrapper
against a real OpenNMS server. Configure it via environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENNMS_URL` | yes | — | Base URL, e.g. `https://opennms.example.com:8443` |
| `OPENNMS_USER` | yes | — | Username (needs at minimum the `rest` role) |
| `OPENNMS_PASSWORD` | yes | — | Password |
| `OPENNMS_VERIFY_SSL` | no | `true` | Set to `false` to skip SSL certificate verification |
| `OPENNMS_TIMEOUT` | no | `60` | Per-request timeout in seconds |

**Read-only mode** (default) issues only GET requests — safe against any server including production:

```bash
export OPENNMS_URL="https://opennms.example.com:8443"
export OPENNMS_USER="admin"
export OPENNMS_PASSWORD="secret"
python smoke_test.py
```

**Write mode** creates and then deletes objects. Only use against a dev or staging instance,
such as the throwaway Docker instance in `tests/live/compose.yaml`.

```bash
python smoke_test.py --write          # interactive prompt required
python smoke_test.py --write --yes    # skip prompt (CI pipelines only)
python smoke_test.py --skip get_flow  # skip tests by label prefix
```

## All methods

See the [API Reference](api.md) for all methods and TypedDict payload schemas.

## Acknowledgements

All API shapes are derived from the official
[OpenNMS](https://www.opennms.com/) REST API documentation.

[requests](https://docs.python-requests.org/) handles all HTTP communication.
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) renders this
documentation site.

[GitHub](https://github.com/), [Read the Docs](https://readthedocs.org/), and
[PyPI](https://pypi.org/) generously provide source hosting, CI, versioned
docs, and package distribution free of charge for open source projects.
