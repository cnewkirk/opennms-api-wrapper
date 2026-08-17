# REST API coverage

Audit of wrapper coverage against the OpenNMS
[Meridian 2025 REST API documentation](https://docs.opennms.com/meridian/2025/development/rest/rest-api.html)
index. Tracked in
[#44](https://github.com/cnewkirk/opennms-api-wrapper/issues/44).

Last audited: 2026-08-17 (Meridian 2025 docs, wrapper as of `main`).

Method: every resource area listed in the docs index was mapped to the
mixin whose methods call that area's root endpoint path. Node Links,
Status, and Graph API were additionally verified endpoint-by-endpoint
against their individual doc pages.

## Summary

- 69 resource areas documented for Meridian 2025.
- 53 covered by a wrapper mixin.
- 13 not covered (candidates for new mixins — see `TODO.md`).
- 3 intentionally out of scope (web-UI-internal APIs).
- 3 wrapper mixins target endpoints absent from the Meridian 2025 docs
  and need live verification or deprecation.

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

## Not covered (candidates for new mixins)

| Documented area (doc page) | Endpoint |
| --- | --- |
| Status API (`status`) | `/api/v2/status/...` |
| Outage Timelines (`outage_timeline`) | `/rest/timeline` |
| Reports API (`reports`) | database reports |
| Realtime Console Data (`rtc`) | `/rest/rtc` |
| Search API (`search`) | search service |
| GraphML API (`graphml`) | `/rest/graphml` |
| Grafana Endpoints API (`endpoints_grafana`) | Grafana endpoint config |
| Geocoding API (`geocoding`) | geocoding config |
| Geolocation API (`geolocation`) | node geolocation resolution |
| Logs API (`logs`) | server log access |
| Filesystem API (`filesystem`) | config filesystem access |
| Data Choices API (`datachoices`) | usage-statistics opt-in |
| News Feed (`newsfeed`) | news feed proxy |

## Out of scope (web-UI-internal)

Menu API (`menu`), Web Assets API (`web_assets`), and UI Extension /
Plugins API (`plugins`) exist to serve the OpenNMS web UI itself and
offer no monitoring or automation value through a wrapper.

## Wrapper endpoints absent from the Meridian 2025 docs

These mixins wrap endpoints that no longer appear in the current docs
index. Verify against a live modern server; deprecate if removed
upstream.

| Mixin | Endpoint |
| --- | --- |
| `AvailabilityMixin` | `/rest/availability` |
| `MapsMixin` | `/rest/maps` |
| `EventConfMixin` | `/rest/eventconf` |
