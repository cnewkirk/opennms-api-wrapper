"""
Accurate OpenNMS Horizon 35 REST API response shapes for use in tests.

Field names are derived from OnmsAlarm, OnmsNode, OnmsIpInterface,
OnmsSnmpInterface, OnmsEvent, OnmsOutage, OnmsNotification,
OnmsAcknowledgment, and OnmsAssetRecord (OpenNMS Horizon 35 JavaDoc).

List responses use the singular resource name as the wrapper key plus
``totalCount``, ``count``, and ``offset``.

Date strings use the OpenNMS format: ``"YYYY-MM-DDTHH:MM:SS.sssZ"``
(ISO-8601 with milliseconds and +0000 UTC offset).
"""

# ---------------------------------------------------------------------------
# Shared building blocks
# ---------------------------------------------------------------------------

SERVICE_TYPE = {"id": 1, "name": "ICMP"}

EVENT_PARM = {
    "parmName": "ifIndex",
    "value": {"content": "6", "type": "string", "encoding": "text"},
}

# ---------------------------------------------------------------------------
# Alarm
# ---------------------------------------------------------------------------

ALARM = {
    "id": 42,
    "uei": "uei.opennms.org/nodes/nodeDown",
    "nodeId": 1,
    "nodeLabel": "router01.example.com",
    "ipAddress": "192.168.1.1",
    "serviceType": SERVICE_TYPE,
    "reductionKey": "uei.opennms.org/nodes/nodeDown::1",
    "clearKey": None,
    "alarmType": 1,
    "count": 3,
    "severity": "MAJOR",
    "firstEventTime": "2024-06-01T08:00:00.000+0000",
    "lastEventTime": "2024-06-01T09:30:00.000+0000",
    "logMsg": "Node router01.example.com is down.",
    "description": "<p>Router is not responding.</p>",
    "operInstruct": None,
    "ackTime": "2024-06-01T09:45:00.000+0000",
    "ackUser": "admin",
    "x733ProbableCause": 0,
    "parameters": [EVENT_PARM],
    "relatedAlarms": [],
    "lastEvent": {
        "id": 1001,
        "uei": "uei.opennms.org/nodes/nodeDown",
        "time": "2024-06-01T09:30:00.000+0000",
    },
}

ALARM_LIST = {
    "alarm": [ALARM],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Alarm Statistics
# ---------------------------------------------------------------------------

ALARM_STATS = {
    "totalCount": 15,
    "acknowledgedCount": 5,
    "unacknowledgedCount": 10,
    "newestAcknowledged": ALARM,
    "newestUnacknowledged": {**ALARM, "id": 43, "ackTime": None, "ackUser": None},
    "oldestAcknowledged": {**ALARM, "id": 10},
    "oldestUnacknowledged": {**ALARM, "id": 11, "ackTime": None, "ackUser": None},
}

ALARM_STATS_BY_SEVERITY = [
    {"severity": "CRITICAL", "totalCount": 2, "acknowledgedCount": 0, "unacknowledgedCount": 2},
    {"severity": "MAJOR",    "totalCount": 5, "acknowledgedCount": 2, "unacknowledgedCount": 3},
    {"severity": "MINOR",    "totalCount": 4, "acknowledgedCount": 2, "unacknowledgedCount": 2},
]

# ---------------------------------------------------------------------------
# Alarm History
# ---------------------------------------------------------------------------

ALARM_HISTORY_STATE = {
    "id": "42:2024-06-01T09:30:00.000+0000",
    "alarmId": 42,
    "time": "2024-06-01T09:30:00.000+0000",
    "type": "ALARM_CREATED",
    "user": None,
    "alarm": ALARM,
}

ALARM_HISTORY_STATES_LIST = [ALARM_HISTORY_STATE]
ALARM_HISTORY_LIST = [ALARM]

# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

EVENT = {
    "id": 1001,
    "uei": "uei.opennms.org/nodes/nodeDown",
    "label": "Node Down",
    "time": "2024-06-01T09:30:00.000+0000",
    "createTime": "2024-06-01T09:30:01.000+0000",
    "source": "OpenNMS.Poller.Monitor.IcmpMonitor",
    "nodeId": 1,
    "nodeLabel": "router01.example.com",
    "ipAddress": "192.168.1.1",
    "serviceType": SERVICE_TYPE,
    "severity": "MAJOR",
    "logMsg": "Node router01.example.com is down.",
    "logMsgDest": "logndisplay",
    "eventDisplay": "Y",
    "ackUser": None,
    "ackTime": None,
    "parameters": [EVENT_PARM],
}

EVENT_LIST = {
    "event": [EVENT],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

NODE = {
    "id": 1,
    "label": "router01.example.com",
    "labelSource": "H",
    "foreignSource": "Routers",
    "foreignId": "router01",
    "location": "Default",
    "type": "A",
    "sysObjectId": ".1.3.6.1.4.1.9.1.1",
    "sysName": "router01",
    "sysDescription": "Cisco IOS Software, Version 15.1",
    "sysContact": "noc@example.com",
    "sysLocation": "DC1 Rack A1",
    "createTime": "2024-01-15T12:00:00.000+0000",
    "lastCapsdPoll": "2024-06-01T09:00:00.000+0000",
    "categories": [{"id": 2, "name": "Production"}],
}

NODE_LIST = {
    "node": [NODE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# IP Interface
# ---------------------------------------------------------------------------

IP_INTERFACE = {
    "id": 101,
    "ipAddress": "192.168.1.1",
    "hostName": "router01.example.com",
    "isManaged": "M",
    "snmpPrimary": "P",
    "ipLastCapsdPoll": "2024-06-01T09:00:00.000+0000",
    "isDown": False,
    "nodeId": 1,
    "monitoredServices": [
        {
            "id": 201,
            "serviceName": "ICMP",
            "status": "A",
            "lastGood": "2024-06-01T09:28:00.000+0000",
            "lastFail": "2024-06-01T08:00:00.000+0000",
            "qualifier": None,
            "source": "P",
            "respond": "Y",
            "down": False,
            "serviceType": SERVICE_TYPE,
        }
    ],
}

IP_INTERFACE_LIST = {
    "ipInterface": [IP_INTERFACE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# SNMP Interface
# ---------------------------------------------------------------------------

SNMP_INTERFACE = {
    "id": 301,
    "ifIndex": 6,
    "ifName": "GigabitEthernet0/0",
    "ifDescr": "GigabitEthernet0/0",
    "ifAlias": "uplink-to-core",
    "ifType": 6,
    "ifOperStatus": 1,
    "ifAdminStatus": 1,
    "ifSpeed": 1000000000,
    "physAddr": "04:01:3f:75:f1:01",
    "collect": "C",
    "poll": "P",
    "nodeId": 1,
    "lastCapsdPoll": "2024-06-01T09:00:00.000+0000",
}

SNMP_INTERFACE_LIST = {
    "snmpInterface": [SNMP_INTERFACE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Monitored Service
# ---------------------------------------------------------------------------

MONITORED_SERVICE = {
    "id": 201,
    "serviceName": "ICMP",
    "status": "A",
    "lastGood": "2024-06-01T09:28:00.000+0000",
    "lastFail": "2024-06-01T08:00:00.000+0000",
    "qualifier": None,
    "source": "P",
    "respond": "Y",
    "down": False,
    "serviceType": SERVICE_TYPE,
}

MONITORED_SERVICE_LIST = {
    "service": [MONITORED_SERVICE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Asset Record
# ---------------------------------------------------------------------------

ASSET_RECORD = {
    "id": 1,
    "category": "Routers",
    "manufacturer": "Cisco",
    "vendor": "Cisco Systems",
    "modelNumber": "ISR4331",
    "serialNumber": "FDO2147A0BC",
    "description": "Core distribution router",
    "operatingSystem": "IOS-XE 17.3",
    "rack": "A",
    "building": "HQ",
    "floor": "1",
    "room": "DC1",
    "country": "US",
    "lastModifiedBy": "admin",
    "lastModifiedDate": "2024-05-20T14:00:00.000+0000",
}

# ---------------------------------------------------------------------------
# Hardware Entity
# ---------------------------------------------------------------------------

HARDWARE_ENTITY = {
    "id": 1,
    "entityPhysicalIndex": 1,
    "entPhysicalDescr": "Cisco ISR4331 chassis",
    "entPhysicalClass": 3,
    "entPhysicalName": "Chassis",
    "entPhysicalSerialNum": "FDO2147A0BC",
    "entPhysicalMfgName": "Cisco Systems",
    "entPhysicalModelName": "ISR4331",
    "entPhysicalIsFRU": True,
    "children": [],
}

# ---------------------------------------------------------------------------
# Outage
# ---------------------------------------------------------------------------

OUTAGE = {
    "id": 501,
    "ifLostService": "2024-06-01T08:00:00.000+0000",
    "ifRegainedService": None,
    "ipAddress": "192.168.1.1",
    "serviceType": SERVICE_TYPE,
    "monitoredService": {
        "id": 201,
        "serviceName": "ICMP",
        "status": "A",
        "down": True,
        "serviceType": SERVICE_TYPE,
        "ipInterface": {"id": 101, "ipAddress": "192.168.1.1", "nodeId": 1},
    },
    "node": {"id": 1, "label": "router01.example.com"},
}

OUTAGE_LIST = {
    "outage": [OUTAGE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

NOTIFICATION = {
    "notifyId": 601,
    "textMsg": "Node router01.example.com is down.",
    "subject": "node down",
    "numericMsg": None,
    "pageTime": "2024-06-01T08:01:00.000+0000",
    "respondTime": "2024-06-01T08:10:00.000+0000",
    "answeredBy": "admin",
    "ipAddress": "192.168.1.1",
    "queueId": "default",
    "notifConfigName": "nodeDown",
    "eventUei": "uei.opennms.org/nodes/nodeDown",
    "ackUser": "admin",
    "ackTime": "2024-06-01T08:10:00.000+0000",
    "ackId": 701,
    "serviceType": SERVICE_TYPE,
    "node": {"id": 1, "label": "router01.example.com"},
}

NOTIFICATION_LIST = {
    "notification": [NOTIFICATION],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Acknowledgement
# ---------------------------------------------------------------------------

ACKNOWLEDGEMENT = {
    "id": 701,
    "ackTime": "2024-06-01T08:10:00.000+0000",
    "ackUser": "admin",
    "ackType": "ALARM",
    "ackAction": "ACKNOWLEDGE",
    "refId": 42,
}

ACKNOWLEDGEMENT_LIST = {
    "ack": [ACKNOWLEDGEMENT],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Requisition
# ---------------------------------------------------------------------------

REQUISITION_NODE = {
    "foreign-id": "router01",
    "node-label": "router01.example.com",
    "location": "Default",
    "interface": [
        {
            "ip-addr": "192.168.1.1",
            "snmp-primary": "P",
            "status": 1,
            "monitored-service": [{"service-name": "ICMP"}, {"service-name": "SNMP"}],
        }
    ],
    "category": [{"name": "Production"}],
    "asset": [{"name": "manufacturer", "value": "Cisco"}],
    "meta-data": [],
}

REQUISITION = {
    "foreign-source": "Routers",
    "date-stamp": "2024-06-01T10:00:00.000+0000",
    "node": [REQUISITION_NODE],
    "node-count": 1,
}

REQUISITION_LIST = {"requisition": [REQUISITION], "count": 1}

REQUISITION_NODE_LIST = {
    "node": [REQUISITION_NODE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

REQUISITION_INTERFACE = REQUISITION_NODE["interface"][0]
REQUISITION_SERVICE = {"service-name": "ICMP"}
REQUISITION_CATEGORY = {"name": "Production"}
REQUISITION_ASSET = {"name": "manufacturer", "value": "Cisco"}

# ---------------------------------------------------------------------------
# Foreign Source
# ---------------------------------------------------------------------------

FOREIGN_SOURCE_DETECTOR = {
    "name": "ICMP",
    "class": "org.opennms.netmgt.provision.detector.icmp.IcmpDetector",
    "parameter": [],
}

FOREIGN_SOURCE_POLICY = {
    "name": "Do Not Persist Discovered IPs",
    "class": "org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy",
    "parameter": [{"key": "action", "value": "DO_NOT_PERSIST"}],
}

FOREIGN_SOURCE = {
    "name": "Routers",
    "date-stamp": "2024-05-20T14:00:00.000+0000",
    "scan-interval": "1d",
    "detectors": [FOREIGN_SOURCE_DETECTOR],
    "policies": [FOREIGN_SOURCE_POLICY],
}

FOREIGN_SOURCE_LIST = {
    "foreignSource": [FOREIGN_SOURCE],
    "totalCount": 1,
    "count": 1,
}

# ---------------------------------------------------------------------------
# SNMP Configuration
# ---------------------------------------------------------------------------

SNMP_CONFIG = {
    "version": "v2c",
    "port": 161,
    "community": "public",
    "timeout": 1800,
    "retries": 1,
    "maxVarsPerPdu": 10,
    "maxRepetitions": 2,
    "maxRequestSize": 65535,
    "proxyHost": None,
    "securityName": None,
    "location": "Default",
}

# ---------------------------------------------------------------------------
# Group
# ---------------------------------------------------------------------------

GROUP = {
    "name": "network-ops",
    "comments": "Network operations team",
    "users": ["admin", "jsmith"],
    "categories": ["Production"],
}

GROUP_LIST = {
    "group": [GROUP],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

GROUP_USER_LIST = {"users": ["admin", "jsmith"]}
GROUP_CATEGORY_LIST = {"categories": ["Production", "Routers"]}

# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

USER = {
    "user-id": "jsmith",
    "full-name": "Jane Smith",
    "user-comments": "Senior Network Engineer",
    "email": "jsmith@example.com",
    "password": None,
    "password-salt": True,
    "duty-schedule": ["MoTuWeThFrSaSu800-2300"],
    "roles": ["ROLE_USER"],
}

USER_LIST = {
    "user": [USER],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------

CATEGORY = {
    "id": 2,
    "name": "Production",
    "authorizedGroups": ["network-ops"],
}

CATEGORY_LIST = {
    "category": [CATEGORY],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Scheduled Outage
# ---------------------------------------------------------------------------

SCHED_OUTAGE = {
    "name": "Weekend-Maintenance",
    "type": "weekly",
    "time": [
        {"day": "saturday", "begins": "00:00:00", "ends": "23:59:59"},
        {"day": "sunday",   "begins": "00:00:00", "ends": "23:59:59"},
    ],
    "node": [{"id": 1}, {"id": 2}],
    "interface": [{"address": "192.168.0.1"}],
}

SCHED_OUTAGE_LIST = {"scheduleOutage": [SCHED_OUTAGE]}

# ---------------------------------------------------------------------------
# KSC Report
# ---------------------------------------------------------------------------

KSC_REPORT = {
    "id": 1,
    "label": "Core Bandwidth Report",
    "show_timespan_button": True,
    "show_graphtype_button": False,
    "graphs_per_line": 2,
    "graphs": [
        {
            "title": "Core Switch Bandwidth",
            "resourceId": "node[1].interfaceSnmp[eth0-04013f75f101]",
            "timespan": "7_day",
            "graphtype": "mib2.bits",
        }
    ],
}

KSC_REPORT_LIST = {
    "kscReport": [{"id": 1, "label": "Core Bandwidth Report"}],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------

RESOURCE = {
    "id": "node[1].interfaceSnmp[eth0-04013f75f101]",
    "label": "eth0 (04:01:3f:75:f1:01)",
    "name": "eth0-04013f75f101",
    "typeLabel": "SNMP Interface Data",
    "parentId": "node[1]",
    "stringPropertyAttributes": {"ifName": "eth0", "ifAlias": "uplink-to-core"},
    "externalValueAttributes": {},
    "rrdGraphAttributes": {
        "ifInOctets": {
            "name": "ifInOctets",
            "relativePath": "snmp/1/eth0-04013f75f101",
            "rrdFile": "ifInOctets.jrb",
        }
    },
    "children": {"resource": []},
}

RESOURCE_TREE = {"resource": RESOURCE}

# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

MEASUREMENTS = {
    "start": 1425580938256,
    "end": 1425588138256,
    "step": 300000,
    "timestamps": [1425581100000, 1425581400000, 1425581700000],
    "labels": ["ifInOctets"],
    "columns": [{"values": [139948.5, 199006.3, 187234.8]}],
    "metadata": {
        "resources": [
            {
                "id": "node[1].interfaceSnmp[eth0-04013f75f101]",
                "label": "eth0 (04:01:3f:75:f1:01)",
            }
        ],
        "nodes": [{"id": 1, "label": "router01.example.com"}],
    },
}

# ---------------------------------------------------------------------------
# Heatmap
# ---------------------------------------------------------------------------

HEATMAP_RESPONSE = {
    "heatmapEntry": [
        {
            "id": 2,
            "label": "Production",
            "nodesTotal": 15,
            "nodesWithOutages": 2,
            "nodesWithAlarms": 5,
            "maximumSeverity": "MAJOR",
        }
    ]
}

# ---------------------------------------------------------------------------
# Map
# ---------------------------------------------------------------------------

MAP = {
    "id": 1,
    "name": "Core Network",
    "mapWidth": 1024,
    "mapHeight": 768,
    "accessMode": "RW",
    "owner": "admin",
    "lastModifiedTime": "2024-05-01T10:00:00.000+0000",
    "createTime": "2024-01-01T08:00:00.000+0000",
}

MAP_LIST = {"map": [MAP], "totalCount": 1, "count": 1, "offset": 0}

MAP_ELEMENTS = {
    "mapElement": [
        {
            "id": 1001,
            "mapId": 1,
            "elementId": 1,
            "type": "N",
            "label": "router01.example.com",
            "x": 200,
            "y": 150,
            "severity": "MAJOR",
        }
    ]
}

# ---------------------------------------------------------------------------
# Graph Container (Topology)
# ---------------------------------------------------------------------------

GRAPH_CONTAINER = {
    "id": "nodes",
    "label": "Nodes",
    "graphs": [
        {
            "namespace": "nodes",
            "description": "The default OpenNMS node graph",
            "preferredLayout": "Grid Layout",
            "focus": {"type": "SELECTION", "vertices": []},
        }
    ],
}

GRAPH_CONTAINER_LIST = {"graphContainer": [GRAPH_CONTAINER]}

GRAPH = GRAPH_CONTAINER["graphs"][0]

GRAPH_SUGGESTIONS = {
    "suggestion": [
        {"label": "router01.example.com", "context": "nodes"}
    ]
}

GRAPH_SEARCH_RESULTS = {
    "searchResult": [
        {"id": "nodes:1", "label": "router01.example.com", "namespace": "nodes"}
    ]
}

# ---------------------------------------------------------------------------
# Flows
# ---------------------------------------------------------------------------

FLOW_EXPORTER = {
    "node": {
        "id": 1,
        "foreignSource": "Routers",
        "foreignId": "router01",
        "label": "router01.example.com",
        "location": "Default",
    },
    "snmpInterface": {
        "index": 6,
        "name": "GigabitEthernet0/0",
        "speed": 1000000000,
    },
}

FLOW_EXPORTER_LIST = {"exporters": [FLOW_EXPORTER]}

FLOW_APPLICATIONS = {
    "start": 1425580938256,
    "end": 1425588138256,
    "applications": [
        {"application": "HTTP",  "bytesIn": 1048576, "bytesOut": 204800},
        {"application": "HTTPS", "bytesIn": 5242880, "bytesOut": 1048576},
    ],
}

FLOW_APPLICATIONS_ENUMERATE = {"label": ["HTTP", "HTTPS", "SSH"]}

FLOW_SERIES = {
    "start": 1425580938256,
    "end": 1425588138256,
    "step": 300000,
    "timestamps": [1425581100000, 1425581400000],
    "columns": [
        {
            "label": "HTTP",
            "ingress": {"values": [139948.5, 199006.3]},
            "egress":  {"values": [51661.2,  64741.0]},
        }
    ],
}

FLOW_CONVERSATIONS = {
    "start": 1425580938256,
    "end": 1425588138256,
    "conversations": [
        {
            "location": "Default",
            "protocol": "TCP",
            "sourceIp": "10.0.0.1",
            "sourcePort": 45123,
            "destIp": "192.168.1.1",
            "destPort": 443,
            "bytesIn": 2097152,
            "bytesOut": 524288,
        }
    ],
}

FLOW_HOSTS = {
    "start": 1425580938256,
    "end": 1425588138256,
    "hosts": [
        {"host": "192.168.1.1", "bytesIn": 5242880, "bytesOut": 2097152},
    ],
}

# ---------------------------------------------------------------------------
# Device Configuration
# ---------------------------------------------------------------------------

DEVICE_CONFIG = {
    "id": 901,
    "ipInterfaceId": 101,
    "ipAddress": "192.168.1.1",
    "deviceName": "router01.example.com",
    "location": "Default",
    "serviceName": "DeviceConfig-default",
    "configType": "default",
    "createdTime": "2024-06-01T02:00:00.000+0000",
    "lastUpdatedTime": "2024-06-01T02:00:05.000+0000",
    "lastSucceeded": "2024-06-01T02:00:05.000+0000",
    "lastFailed": None,
    "failureReason": None,
    "isLatest": True,
    "backupStatus": "SUCCEEDED",
}

DEVICE_CONFIG_LIST = {
    "deviceConfigs": [DEVICE_CONFIG],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Situation (v2 – alarm with isSituation=True and relatedAlarms)
# ---------------------------------------------------------------------------

SITUATION = {
    **ALARM,
    "id": 99,
    "uei": "uei.opennms.org/alarms/situation",
    "severity": "CRITICAL",
    "reductionKey": "uei.opennms.org/alarms/situation::99",
    "relatedAlarms": [
        {"id": 42, "reductionKey": ALARM["reductionKey"]},
        {"id": 43, "reductionKey": "uei.opennms.org/nodes/nodeDown::2"},
    ],
    "isSituation": True,
    "affectedNodeCount": 2,
}

SITUATION_LIST = {"alarm": [SITUATION], "totalCount": 1, "count": 1, "offset": 0}

# ---------------------------------------------------------------------------
# Business Service (v2)
# ---------------------------------------------------------------------------

BUSINESS_SERVICE = {
    "id": 1001,
    "name": "Core Network Availability",
    "attributes": {"dc": "us-east-1", "tier": "critical"},
    "reduceFunction": {"type": "HighestSeverity", "properties": {}},
    "operationalStatus": "MAJOR",
    "edges": [
        {
            "id": 2001,
            "type": "IP_SERVICE",
            "reductionKeys": ["uei.opennms.org/nodes/nodeDown::1"],
            "mapFunction": {"type": "Identity", "properties": {}},
            "weight": 1,
            "operationalStatus": "MAJOR",
        }
    ],
    "parentServices": [],
    "childServices": [],
}

BUSINESS_SERVICE_LIST = {
    "business-services": [BUSINESS_SERVICE],
    "totalCount": 1,
    "count": 1,
    "offset": 0,
}

# ---------------------------------------------------------------------------
# Metadata (v2) – returned as a bare list
# ---------------------------------------------------------------------------

METADATA_ENTRY = {
    "context": "X-OpenNMS-System",
    "key": "managedBy",
    "value": "ansible-tower",
}

METADATA_LIST = [
    METADATA_ENTRY,
    {"context": "X-OpenNMS-System", "key": "environment", "value": "production"},
    {"context": "requisition",       "key": "category",    "value": "Routers"},
]

# ---------------------------------------------------------------------------
# Server Info
# ---------------------------------------------------------------------------

SERVER_INFO = {
    "displayVersion": "Horizon 35.0.0",
    "version": "35.0.0",
    "packageName": "opennms",
    "packageDescription": "OpenNMS",
    "ticketerConfig": {"plugin": None, "enabled": False},
    "datetimeformatConfig": {
        "zoneId": "America/New_York",
        "datetimeformat": "yyyy-MM-dd'T'HH:mm:ss.SSSZ",
    },
    "services": {
        "OpenNMS:Name=Pollerd":  "running",
        "OpenNMS:Name=Collectd": "running",
        "OpenNMS:Name=Eventd":   "running",
        "OpenNMS:Name=Alarmd":   "running",
    },
}
