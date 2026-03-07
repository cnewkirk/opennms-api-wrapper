# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-07

### Added

- Near-complete OpenNMS REST API coverage: 24 new endpoint groups with ~150
  new public methods, closing all Tier 1 (core ops), Tier 2
  (feature-specific), and Tier 3 (config/admin) API gaps.
- New Tier 1 mixins: monitoring locations, minions, ifservices, availability,
  health, whoami.
- New Tier 2 mixins: classifications, situation feedback, user-defined links
  (v2), applications (v2), perspective poller (v2), foreign sources config,
  requisition names, SNMP metadata (v2), provisiond (v2), event configuration
  (v2), monitoring systems, asset suggestions.
- New Tier 3 mixins: secure credentials vault (SCV), configuration management,
  SNMP trap NBI config, email NBI config, syslog NBI config, javamail config.
- Extended existing mixins: prefab graph methods (+4), flow DSCP and graph URL
  (+4), business service edges/functions/daemon reload (+10).
- `_patch()` HTTP helper in base class for PATCH requests (used by eventconf
  enable/disable).
- `_delete()` now accepts optional `json_data` parameter (used by eventconf
  bulk delete).
- 454-test suite (up from 301), all passing.
- Smoke test sections for all new endpoint groups (140 total checks, up from
  ~80).
- Validated against OpenNMS Meridian 2024.3.0 (106 passed, 0 failed, 25
  warned).

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
