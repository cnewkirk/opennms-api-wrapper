"""TypedDict schemas for OpenNMS API request payloads.

These types describe the ``dict`` arguments accepted by write methods on
:class:`~opennms_api_wrapper.OpenNMS`.  All fields are ``total=False``
(every field is optional at the Python level); fields marked *Required*
in the descriptions must be included or the server will return a 400.

Example usage::

    from opennms_api_wrapper.types import SnmpConfig, RequisitionNode

    client.set_snmp_config("10.0.0.1", SnmpConfig(version="v2c", community="public"))

    node = RequisitionNode(**{
        "foreign-id": "router01",
        "node-label": "router01.example.com",
        "interface": [{"ip-addr": "10.0.0.1", "snmp-primary": "P", "status": 1}],
    })
    client.create_requisition_node("Routers", node)
"""

from typing import List, TypedDict

# ---------------------------------------------------------------------------
# SNMP Configuration
# Keys are camelCase — class syntax works cleanly.
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
# Monitoring Location
# Keys use hyphens — functional (dict-literal) syntax required.
# ---------------------------------------------------------------------------

MonitoringLocation = TypedDict(
    "MonitoringLocation",
    {
        "location-name": str,   # Required. Unique location name.
        "monitoring-area": str, # Geographic or logical area label.
        "priority": int,        # Display sort order in the UI.
    },
    total=False,
)
MonitoringLocation.__doc__ = """Monitoring location payload for
:meth:`~opennms_api_wrapper.OpenNMS.create_monitoring_location`.

Keys:
    location-name (str): *Required.* Unique location identifier.
    monitoring-area (str): Geographic or logical area label.
    priority (int): Display sort order.
"""


# ---------------------------------------------------------------------------
# Requisition (provisioning) types
# All keys use hyphens — functional syntax throughout.
# ---------------------------------------------------------------------------

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
        "ip-addr": str,             # Required. IP address of the interface.
        "snmp-primary": str,        # "P" primary | "S" secondary | "N" not eligible
        "status": int,              # 1 = managed, 3 = not managed
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
        "name": str,   # Asset field name, e.g. "manufacturer", "serialNumber".
        "value": str,  # Asset field value.
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
        "foreign-id": str,                      # Required. Unique node ID in this requisition.
        "node-label": str,                      # Required. Display name for the node.
        "location": str,                        # Monitoring location name, e.g. "Default".
        "interface": List[RequisitionInterface],
        "category": List[dict],                 # e.g. [{"name": "Production"}]
        "asset": List[RequisitionAsset],
        "meta-data": List[dict],                # [{"context": str, "key": str, "value": str}]
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
