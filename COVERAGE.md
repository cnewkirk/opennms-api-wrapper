# REST API coverage

What the wrapper covers, measured against the OpenNMS
[Meridian 2025 REST API documentation](https://docs.opennms.com/meridian/2025/development/rest/rest-api.html)
index.

## Summary

- 69 resource areas documented for Meridian 2025.
- 66 covered by a wrapper mixin — every documented area except the
  3 web-UI-internal APIs, which are intentionally out of scope.
- 2 wrapper mixins target endpoints outside the Meridian 2025 docs
  index (see the last section).

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
| Data Choices API (`datachoices`) | `DataChoicesMixin` |
| Device Config (`device_config`) | `DeviceConfigMixin` |
| Discovery (`discovery`) | `DiscoveryMixin` |
| Email NBI Configuration (`emailnbi-config`) | `EmailNbiMixin` |
| Events (`events`) | `EventsMixin` |
| Filesystem API (`filesystem`) | `FilesystemMixin` |
| Flow API (`flows`) | `FlowsMixin` |
| Flow Classification (`classifications`) | `ClassificationsMixin` |
| Foreign Source Configuration (`foreign_sources_config`) | `ForeignSourcesConfigMixin` |
| Foreign Sources (`foreign_sources`) | `ForeignSourcesMixin` |
| Geocoding API (`geocoding`) | `GeocodingMixin` |
| Geolocation API (`geolocation`) | `GeolocationMixin` |
| Grafana Endpoints API (`endpoints_grafana`) | `GrafanaEndpointsMixin` |
| Graph API (`graph`) | `GraphsMixin` |
| GraphML API (`graphml`) | `GraphMlMixin` |
| Groups (`groups`) | `GroupsMixin` |
| Hardware Inventory (`hardware_inventory`) | `NodesMixin` |
| Health (`health_rest`) | `HealthMixin` |
| Heatmap (`heatmap`) | `HeatmapMixin` |
| Info (`info`) | `InfoMixin` |
| IP Interfaces (`ipinterfaces`) | `IpInterfacesV2Mixin` (+ v1 via `NodesMixin`) |
| JavaMail Configuration (`javamail-config`) | `JavamailConfigMixin` |
| KSC Reports (`ksc_reports`) | `KscReportsMixin` |
| Logs API (`logs`) | `LogsMixin` |
| Measurements (`measurements`) | `MeasurementsMixin` |
| Metadata (`meta-data`) | `MetadataMixin` |
| Minions (`minions`) | `MinionsMixin` |
| Monitored Services (`ifservices`) | `IfServicesMixin` |
| Monitoring Locations (`monitoring_locations`) | `MonitoringLocationsMixin` |
| Monitoring Systems (`monitoring_systems`) | `MonitoringSystemsMixin` |
| News Feed (`newsfeed`) | `NewsFeedMixin` |
| Node Links (`node_links`) | `EnLinkdMixin` |
| Nodes (`nodes`) | `NodesMixin` |
| Notifications (`notifications`) | `NotificationsMixin` |
| Outage Timelines (`outage_timeline`) | `TimelineMixin` |
| Outages (`outages`) | `OutagesMixin` |
| Perspective Poller (`perspectivepoller`) | `PerspectivePollerMixin` |
| Provisiond Status (`provisiond_status`) | `ProvisiondMixin` |
| Realtime Console Data (`rtc`) | `AvailabilityMixin` |
| Reports API (`reports`) | `ReportsMixin` |
| Requisition Names (`requisition_names`) | `RequisitionNamesMixin` |
| Requisitions (`requisitions`) | `RequisitionsMixin` |
| Resources (`resources`) | `ResourcesMixin` |
| Scheduled Outages (`scheduled_outages`) | `SchedOutagesMixin` |
| Search API (`search`) | `SearchMixin` |
| Secure Credentials Vault (`scv`) | `ScvMixin` |
| Situation Feedback (`situation-feedback`) | `SituationFeedbackMixin` |
| Situations (`situations`) | `SituationsMixin` |
| SNMP Configuration (`snmp_configuration`) | `SnmpConfigMixin` |
| SNMP Interfaces (`snmpinterfaces`) | `SnmpInterfacesV2Mixin` (+ v1 via `NodesMixin`) |
| SNMP Metadata (`snmpmetadata`) | `SnmpMetadataMixin` |
| SNMP Trap NBI Configuration (`snmptrapnbi-config`) | `SnmpTrapNbiMixin` |
| Status API (`status`) | `StatusMixin` |
| Syslog NBI Configuration (`syslognbi-config`) | `SyslogNbiMixin` |
| User-Defined Links (`user-defined-links`) | `UserDefinedLinksMixin` |
| Users (`users`) | `UsersMixin` |
| Whoami (`whoami`) | `WhoamiMixin` |

## Out of scope (web-UI-internal)

Menu API (`menu`), Web Assets API (`web_assets`), and UI Extension /
Plugins API (`plugins`) exist to serve the OpenNMS web UI itself and
offer no monitoring or automation value through a wrapper.

## Wrapper endpoints outside the Meridian 2025 docs index

- `EventConfMixin` (`/api/v2/eventconf`) — the API exists in
  OpenNMS Horizon 35+ only and is therefore not in the Meridian
  2025 docs.
- `MapsMixin` (`/rest/maps`) — the maps API was removed upstream in
  OpenNMS Horizon 16; the mixin is retained for backwards
  compatibility with pre-16 servers and 404s on newer ones.
