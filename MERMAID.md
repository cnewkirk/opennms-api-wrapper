# Architecture Diagrams — opennms-api-wrapper

## Package composition

`OpenNMS` (in `client.py`) is built by multiple-inheriting from `_OpenNMSBase`
and 54 mixin classes — one per API resource group.  Dashed arrows represent
mixin inheritance; the solid arrow represents the base-class relationship.

```mermaid
flowchart TD
    caller(["Your Code"])

    subgraph fault_sg["Fault Management"]
        AlarmsMixin
        AlarmStatsMixin
        AlarmHistoryMixin
    end

    subgraph events_sg["Events and Notifications"]
        EventsMixin
        NotificationsMixin
        AcksMixin
    end

    subgraph inventory_sg["Network Inventory"]
        NodesMixin
        OutagesMixin
    end

    subgraph provision_sg["Provisioning"]
        RequisitionsMixin
        ForeignSourcesMixin
        ForeignSourcesConfigMixin
        RequisitionNamesMixin
        SnmpConfigMixin
        ProvisiondMixin
    end

    subgraph admin_sg["Administration"]
        GroupsMixin
        UsersMixin
        CategoriesMixin
        SchedOutagesMixin
        KscReportsMixin
        MonitoringLocationsMixin
        MinionsMixin
        MonitoringSystemsMixin
        WhoamiMixin
    end

    subgraph data_sg["Data and Reporting"]
        ResourcesMixin
        MeasurementsMixin
        HeatmapMixin
        FlowsMixin
        DeviceConfigMixin
        ClassificationsMixin
    end

    subgraph viz_sg["Visualization"]
        MapsMixin
        GraphsMixin
    end

    subgraph v2_sg["v2-only Resources"]
        SituationsMixin
        BusinessServicesMixin
        MetadataMixin
        DiscoveryMixin
        IpInterfacesV2Mixin
        SnmpInterfacesV2Mixin
        EnLinkdMixin
        ApplicationsMixin
        PerspectivePollerMixin
        UserDefinedLinksMixin
        SnmpMetadataMixin
        EventConfMixin
    end

    subgraph ops_sg["Operations"]
        AvailabilityMixin
        HealthMixin
        IfServicesMixin
        SituationFeedbackMixin
        AssetSuggestionsMixin
    end

    subgraph config_sg["Configuration"]
        ScvMixin
        ConfigMgmtMixin
        SnmpTrapNbiMixin
        EmailNbiMixin
        SyslogNbiMixin
        JavamailConfigMixin
    end

    InfoMixin["InfoMixin"]

    BaseClass["_OpenNMSBase - _base.py<br/>_get / _post / _put / _delete / _patch<br/>_parse / _url"]

    subgraph client_sg["client.py"]
        OpenNMS["OpenNMS<br/>~400 public methods - flat namespace"]
    end

    caller -->|"client.method()"| OpenNMS

    fault_sg     -.->|"mixin"| OpenNMS
    events_sg    -.->|"mixin"| OpenNMS
    inventory_sg -.->|"mixin"| OpenNMS
    provision_sg -.->|"mixin"| OpenNMS
    admin_sg     -.->|"mixin"| OpenNMS
    data_sg      -.->|"mixin"| OpenNMS
    viz_sg       -.->|"mixin"| OpenNMS
    v2_sg        -.->|"mixin"| OpenNMS
    ops_sg       -.->|"mixin"| OpenNMS
    config_sg    -.->|"mixin"| OpenNMS
    InfoMixin    -.->|"mixin"| OpenNMS

    BaseClass -->|"base class"| OpenNMS

    classDef mixin  fill:#dbeafe,stroke:#3b82f6,color:#1e3a5f
    classDef core   fill:#fef3c7,stroke:#d97706,color:#78350f,font-weight:bold
    classDef base   fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef caller fill:#f1f5f9,stroke:#94a3b8,color:#334155

    class AlarmsMixin,AlarmStatsMixin,AlarmHistoryMixin mixin
    class EventsMixin,NotificationsMixin,AcksMixin mixin
    class NodesMixin,OutagesMixin mixin
    class RequisitionsMixin,ForeignSourcesMixin,ForeignSourcesConfigMixin,RequisitionNamesMixin,SnmpConfigMixin,ProvisiondMixin mixin
    class GroupsMixin,UsersMixin,CategoriesMixin,SchedOutagesMixin,KscReportsMixin,MonitoringLocationsMixin,MinionsMixin,MonitoringSystemsMixin,WhoamiMixin mixin
    class ResourcesMixin,MeasurementsMixin,HeatmapMixin,FlowsMixin,DeviceConfigMixin,ClassificationsMixin mixin
    class MapsMixin,GraphsMixin mixin
    class SituationsMixin,BusinessServicesMixin,MetadataMixin,DiscoveryMixin,IpInterfacesV2Mixin,SnmpInterfacesV2Mixin,EnLinkdMixin,ApplicationsMixin,PerspectivePollerMixin,UserDefinedLinksMixin,SnmpMetadataMixin,EventConfMixin mixin
    class AvailabilityMixin,HealthMixin,IfServicesMixin,SituationFeedbackMixin,AssetSuggestionsMixin mixin
    class ScvMixin,ConfigMgmtMixin,SnmpTrapNbiMixin,EmailNbiMixin,SyslogNbiMixin,JavamailConfigMixin mixin
    class InfoMixin mixin
    class OpenNMS core
    class BaseClass base
    class caller caller
```

---

## Request lifecycle

What happens at runtime when any method on the client is called.

```mermaid
flowchart LR
    code(["your_code.py"])

    subgraph client_layer["client.py - OpenNMS"]
        method["client.get_alarms(severity='MAJOR')<br/>client.create_node(node_data)<br/>client.ack_alarm(42)"]
    end

    subgraph base_layer["_base.py - _OpenNMSBase"]
        direction TB
        helpers["_get / _post / _put / _delete<br/>selects v1 or v2 base URL<br/>timeout=30s on every request"]
        parse["_parse(response)<br/>1. raise_for_status()<br/>2. JSON       -> dict / list<br/>3. text/plain -> int / str<br/>4. 204        -> None"]
        helpers --> parse
    end

    subgraph sess_layer["requests.Session"]
        sess["HTTP Basic Auth<br/>Accept: application/json<br/>Content-Type: application/json<br/>SSL verification / connection pool"]
    end

    subgraph api_layer["OpenNMS Server - Horizon 30+"]
        direction TB
        v1["/opennms/rest/<br/>v1 REST API<br/>29 resource groups"]
        v2["/opennms/api/v2/<br/>v2 REST API<br/>6 resource groups"]
    end

    result(["Python object<br/>dict / list / int / None"])

    code         -->|"call"| client_layer
    client_layer -->|"delegates"| helpers
    helpers      -->|"HTTP request"| sess_layer
    sess_layer   -->|"HTTPS"| v1
    sess_layer   -->|"HTTPS"| v2
    v1           -->|"response"| parse
    v2           -->|"response"| parse
    parse        -->|"parsed value"| result

    classDef user    fill:#fff7ed,stroke:#f97316,color:#9a3412
    classDef client  fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef base    fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef session fill:#eff6ff,stroke:#3b82f6,color:#1e40af
    classDef api     fill:#fdf4ff,stroke:#a855f7,color:#6b21a8

    class code,result user
    class method client
    class helpers,parse base
    class sess session
    class v1,v2 api
```

---

*See [ARCHITECTURE.md](ARCHITECTURE.md) for the decision record behind each design choice.*
