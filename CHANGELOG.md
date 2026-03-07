# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
