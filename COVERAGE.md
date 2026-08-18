# REST API coverage

Audit of wrapper coverage against the OpenNMS
[Meridian 2025 REST API documentation](https://docs.opennms.com/meridian/2025/development/rest/rest-api.html)
index. Tracked in
[#44](https://github.com/cnewkirk/opennms-api-wrapper/issues/44).

Last audited: 2026-08-17 (Meridian 2025 docs, wrapper as of `main`).
Gap closure implemented in
[#46](https://github.com/cnewkirk/opennms-api-wrapper/issues/46).

Method: every resource area listed in the docs index was mapped to the
mixin whose methods call that area's root endpoint path. Node Links,
Status, and Graph API were additionally verified endpoint-by-endpoint
against their individual doc pages. All 12 new endpoint groups were
then live-validated against a Meridian 2025 foundation instance
(Horizon 34.0.1, `tests/live/compose.yaml`) — 37/37 checks passing,
with the Filesystem API exercised to its expected 403 (the
`FILESYSTEM EDITOR` role is not granted to admin by default).

## Summary

- 69 resource areas documented for Meridian 2025.
- 66 covered by a wrapper mixin — every documented area except the
  3 web-UI-internal APIs, which are intentionally out of scope.
- 2 wrapper mixins target endpoints outside the Meridian 2025 docs:
  `EventConfMixin` (verified still present upstream, just
  undocumented) and `MapsMixin` (removed upstream in Horizon 16;
  retained for backwards compatibility with annotated docstrings).

## Covered resource areas

| Documented area (doc page) | Mixin |
| --- | --- |
| Acknowledgements (`acknowledgements`) | `AcksMixin` |
| Alarm History (`alarm_history`) | `AlarmHistoryMixin` |
| Alarm Statistics (`alarm_statistics`) | `AlarmStatsMixin` |
| Alarms (`alarms`) | `AlarmsMixin` |
| Applications (`applications`) | `ApplicationsMixin` |
| Asset Suggestions (`asset_suggestions`) | `AssetSuggestionsMixin` |
| Business Service Monitoring (`bsm-development`) | `BusinessServicesMixin` |
| Categories (`categories`) | `CategoriesMixin` |
| Config Management (`config_management`) | `ConfigMgmtMixin` |
| Device Config (`device_config`) | `DeviceConfigMixin` |
| Discovery (`discovery`) | `DiscoveryMixin` |
| Email NBI Configuration (`emailnbi-config`) | `EmailNbiMixin` |
| Events (`events`) | `EventsMixin` |
| Flow API (`flows`) | `FlowsMixin` |
| Flow Classification (`classifications`) | `ClassificationsMixin` |
| Foreign Source Configuration (`foreign_sources_config`) | `ForeignSourcesConfigMixin` |
| Foreign Sources (`foreign_sources`) | `ForeignSourcesMixin` |
| Graph API (`graph`) | `GraphsMixin` |
| Groups (`groups`) | `GroupsMixin` |
| Hardware Inventory (`hardware_inventory`) | `NodesMixin` (`get_node_hardware_inventory` et al.) |
| Health (`health_rest`) | `HealthMixin` |
| Heatmap (`heatmap`) | `HeatmapMixin` |
| Info (`info`) | `InfoMixin` |
| IP Interfaces (`ipinterfaces`) | `IpInterfacesV2Mixin` (+ v1 via `NodesMixin`) |
| JavaMail Configuration (`javamail-config`) | `JavamailConfigMixin` |
| KSC Reports (`ksc_reports`) | `KscReportsMixin` |
| Measurements (`measurements`) | `MeasurementsMixin` |
| Metadata (`meta-data`) | `MetadataMixin` |
| Minions (`minions`) | `MinionsMixin` |
| Monitored Services (`ifservices`) | `IfServicesMixin` |
| Monitoring Locations (`monitoring_locations`) | `MonitoringLocationsMixin` |
| Monitoring Systems (`monitoring_systems`) | `MonitoringSystemsMixin` |
| Node Links (`node_links`) | `EnLinkdMixin` (all 11 documented endpoints) |
| Nodes (`nodes`) | `NodesMixin` |
| Notifications (`notifications`) | `NotificationsMixin` |
| Outages (`outages`) | `OutagesMixin` |
| Perspective Poller (`perspectivepoller`) | `PerspectivePollerMixin` |
| Provisiond Status (`provisiond_status`) | `ProvisiondMixin` |
| Realtime Console Data (`rtc`) | `AvailabilityMixin` (the page documents `/rest/availability`) |
| Requisition Names (`requisition_names`) | `RequisitionNamesMixin` |
| Requisitions (`requisitions`) | `RequisitionsMixin` |
| Resources (`resources`) | `ResourcesMixin` |
| Scheduled Outages (`scheduled_outages`) | `SchedOutagesMixin` |
| Secure Credentials Vault (`scv`) | `ScvMixin` |
| Situation Feedback (`situation-feedback`) | `SituationFeedbackMixin` |
| Situations (`situations`) | `SituationsMixin` |
| SNMP Configuration (`snmp_configuration`) | `SnmpConfigMixin` |
| SNMP Interfaces (`snmpinterfaces`) | `SnmpInterfacesV2Mixin` (+ v1 via `NodesMixin`) |
| SNMP Metadata (`snmpmetadata`) | `SnmpMetadataMixin` |
| SNMP Trap NBI Configuration (`snmptrapnbi-config`) | `SnmpTrapNbiMixin` |
| Syslog NBI Configuration (`syslognbi-config`) | `SyslogNbiMixin` |
| User-Defined Links (`user-defined-links`) | `UserDefinedLinksMixin` |
| Users (`users`) | `UsersMixin` |
| Whoami (`whoami`) | `WhoamiMixin` |
| Status API (`status`) | `StatusMixin` |
| Outage Timelines (`outage_timeline`) | `TimelineMixin` (`/rest/timeline` — the upstream service path, verified in `TimelineRestService.java`) |
| Reports API (`reports`) | `ReportsMixin` |
| Search API (`search`) | `SearchMixin` |
| GraphML API (`graphml`) | `GraphMlMixin` (XML bodies — GraphML is an XML format) |
| Grafana Endpoints API (`endpoints_grafana`) | `GrafanaEndpointsMixin` |
| Geocoding API (`geocoding`) | `GeocodingMixin` |
| Geolocation API (`geolocation`) | `GeolocationMixin` |
| Logs API (`logs`) | `LogsMixin` |
| Filesystem API (`filesystem`) | `FilesystemMixin` |
| Data Choices API (`datachoices`) | `DataChoicesMixin` |
| News Feed (`newsfeed`) | `NewsFeedMixin` |

## Out of scope (web-UI-internal)

Menu API (`menu`), Web Assets API (`web_assets`), and UI Extension /
Plugins API (`plugins`) exist to serve the OpenNMS web UI itself and
offer no monitoring or automation value through a wrapper.

## Wrapper endpoints outside the Meridian 2025 docs index

Resolved 2026-08-17 against the OpenNMS source on GitHub:

- `AvailabilityMixin` (`/rest/availability`) — documented after all:
  the Realtime Console Data page (`rtc`) covers exactly these
  endpoints. Covered, nothing to do.
- `EventConfMixin` (`/api/v2/eventconf`) — `EventConfRestService`
  exists upstream from Horizon 35; live-verified 404 on Horizon 34
  (the Meridian 2025 foundation), which is why the API is absent
  from the Meridian 2025 docs. Kept as-is for Horizon 35+ servers.
- `MapsMixin` (`/rest/maps`) — `OnmsMapRestService` last shipped in
  Horizon 15 and was removed in Horizon 16 (2015). The mixin is
  retained for backwards compatibility with pre-16 servers; every
  method docstring notes that the call 404s on newer servers.
