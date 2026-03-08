# opennms-api-wrapper

[![CI](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/opennms-api-wrapper)](https://pypi.org/project/opennms-api-wrapper/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cnewkirk/opennms-api-wrapper/blob/main/LICENSE)

A thin, dependency-minimal Python 3 wrapper for the [OpenNMS](https://www.opennms.com/) REST API (Horizon 35+).
Validated against OpenNMS Meridian 2024.3.0.

## Installation

```bash
pip install opennms-api-wrapper
```

**From source** (latest development version):

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
pip install .
```

## Quick start

```python
import opennms_api_wrapper as opennms

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

**Write mode** creates and then deletes objects. Only use against a dev or staging instance:

```bash
python smoke_test.py --write          # interactive prompt required
python smoke_test.py --write --yes    # skip prompt (CI pipelines only)
python smoke_test.py --skip get_flow  # skip tests by label prefix
```

## All methods

See the [API Reference](api.md) for all methods and TypedDict payload schemas.

## Acknowledgements

This library was designed and tested by a human, with implementation
assistance from [Claude Code](https://claude.ai/code) (Anthropic). All API
shapes are derived from the official [OpenNMS](https://www.opennms.com/)
Horizon 35 REST API documentation.

[requests](https://docs.python-requests.org/) handles all HTTP communication.
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) renders this
documentation site.

[GitHub](https://github.com/), [Read the Docs](https://readthedocs.org/), and
[PyPI](https://pypi.org/) generously provide source hosting, CI, versioned
docs, and package distribution free of charge for open source projects.
