# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-07

### Fixed

- Accept header now includes `text/plain;q=0.9` to prevent 406 errors on
  `/count` endpoints in some OpenNMS versions.
- `get_node_count()` uses the v2 API (`GET /api/v2/nodes?limit=1`) and
  extracts `totalCount`. The v1 `/rest/nodes` endpoint does not expose a
  `/count` sub-resource.

### Changed

- Smoke test: endpoints that depend on optional plugins (alarm history,
  hardware inventory, flows, situations) or heavy queries (resources) now
  report as WARN instead of FAIL.  Each warning cites the required plugin
  or feature.
- Smoke test: events query filters by lowest-ID node to avoid full table
  scans on large databases.

### Added

- Smoke test: `--skip` flag to skip tests by label prefix (e.g.,
  `--skip get_flow` skips all flow tests).
- Smoke test: `OPENNMS_TIMEOUT` env var (default 60 seconds).
- Validated against OpenNMS Meridian 2024.3.0 (65 passed, 0 failed).

## [0.1.0] - 2026-03-06

### Added

- Initial release covering all OpenNMS Horizon 35 REST API endpoints (v1
  and v2).
- Single `OpenNMS` client class importable as `import opennms_api_wrapper as
  opennms`.
- JSON-only request/response handling throughout; no XML dependency.
- Synchronous, dependency-minimal design (only `requests` required at
  runtime).
- 290-test suite with full method coverage; HTTP mocked at the adapter level
  using the `responses` library — no live server required to run tests.
- Resource groups covered: alarms, alarm statistics, alarm history, events,
  nodes (with IP interfaces, SNMP interfaces, monitored services, categories,
  assets, and hardware inventory), outages, notifications, acknowledgements,
  requisitions, foreign sources, SNMP configuration, groups, users,
  categories, scheduled outages, KSC reports, resources, measurements,
  heatmap, maps, topology graphs, flows, device configuration, situations
  (v2), business services (v2), metadata (v2), server info, discovery (v2),
  and global IP/SNMP interface views (v2).
