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

## All methods

See the [API Reference](api.md) for all methods and TypedDict payload schemas.
