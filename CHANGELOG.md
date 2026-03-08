# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.4] - 2026-03-08

### Changed

- **Split connect/read timeout**: the `timeout` parameter now sets the read
  timeout; the connect timeout is capped at `min(timeout, 10)` seconds so
  unreachable hosts fail fast without waiting for the full read timeout.
  Fully transparent — the `timeout` parameter is unchanged.
- **Larger connection pool**: `HTTPAdapter` is always mounted with
  `pool_connections=4` and `pool_maxsize=20`, improving throughput for
  callers that parallelize requests via `ThreadPoolExecutor`.

## [0.4.3] - 2026-03-08

### Changed

- Project homepage in `pyproject.toml` now points to the Read the Docs
  documentation site instead of the GitHub repository.
- PyPI package description updated to "unofficial Python 3 client" to
  accurately reflect the project's relationship with OpenNMS.
- `README.md` and `docs/index.md`: library described as an "unofficial client"
  throughout; live-server validation qualified as read-only only; write mode
  noted as untested live.
- OpenNMS resources block added (Docs, REST API reference, Community forum).

## [0.4.2] - 2026-03-08

### Changed

- Read the Docs is now the canonical `Documentation` URL in `pyproject.toml`;
  GitHub Pages retained as `"API Reference"` pointing directly to the rendered
  method docs.
- All user-facing API reference links updated to `readthedocs.io` (no personal
  username in URLs).
- Acknowledgements added to `docs/index.md` so they appear on the RTD site as
  well as on GitHub and PyPI.
- RTD badge added to README.
- `CLAUDE.md` removed from the source distribution — it is AI developer
  tooling, not content for package consumers.

## [0.4.1] - 2026-03-08

### Added

- **`py.typed` marker (PEP 561)**: type checkers (mypy, pyright, Pylance) now
  automatically discover the package's TypedDicts and annotations without any
  user configuration.  `Typing :: Typed` PyPI classifier added.
- **Read the Docs support**: `.readthedocs.yaml` added for versioned docs at
  <https://opennms-api-wrapper.readthedocs.io>.
- **Security policy**: `SECURITY.md` added with supported-versions table and
  private disclosure instructions via GitHub Security Advisories.

### Changed

- Installation docs updated: `pip install opennms-api-wrapper` (PyPI) is now
  the primary install method; stale GitHub tarball URLs removed.
- Smoke test environment variables documented in the MkDocs site
  (`docs/index.md`), not only in the script and README.
- Test count removed from all locations except the README features list to
  reduce maintenance burden.

## [0.4.0] - 2026-03-07

### Added

- **Exception hierarchy**: HTTP errors now raise typed exceptions instead of
  bare `requests.exceptions.HTTPError`.  All exceptions are exported from
  the top-level package — no need to import `requests` in calling code.

  ```
  OpenNMSError
  └── OpenNMSHTTPError  (.status_code, .response)
      ├── BadRequestError      400
      ├── AuthenticationError  401
      ├── ForbiddenError       403
      ├── NotFoundError        404
      ├── ConflictError        409
      └── ServerError          5xx
  ```

- **Pagination helper**: `client.paginate(method, key, page_size=100,
  **kwargs)` — a generator that transparently handles `limit`/`offset`
  pagination and yields individual items from any list endpoint.

## [0.3.1] - 2026-03-07

### Added

- **TypedDict payload schemas**: `opennms_api_wrapper.types` now exports
  `TypedDict` classes covering every write-method argument.  Schemas appear
  in IDE autocompletion and in the API docs; all fields are optional
  (`total=False`) for maximum flexibility.  Hyphenated v1 keys (e.g.,
  `foreign-id`, `node-label`) use functional `TypedDict(...)` syntax; all
  other schemas use class syntax for full IDE autocompletion.
- **MkDocs Material docs site**: replaced pdoc with MkDocs Material +
  mkdocstrings.  `mkdocs.yml`, `docs/index.md`, and `docs/api.md` added.
  GitHub Pages workflow updated; all public methods and TypedDict schemas
  are now rendered at
  <https://cnewkirk.github.io/opennms-api-wrapper/api/>.
- **Retry with exponential backoff**: HTTP client now retries on connection
  errors and transient server errors (500, 502, 503, 504) with exponential
  backoff (0.5 s factor, up to 3 retries by default).  Uses urllib3's built-in
  `Retry` — no new dependencies.  Pass `retries=0` to disable.
- Smoke test: deeper drill-down coverage for nodes (single IP interface, SNMP
  interface, category, service), requisition nodes (interfaces, categories,
  assets), foreign source detectors/policies, business services, enlinkd link
  types/elements, classifications, eventconf sources, SCV credentials, and
  config management schemas.
- New unit tests for eventconf file upload (from path and from bytes).
- 7 new retry configuration tests (`test_retries.py`).

### Changed

- Mixin methods now pass empty `params={}` directly instead of using
  `params={} or None`; `requests` handles empty dicts correctly and this
  removes a subtle footgun.
- `_eventconf.py`: refactored to use `_post_files()`, `_post_text()`, and
  `_get_text()` base helpers instead of raw `_session` calls.
- `_classifications.py`: `import_classification_rules_csv()` refactored to
  use `_post_text()`.
- ADR-010 updated from "No retry" to "Retry with exponential backoff".

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
- 463-test suite (up from 301), all passing.
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
