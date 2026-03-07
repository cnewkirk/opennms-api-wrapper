"""TypedDict schemas for OpenNMS API request payloads.

These types describe the ``dict`` arguments accepted by write methods on
:class:`~opennms_api_wrapper.OpenNMS`.  All fields are ``total=False``
(every field is optional at the Python level); fields marked *Required*
in the descriptions must be included or the server will return a 400.

Plain dicts are accepted everywhere a TypedDict is annotated — the types
exist purely for documentation and static type checking.

Example usage::

    from opennms_api_wrapper.types import SnmpConfig, RequisitionNode

    client.set_snmp_config("10.0.0.1", SnmpConfig(version="v2c", community="public"))

    node: RequisitionNode = {
        "foreign-id": "router01",
        "node-label": "router01.example.com",
        "interface": [{"ip-addr": "10.0.0.1", "snmp-primary": "P", "status": 1}],
    }
    client.create_requisition_node("Routers", node)
"""

from typing import Any, Dict, List, TypedDict

# ---------------------------------------------------------------------------
# Node API  (keys are camelCase)
# ---------------------------------------------------------------------------


class Node(TypedDict, total=False):
    """Node payload for :meth:`~opennms_api_wrapper.OpenNMS.create_node` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_node`.

    Attributes:
        label: *Required for create.* Human-readable node display name.
        type: Node type.  ``"A"`` (active) is the standard value.
        foreignSource: Requisition / foreign source name.
        foreignId: Unique ID within the foreign source.
        location: Monitoring location name.  Defaults to ``"Default"``.
        sysName: SNMP sysName.
        sysDescription: SNMP sysDescr.
        sysContact: SNMP sysContact.
        sysLocation: SNMP sysLocation.
    """

    label: str
    type: str
    foreignSource: str
    foreignId: str
    location: str
    sysName: str
    sysDescription: str
    sysContact: str
    sysLocation: str


class NodeIpInterface(TypedDict, total=False):
    """IP interface payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_node_ip_interface` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_node_ip_interface`.

    Attributes:
        ipAddress: *Required for create.* IP address of the interface.
        isManaged: Management status.  ``"M"`` managed, ``"U"`` unmanaged,
            ``"D"`` deleted.  Defaults to ``"M"``.
        snmpPrimary: SNMP primary flag.  ``"P"`` primary, ``"S"`` secondary,
            ``"N"`` not eligible.  Defaults to ``"N"``.
        hostName: Reverse-DNS hostname for this interface.
    """

    ipAddress: str
    isManaged: str
    snmpPrimary: str
    hostName: str


class NodeSnmpInterface(TypedDict, total=False):
    """SNMP interface payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_node_snmp_interface` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_node_snmp_interface`.

    Attributes:
        ifIndex: *Required for create.* SNMP ifIndex.
        ifName: Interface name, e.g. ``"GigabitEthernet0/0"``.
        ifDescr: Interface description from SNMP ifDescr.
        ifAlias: Interface alias from SNMP ifAlias.
        ifType: SNMP ifType integer (6 = ethernetCsmacd).
        collect: Collection flag.  ``"C"`` collect, ``"N"`` do not collect.
        poll: Poll flag.  ``"P"`` poll, ``"N"`` do not poll.
    """

    ifIndex: int
    ifName: str
    ifDescr: str
    ifAlias: str
    ifType: int
    collect: str
    poll: str


class NodeAssetRecord(TypedDict, total=False):
    """Asset record payload for
    :meth:`~opennms_api_wrapper.OpenNMS.update_node_asset_record`.

    All fields are optional.  Pass only the fields you want to change.

    Attributes:
        category: Asset category, e.g. ``"Routers"``.
        manufacturer: Hardware manufacturer.
        vendor: Vendor name.
        modelNumber: Model number.
        serialNumber: Serial number.
        description: Free-text description.
        operatingSystem: Operating system name and version.
        rack: Rack identifier.
        building: Building identifier.
        floor: Floor identifier.
        room: Room identifier.
        country: Country code.
    """

    category: str
    manufacturer: str
    vendor: str
    modelNumber: str
    serialNumber: str
    description: str
    operatingSystem: str
    rack: str
    building: str
    floor: str
    room: str
    country: str


class HardwareEntity(TypedDict, total=False):
    """Hardware inventory entity payload for
    :meth:`~opennms_api_wrapper.OpenNMS.add_node_hardware_inventory` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_node_hardware_entity`.

    Attributes:
        entityPhysicalIndex: *Required for create.* ENTITY-MIB
            entPhysicalIndex.
        entPhysicalDescr: Physical description.
        entPhysicalClass: Physical class integer (e.g. 3 = chassis).
        entPhysicalName: Physical name.
        entPhysicalSerialNum: Serial number.
        entPhysicalMfgName: Manufacturer name.
        entPhysicalModelName: Model name.
        entPhysicalIsFRU: Whether this entity is a field-replaceable unit.
        children: Child hardware entities.
    """

    entityPhysicalIndex: int
    entPhysicalDescr: str
    entPhysicalClass: int
    entPhysicalName: str
    entPhysicalSerialNum: str
    entPhysicalMfgName: str
    entPhysicalModelName: str
    entPhysicalIsFRU: bool
    children: List[dict]


# ---------------------------------------------------------------------------
# Requisition / Provisioning
# Most keys use hyphens or the reserved word "class" — functional syntax.
# ---------------------------------------------------------------------------

ForeignSourceDetector = TypedDict(
    "ForeignSourceDetector",
    {
        "name": str,        # Required. Detector display name, e.g. "ICMP".
        "class": str,       # Required. Fully-qualified Java detector class.
        "parameter": list,  # list[dict] with {"key": str, "value": str}.
    },
    total=False,
)
ForeignSourceDetector.__doc__ = """Provisioning detector within a
:class:`ForeignSource`.

Keys:
    name (str): *Required.* Detector display name, e.g. ``"ICMP"``.
    class (str): *Required.* Fully-qualified Java detector class name,
        e.g. ``"org.opennms.netmgt.provision.detector.icmp.IcmpDetector"``.
    parameter (list[dict]): Detector parameters as
        ``[{"key": str, "value": str}]``.
"""

ForeignSourcePolicy = TypedDict(
    "ForeignSourcePolicy",
    {
        "name": str,        # Required. Policy display name.
        "class": str,       # Required. Fully-qualified Java policy class.
        "parameter": list,  # list[dict] with {"key": str, "value": str}.
    },
    total=False,
)
ForeignSourcePolicy.__doc__ = """Provisioning policy within a
:class:`ForeignSource`.

Keys:
    name (str): *Required.* Policy display name.
    class (str): *Required.* Fully-qualified Java policy class name,
        e.g. ``"org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy"``.
    parameter (list[dict]): Policy parameters as
        ``[{"key": str, "value": str}]``.
"""

ForeignSource = TypedDict(
    "ForeignSource",
    {
        "name": str,                            # Required. Foreign source name.
        "scan-interval": str,                   # Rescan interval, e.g. "1d", "1w".
        "detectors": List[ForeignSourceDetector],
        "policies": List[ForeignSourcePolicy],
    },
    total=False,
)
ForeignSource.__doc__ = """Foreign source definition for
:meth:`~opennms_api_wrapper.OpenNMS.create_foreign_source` and
:meth:`~opennms_api_wrapper.OpenNMS.update_foreign_source`.

Keys:
    name (str): *Required.* Foreign source name.
    scan-interval (str): Rescan interval in OpenNMS duration format,
        e.g. ``"1d"`` (daily), ``"1w"`` (weekly), ``"-1"`` (no rescan).
    detectors (list[ForeignSourceDetector]): Provisioning detectors.
    policies (list[ForeignSourcePolicy]): Provisioning policies.
"""

RequisitionService = TypedDict(
    "RequisitionService",
    {
        "service-name": str,  # e.g. "ICMP", "SNMP", "HTTP"
    },
    total=False,
)
RequisitionService.__doc__ = """Monitored-service entry within a
:class:`RequisitionInterface`.

Keys:
    service-name (str): Service name matching a provisioning detector,
        e.g. ``"ICMP"``, ``"SNMP"``, ``"HTTP"``.
"""

RequisitionInterface = TypedDict(
    "RequisitionInterface",
    {
        "ip-addr": str,                              # Required. IP address.
        "snmp-primary": str,                         # "P" | "S" | "N"
        "status": int,                               # 1 = managed, 3 = unmanaged
        "monitored-service": List[RequisitionService],
    },
    total=False,
)
RequisitionInterface.__doc__ = """IP interface entry within a
:class:`RequisitionNode`.

Keys:
    ip-addr (str): *Required.* IP address of the interface.
    snmp-primary (str): SNMP primary flag — ``"P"`` (primary), ``"S"``
        (secondary), ``"N"`` (not eligible).  Default ``"N"``.
    status (int): Management status — ``1`` managed, ``3`` unmanaged.
    monitored-service (list[RequisitionService]): Services to monitor.
"""

RequisitionAsset = TypedDict(
    "RequisitionAsset",
    {
        "name": str,
        "value": str,
    },
    total=False,
)
RequisitionAsset.__doc__ = """Asset record entry within a :class:`RequisitionNode`.

Keys:
    name (str): Asset field name, e.g. ``"manufacturer"``,
        ``"serialNumber"``, ``"description"``.
    value (str): Asset field value.
"""

RequisitionNode = TypedDict(
    "RequisitionNode",
    {
        "foreign-id": str,                          # Required. Unique node ID.
        "node-label": str,                          # Required. Display name.
        "location": str,
        "interface": List[RequisitionInterface],
        "category": List[dict],                     # [{"name": str}]
        "asset": List[RequisitionAsset],
        "meta-data": List[dict],                    # [{"context", "key", "value"}]
    },
    total=False,
)
RequisitionNode.__doc__ = """Node payload for
:meth:`~opennms_api_wrapper.OpenNMS.create_requisition_node`.

Keys:
    foreign-id (str): *Required.* Unique node identifier within the
        requisition.  Must be stable across imports.
    node-label (str): *Required.* Human-readable node display name.
    location (str): Monitoring location name.  Defaults to ``"Default"``.
    interface (list[RequisitionInterface]): IP interfaces to provision.
    category (list[dict]): Surveillance categories,
        e.g. ``[{"name": "Production"}]``.
    asset (list[RequisitionAsset]): Asset record fields.
    meta-data (list[dict]): Metadata entries with ``"context"``,
        ``"key"``, and ``"value"`` keys.
"""

Requisition = TypedDict(
    "Requisition",
    {
        "foreign-source": str,              # Required. Requisition name.
        "node": List[RequisitionNode],
    },
    total=False,
)
Requisition.__doc__ = """Requisition payload for
:meth:`~opennms_api_wrapper.OpenNMS.create_requisition`.

Keys:
    foreign-source (str): *Required.* Requisition (foreign source) name.
    node (list[RequisitionNode]): Nodes to include in the requisition.
"""

# ---------------------------------------------------------------------------
# Organization  (Group uses valid identifiers; User has hyphens)
# ---------------------------------------------------------------------------


class Group(TypedDict, total=False):
    """Group payload for :meth:`~opennms_api_wrapper.OpenNMS.create_group`
    and :meth:`~opennms_api_wrapper.OpenNMS.update_group`.

    Attributes:
        name: *Required for create.* Unique group name.
        comments: Free-text description of the group.
    """

    name: str
    comments: str


User = TypedDict(
    "User",
    {
        "user-id": str,           # Required. Unique username.
        "full-name": str,
        "user-comments": str,
        "email": str,
        "password": str,
        "duty-schedule": List[str],  # e.g. ["MoTuWeThFrSaSu800-2300"]
    },
    total=False,
)
User.__doc__ = """User payload for :meth:`~opennms_api_wrapper.OpenNMS.create_user`
and :meth:`~opennms_api_wrapper.OpenNMS.update_user`.

Keys:
    user-id (str): *Required for create.* Unique username.
    full-name (str): Display name.
    user-comments (str): Free-text comment.
    email (str): Email address.
    password (str): Plain-text password (pass ``hash_password=True`` to
        have OpenNMS hash it on receipt).
    duty-schedule (list[str]): Duty schedule strings,
        e.g. ``["MoTuWeThFrSaSu800-2300"]``.
"""


class Category(TypedDict, total=False):
    """Category payload for :meth:`~opennms_api_wrapper.OpenNMS.create_category`
    and :meth:`~opennms_api_wrapper.OpenNMS.update_category`.

    Attributes:
        name: *Required for create.* Unique category name.
        authorizedGroups: Groups authorized to see this category.
    """

    name: str
    authorizedGroups: List[str]


# ---------------------------------------------------------------------------
# Scheduled Outages
# ---------------------------------------------------------------------------


class SchedOutageTime(TypedDict, total=False):
    """Time window entry within a :class:`SchedOutage`.

    Attributes:
        day: Day specifier.  For ``"weekly"`` outages: lowercase weekday
            name (e.g. ``"saturday"``).  For ``"monthly"``: integer
            day-of-month.
        begins: Start time ``"HH:MM:SS"`` (daily/weekly/monthly) or
            full datetime ``"DD-Mon-YYYY HH:MM:SS"`` (specific).
        ends: End time in the same format as *begins*.
    """

    day: str
    begins: str
    ends: str


class SchedOutage(TypedDict, total=False):
    """Scheduled outage payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_sched_outage`.

    Attributes:
        name: *Required.* Unique scheduled outage name.
        type: Outage type: ``"weekly"``, ``"monthly"``, ``"specific"``,
            or ``"daily"``.
        time: List of time windows during which the outage applies.
        node: Nodes to suppress during the outage,
            e.g. ``[{"id": 1}, {"id": 2}]``.
        interface: IP interfaces to suppress,
            e.g. ``[{"address": "192.168.0.1"}]``.
    """

    name: str
    type: str
    time: List[SchedOutageTime]
    node: List[dict]
    interface: List[dict]


# ---------------------------------------------------------------------------
# KSC Reports
# ---------------------------------------------------------------------------


class KscGraph(TypedDict, total=False):
    """Graph entry within a :class:`KscReport`.

    Attributes:
        title: Graph title.
        resourceId: OpenNMS resource ID,
            e.g. ``"node[1].interfaceSnmp[eth0-04013f75f101]"``.
        timespan: Timespan identifier, e.g. ``"7_day"``, ``"1_month"``.
        graphtype: Graph type (RRD graph definition name),
            e.g. ``"mib2.bits"``.
        graphIndex: Position of this graph within the report.
    """

    title: str
    resourceId: str
    timespan: str
    graphtype: str
    graphIndex: int


class KscReport(TypedDict, total=False):
    """KSC report payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_ksc_report` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_ksc_report`.

    Attributes:
        id: Report ID (set to ``0`` for new reports).
        label: *Required.* Report display name.
        show_timespan_button: Show the timespan selection button.
        show_graphtype_button: Show the graph type selection button.
        graphs_per_line: Number of graphs per row.
        graphs: List of graph definitions.
    """

    id: int
    label: str
    show_timespan_button: bool
    show_graphtype_button: bool
    graphs_per_line: int
    graphs: List[KscGraph]


# ---------------------------------------------------------------------------
# Maps
# ---------------------------------------------------------------------------


class Map(TypedDict, total=False):
    """Map payload for :meth:`~opennms_api_wrapper.OpenNMS.create_map`
    and :meth:`~opennms_api_wrapper.OpenNMS.update_map`.

    Attributes:
        name: *Required for create.* Unique map name.
        mapWidth: Map canvas width in pixels.
        mapHeight: Map canvas height in pixels.
        accessMode: Access control mode: ``"RW"`` (read-write) or
            ``"RO"`` (read-only).
        owner: Username of the map owner.
    """

    name: str
    mapWidth: int
    mapHeight: int
    accessMode: str
    owner: str


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


class Event(TypedDict, total=False):
    """Event payload for :meth:`~opennms_api_wrapper.OpenNMS.create_event`.

    Attributes:
        uei: *Required.* Event UEI,
            e.g. ``"uei.opennms.org/internal/test"``.
        source: Event source identifier (name of the generating script
            or application).
        severity: Event severity: ``"Indeterminate"``, ``"Cleared"``,
            ``"Normal"``, ``"Warning"``, ``"Minor"``, ``"Major"``,
            ``"Critical"``.
        nodeId: Database ID of the associated node.
        interface: IP address of the associated interface.
        service: Service name of the associated service.
        ifIndex: SNMP ifIndex of the associated interface.
        description: HTML-formatted description.
        logMsg: Short log message text.
        operInstruct: Operator instructions.
        parms: Event parameters as
            ``{"parm": [{"parmName": str, "value": {"content": str}}]}``.
    """

    uei: str
    source: str
    severity: str
    nodeId: int
    interface: str
    service: str
    ifIndex: int
    description: str
    logMsg: str
    operInstruct: str
    parms: Dict[str, Any]


class EventConfLogmsg(TypedDict, total=False):
    """Log message entry within an :class:`EventConfEvent`.

    Attributes:
        content: Log message text.
        dest: Destination: ``"logndisplay"``, ``"logonly"``,
            ``"displayonly"``, ``"suppress"``, ``"donotpersist"``.
    """

    content: str
    dest: str


class EventConfEvent(TypedDict, total=False):
    """Event definition payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_eventconf_event` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_eventconf_event`.

    Attributes:
        uei: *Required.* Event UEI.
        label: Human-readable label.
        descr: HTML-formatted description.
        logmsg: Log message configuration.
        severity: Event severity: ``"Indeterminate"``, ``"Cleared"``,
            ``"Normal"``, ``"Warning"``, ``"Minor"``, ``"Major"``,
            ``"Critical"``.
    """

    uei: str
    label: str
    descr: str
    logmsg: EventConfLogmsg
    severity: str


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------


class MeasurementSource(TypedDict, total=False):
    """Data source entry within a :class:`MeasurementsQuery`.

    Attributes:
        resourceId: *Required.* OpenNMS resource ID,
            e.g. ``"node[1].interfaceSnmp[eth0-04013f75f101]"``.
        attribute: *Required.* RRD attribute name, e.g. ``"ifInOctets"``.
        label: *Required.* Column label used in expressions and output.
        aggregation: Consolidation function: ``"AVERAGE"`` (default),
            ``"MIN"``, ``"MAX"``, ``"LAST"``.
        transient: When ``True``, exclude this source from the response
            (used only for intermediate expression values).
    """

    resourceId: str
    attribute: str
    label: str
    aggregation: str
    transient: bool


class MeasurementExpression(TypedDict, total=False):
    """JEXL expression entry within a :class:`MeasurementsQuery`.

    Attributes:
        label: *Required.* Output column label.
        value: *Required.* JEXL expression referencing source labels,
            e.g. ``"ifInOctets * 8"``.
        transient: When ``True``, exclude from response output.
    """

    label: str
    value: str
    transient: bool


class MeasurementsQuery(TypedDict, total=False):
    """Query payload for
    :meth:`~opennms_api_wrapper.OpenNMS.get_measurements_multi`.

    Attributes:
        start: Query start time as a Unix millisecond epoch timestamp.
        end: Query end time as a Unix millisecond epoch timestamp.
        step: Desired step size in milliseconds.
        maxrows: Maximum number of time-step rows to return.
        source: List of data sources to fetch.
        expression: List of JEXL expressions computed from source labels.
    """

    start: int
    end: int
    step: int
    maxrows: int
    source: List[MeasurementSource]
    expression: List[MeasurementExpression]


# ---------------------------------------------------------------------------
# Business Services (v2)
# ---------------------------------------------------------------------------


class BsFunction(TypedDict, total=False):
    """Map or reduce function reference within a Business Service definition.

    Attributes:
        type: Function name, e.g. ``"Identity"``, ``"Increase"``,
            ``"HighestSeverity"``, ``"Threshold"``.
        properties: Function-specific properties dict,
            e.g. ``{"threshold": "0.5"}`` for ``Threshold``.
    """

    type: str
    properties: Dict[str, str]


class BusinessService(TypedDict, total=False):
    """Business service payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_business_service` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_business_service`.

    Attributes:
        name: *Required.* Unique business service name.
        attributes: Arbitrary key/value metadata dict.
        reduceFunction: Reduce function configuration.
    """

    name: str
    attributes: Dict[str, str]
    reduceFunction: BsFunction


class BsIpServiceEdge(TypedDict, total=False):
    """IP-service edge payload for
    :meth:`~opennms_api_wrapper.OpenNMS.add_ip_service_edge`.

    Attributes:
        ipServiceId: *Required.* Database ID of the monitored IP service.
        mapFunction: Map function configuration.
        weight: Edge weight (higher weight = greater influence).
    """

    ipServiceId: int
    mapFunction: BsFunction
    weight: int


class BsReductionKeyEdge(TypedDict, total=False):
    """Reduction-key edge payload for
    :meth:`~opennms_api_wrapper.OpenNMS.add_reduction_key_edge`.

    Attributes:
        reductionKey: *Required.* Alarm reduction key to monitor.
        mapFunction: Map function configuration.
        weight: Edge weight.
    """

    reductionKey: str
    mapFunction: BsFunction
    weight: int


class BsChildEdge(TypedDict, total=False):
    """Child-service edge payload for
    :meth:`~opennms_api_wrapper.OpenNMS.add_child_edge`.

    Attributes:
        childId: *Required.* Database ID of the child business service.
        mapFunction: Map function configuration.
        weight: Edge weight.
    """

    childId: int
    mapFunction: BsFunction
    weight: int


# ---------------------------------------------------------------------------
# Flow Classifications
# ---------------------------------------------------------------------------


class ClassificationRule(TypedDict, total=False):
    """Classification rule payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_classification_rule` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_classification_rule`.

    Attributes:
        name: *Required.* Application name this rule identifies.
        dstPort: Destination port or range, e.g. ``"443"`` or ``"8080-8090"``.
        srcPort: Source port or range.
        dstAddress: Destination IP address or CIDR, e.g. ``"10.0.0.0/8"``.
        srcAddress: Source IP address or CIDR.
        protocol: Protocol: ``"tcp"``, ``"udp"``, ``"icmp"``.
        exporterFilter: FIQL filter selecting which exporters this rule
            applies to.
        groupId: ID of the classification group this rule belongs to.
        position: Sort position within the group.
    """

    name: str
    dstPort: str
    srcPort: str
    dstAddress: str
    srcAddress: str
    protocol: str
    exporterFilter: str
    groupId: int
    position: int


class ClassificationGroup(TypedDict, total=False):
    """Classification group payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_classification_group` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_classification_group`.

    Attributes:
        name: *Required.* Unique group name.
        enabled: Whether this group's rules are active.
    """

    name: str
    enabled: bool


class ClassifyRequest(TypedDict, total=False):
    """Flow classification request for
    :meth:`~opennms_api_wrapper.OpenNMS.classify`.

    Attributes:
        srcAddress: Source IP address.
        srcPort: Source port number.
        dstAddress: Destination IP address.
        dstPort: Destination port number.
        protocol: Protocol integer or name.
        exporterAddress: IP address of the flow exporter.
    """

    srcAddress: str
    srcPort: int
    dstAddress: str
    dstPort: int
    protocol: str
    exporterAddress: str


# ---------------------------------------------------------------------------
# Infrastructure
# ---------------------------------------------------------------------------


class Credential(TypedDict, total=False):
    """Secure Credentials Vault payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_credential` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_credential`.

    Attributes:
        alias: *Required for create.* Unique credential alias.
        username: Credential username.
        password: Credential password.
        attributes: Additional key/value attributes dict.
    """

    alias: str
    username: str
    password: str
    attributes: Dict[str, str]


class Application(TypedDict, total=False):
    """Application payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_application`.

    Attributes:
        name: *Required.* Unique application name.
        monitoredServices: List of monitored service ID references,
            e.g. ``[{"id": 201}]``.
    """

    name: str
    monitoredServices: List[dict]


class UserDefinedLink(TypedDict, total=False):
    """User-defined link payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_user_defined_link`.

    Attributes:
        nodeIdA: *Required.* Database ID of the A-side node.
        nodeIdZ: *Required.* Database ID of the Z-side node.
        componentLabelA: Label for the A-side component (e.g. interface name).
        componentLabelZ: Label for the Z-side component.
        linkId: Unique link identifier string.
        linkLabel: Human-readable link label.
        owner: Username of the link owner.
    """

    nodeIdA: int
    nodeIdZ: int
    componentLabelA: str
    componentLabelZ: str
    linkId: str
    linkLabel: str
    owner: str


# ---------------------------------------------------------------------------
# SNMP Configuration  (keys are camelCase)
# ---------------------------------------------------------------------------


class SnmpConfig(TypedDict, total=False):
    """SNMP configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.set_snmp_config`.

    Fields correspond to ``<definition/>`` attributes in
    ``snmp-config.xsd``.  Unset fields inherit from the OpenNMS default
    SNMP configuration.

    Attributes:
        version: SNMP version: ``"v1"``, ``"v2c"``, or ``"v3"``.
        community: Community string (v1/v2c only).
        port: UDP port.  Default ``161``.
        timeout: Timeout in milliseconds.
        retries: Retry count before giving up.
        maxVarsPerPdu: Maximum variables per GETBULK PDU.
        maxRepetitions: Maximum repetitions for GETBULK.
        maxRequestSize: Maximum PDU size in bytes.
        proxyHost: Proxy host IP for this definition.
        securityName: SNMPv3 security name (username).
        securityLevel: SNMPv3 security level —
            ``1`` noAuthNoPriv, ``2`` authNoPriv, ``3`` authPriv.
        authPassphrase: SNMPv3 authentication passphrase.
        authProtocol: SNMPv3 auth protocol: ``"MD5"`` or ``"SHA"``.
        privPassphrase: SNMPv3 privacy passphrase.
        privProtocol: SNMPv3 privacy protocol: ``"DES"``, ``"AES128"``,
            ``"AES192"``, or ``"AES256"``.
        contextName: SNMPv3 context name.
    """

    version: str
    community: str
    port: int
    timeout: int
    retries: int
    maxVarsPerPdu: int
    maxRepetitions: int
    maxRequestSize: int
    proxyHost: str
    securityName: str
    securityLevel: int
    authPassphrase: str
    authProtocol: str
    privPassphrase: str
    privProtocol: str
    contextName: str


# ---------------------------------------------------------------------------
# Monitoring Location  (keys use hyphens — functional syntax)
# ---------------------------------------------------------------------------

MonitoringLocation = TypedDict(
    "MonitoringLocation",
    {
        "location-name": str,
        "monitoring-area": str,
        "priority": int,
        "tags": List[str],
    },
    total=False,
)
MonitoringLocation.__doc__ = """Monitoring location payload for
:meth:`~opennms_api_wrapper.OpenNMS.create_monitoring_location`.

Keys:
    location-name (str): *Required.* Unique location identifier.
    monitoring-area (str): Geographic or logical area label.
    priority (int): Display sort order.
    tags (list[str]): Optional location tags.
"""


# ---------------------------------------------------------------------------
# NBI Configurations
# ---------------------------------------------------------------------------


class SnmpTrapNbiTrapSink(TypedDict, total=False):
    """SNMP trap sink payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_snmptrap_nbi_trapsink` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_snmptrap_nbi_trapsink`.

    Attributes:
        name: *Required.* Unique trap sink name.
        ipAddress: *Required.* Destination IP address.
        port: Destination UDP port.  Default ``162``.
        community: SNMP community string.  Default ``"public"``.
    """

    name: str
    ipAddress: str
    port: int
    community: str


class SnmpTrapNbiConfig(TypedDict, total=False):
    """SNMP trap NBI configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.update_snmptrap_nbi_config`.

    Attributes:
        enabled: Whether SNMP trap forwarding is enabled.
        trapsinks: List of trap sink definitions.
    """

    enabled: bool
    trapsinks: List[SnmpTrapNbiTrapSink]


class EmailNbiDestination(TypedDict, total=False):
    """Email NBI destination payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_email_nbi_destination` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_email_nbi_destination`.

    Attributes:
        name: *Required.* Unique destination name.
        firstOccurrenceOnly: When ``True``, send only on first occurrence
            of an alarm (not on re-occurrences).
        filters: List of alarm filter expressions.
    """

    name: str
    firstOccurrenceOnly: bool
    filters: List[str]


class EmailNbiConfig(TypedDict, total=False):
    """Email NBI configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.update_email_nbi_config`.

    Attributes:
        enabled: Whether email alarm forwarding is enabled.
        destinations: List of destination definitions.
    """

    enabled: bool
    destinations: List[EmailNbiDestination]


class SyslogNbiDestination(TypedDict, total=False):
    """Syslog NBI destination payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_syslog_nbi_destination` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_syslog_nbi_destination`.

    Attributes:
        name: *Required.* Unique destination name.
        host: *Required.* Destination hostname or IP address.
        port: Destination UDP/TCP port.  Default ``514``.
        firstOccurrenceOnly: When ``True``, forward only on first
            occurrence.
        filters: List of alarm filter expressions.
    """

    name: str
    host: str
    port: int
    firstOccurrenceOnly: bool
    filters: List[str]


class SyslogNbiConfig(TypedDict, total=False):
    """Syslog NBI configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.update_syslog_nbi_config`.

    Attributes:
        enabled: Whether syslog alarm forwarding is enabled.
        destinations: List of destination definitions.
    """

    enabled: bool
    destinations: List[SyslogNbiDestination]


# ---------------------------------------------------------------------------
# Javamail Configuration
# ---------------------------------------------------------------------------


class JavamailDefaultConfig(TypedDict, total=False):
    """Default Javamail configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.set_javamail_default_config`.

    Attributes:
        defaultReadConfigName: Name of the default read-mail configuration.
        defaultSendConfigName: Name of the default send-mail configuration.
        defaultEnd2endConfigName: Name of the default end-to-end
            test configuration.
    """

    defaultReadConfigName: str
    defaultSendConfigName: str
    defaultEnd2endConfigName: str


class JavamailReadmail(TypedDict, total=False):
    """Read-mail configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_javamail_readmail` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_javamail_readmail`.

    Attributes:
        name: *Required.* Unique configuration name.
        host: Mail server hostname.
        port: Mail server port (e.g. ``993`` for IMAPS).
        protocol: Mail protocol: ``"imap"``, ``"imaps"``, ``"pop3"``,
            ``"pop3s"``.
    """

    name: str
    host: str
    port: int
    protocol: str


class JavamailSendmail(TypedDict, total=False):
    """Send-mail configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_javamail_sendmail` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_javamail_sendmail`.

    Attributes:
        name: *Required.* Unique configuration name.
        host: SMTP server hostname.
        port: SMTP server port (e.g. ``25``, ``465``, ``587``).
        protocol: SMTP protocol: ``"smtp"``, ``"smtps"``.
    """

    name: str
    host: str
    port: int
    protocol: str


class JavamailEnd2End(TypedDict, total=False):
    """End-to-end mail test configuration payload for
    :meth:`~opennms_api_wrapper.OpenNMS.create_javamail_end2end` and
    :meth:`~opennms_api_wrapper.OpenNMS.update_javamail_end2end`.

    Attributes:
        name: *Required.* Unique configuration name.
        readMailConfigName: Read-mail configuration to use.
        sendMailConfigName: Send-mail configuration to use.
    """

    name: str
    readMailConfigName: str
    sendMailConfigName: str
