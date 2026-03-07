# opennms-api-wrapper

[![CI](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/cnewkirk/opennms-api-wrapper)](https://github.com/cnewkirk/opennms-api-wrapper/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Pre-release — v0.1.0**
> This is an early release.  The API is functional and fully tested against
> OpenNMS Horizon 35, but may change before v1.0.0.  Feedback and issue
> reports are welcome.

A thin, dependency-minimal Python 3 wrapper for the
[OpenNMS](https://www.opennms.com/) REST API (Horizon 35).

## Features

- Covers every v1 (`/opennms/rest/`) and v2 (`/opennms/api/v2/`) endpoint
- JSON everywhere — no XML handling required
- Single runtime dependency: [`requests`](https://docs.python-requests.org/)
- Synchronous and straightforward — no async complexity
- 290-test suite with full method coverage

## Installation

**From the GitHub release** (no clone required — recommended for most users):

```bash
pip install https://github.com/cnewkirk/opennms-api-wrapper/archive/refs/tags/v0.1.0.tar.gz
```

**From source** (clone first, then install):

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
pip install .
```

When the package is published to PyPI, installation will simplify to
`pip install opennms-api-wrapper`.

## Quick start

```python
import opennms_api_wrapper as opennms

client = opennms.OpenNMS(
    url="https://opennms.example.com:8980",
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

# List alarms with FIQL filter (v2)
alarms = client.get_alarms_v2(fiql="severity==MAJOR")
```

## API coverage

| Resource group | Methods |
|---|---|
| Alarms (v1 + v2) | list, get, count, ack/unack/clear/escalate, bulk ops |
| Alarm statistics | stats, stats by severity |
| Alarm history | history, history at timestamp, state changes |
| Events | list, get, count, create, ack/unack, bulk ack/unack |
| Nodes | full CRUD + IP interfaces, SNMP interfaces, services, categories, assets, hardware |
| Outages | list, get, count, node outages |
| Notifications | list, get, count, trigger destination path |
| Acknowledgements | list, get, count, create, ack/unack notification |
| Requisitions | full CRUD including nodes, interfaces, services, categories, assets |
| Foreign sources | full CRUD including detectors and policies |
| SNMP configuration | get, set |
| Groups | full CRUD + user and category membership |
| Users | full CRUD + role assignment |
| Categories | full CRUD + node and group associations |
| Scheduled outages | full CRUD + daemon associations |
| KSC reports | list, get, count, create, update |
| Resources | list, get, get for node, select, delete |
| Measurements | single attribute (GET), multi-source (POST) |
| Heatmap | outages + alarms × categories / foreign sources / services / nodes |
| Maps | full CRUD + map elements |
| Topology graphs | containers, graph, graph view (POST), search suggestions, search results |
| Flows | count, exporters, applications, conversations, hosts |
| Device configuration | list, get, get by interface, latest, download, backup |
| Situations (v2) | list, create, add alarms, clear, accept, remove alarms |
| Business services (v2) | full CRUD |
| Metadata (v2) | full CRUD for node, interface, and service metadata |
| Server info | get |
| Discovery (v2) | submit scan configuration |
| IP interfaces (v2) | list with FIQL |
| SNMP interfaces (v2) | list with FIQL |

## Authentication

Basic authentication is used. Pass `verify_ssl=False` to disable certificate
verification (useful for self-signed certs in lab environments):

```python
client = opennms.OpenNMS(
    url="https://opennms.example.com:8980",
    username="admin",
    password="admin",
    verify_ssl=False,
)
```

## Development

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/cnewkirk/opennms-api-wrapper.

## Acknowledgements

This library was designed and tested by a human, with implementation
assistance from [Claude Code](https://claude.ai/code) (Anthropic). All API
shapes are derived from the official OpenNMS Horizon 35 REST API
documentation.
