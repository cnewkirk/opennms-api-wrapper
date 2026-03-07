"""Main OpenNMS client class."""
from ._base import _OpenNMSBase
from ._alarms import AlarmsMixin
from ._alarm_stats import AlarmStatsMixin
from ._alarm_history import AlarmHistoryMixin
from ._events import EventsMixin
from ._nodes import NodesMixin
from ._outages import OutagesMixin
from ._notifications import NotificationsMixin
from ._acks import AcksMixin
from ._requisitions import RequisitionsMixin
from ._foreign_sources import ForeignSourcesMixin
from ._snmp_config import SnmpConfigMixin
from ._groups import GroupsMixin
from ._users import UsersMixin
from ._categories import CategoriesMixin
from ._sched_outages import SchedOutagesMixin
from ._ksc_reports import KscReportsMixin
from ._resources import ResourcesMixin
from ._measurements import MeasurementsMixin
from ._heatmap import HeatmapMixin
from ._maps import MapsMixin
from ._graphs import GraphsMixin
from ._flows import FlowsMixin
from ._device_config import DeviceConfigMixin
from ._situations import SituationsMixin
from ._business_services import BusinessServicesMixin
from ._metadata import MetadataMixin
from ._info import InfoMixin
from ._discovery import DiscoveryMixin
from ._ipinterfaces_v2 import IpInterfacesV2Mixin
from ._snmpinterfaces_v2 import SnmpInterfacesV2Mixin
from ._enlinkd import EnLinkdMixin
from ._monitoring_locations import MonitoringLocationsMixin
from ._minions import MinionsMixin
from ._ifservices import IfServicesMixin
from ._availability import AvailabilityMixin
from ._health import HealthMixin
from ._whoami import WhoamiMixin
from ._classifications import ClassificationsMixin
from ._situation_feedback import SituationFeedbackMixin
from ._user_defined_links import UserDefinedLinksMixin
from ._applications import ApplicationsMixin
from ._perspective_poller import PerspectivePollerMixin
from ._foreign_sources_config import ForeignSourcesConfigMixin
from ._requisition_names import RequisitionNamesMixin
from ._snmp_metadata import SnmpMetadataMixin
from ._provisiond import ProvisiondMixin
from ._eventconf import EventConfMixin
from ._monitoring_systems import MonitoringSystemsMixin
from ._asset_suggestions import AssetSuggestionsMixin
from ._scv import ScvMixin
from ._config_mgmt import ConfigMgmtMixin
from ._snmptrap_nbi import SnmpTrapNbiMixin
from ._email_nbi import EmailNbiMixin
from ._syslog_nbi import SyslogNbiMixin
from ._javamail_config import JavamailConfigMixin


class OpenNMS(
    _OpenNMSBase,
    InfoMixin,
    AlarmsMixin,
    AlarmStatsMixin,
    AlarmHistoryMixin,
    EventsMixin,
    NodesMixin,
    OutagesMixin,
    NotificationsMixin,
    AcksMixin,
    RequisitionsMixin,
    ForeignSourcesMixin,
    SnmpConfigMixin,
    GroupsMixin,
    UsersMixin,
    CategoriesMixin,
    SchedOutagesMixin,
    KscReportsMixin,
    ResourcesMixin,
    MeasurementsMixin,
    HeatmapMixin,
    MapsMixin,
    GraphsMixin,
    FlowsMixin,
    DeviceConfigMixin,
    SituationsMixin,
    BusinessServicesMixin,
    MetadataMixin,
    DiscoveryMixin,
    IpInterfacesV2Mixin,
    SnmpInterfacesV2Mixin,
    EnLinkdMixin,
    MonitoringLocationsMixin,
    MinionsMixin,
    IfServicesMixin,
    AvailabilityMixin,
    HealthMixin,
    WhoamiMixin,
    ClassificationsMixin,
    SituationFeedbackMixin,
    UserDefinedLinksMixin,
    ApplicationsMixin,
    PerspectivePollerMixin,
    ForeignSourcesConfigMixin,
    RequisitionNamesMixin,
    SnmpMetadataMixin,
    ProvisiondMixin,
    EventConfMixin,
    MonitoringSystemsMixin,
    AssetSuggestionsMixin,
    ScvMixin,
    ConfigMgmtMixin,
    SnmpTrapNbiMixin,
    EmailNbiMixin,
    SyslogNbiMixin,
    JavamailConfigMixin,
):
    """Thin Python wrapper for the OpenNMS REST API.

    All responses are returned as parsed Python objects (dicts/lists/ints).
    Failed HTTP requests raise ``requests.exceptions.HTTPError``.

    Usage::

        import opennms_api_wrapper as opennms

        client = opennms.OpenNMS(
            url="http://localhost:8980",
            username="admin",
            password="admin",
        )

        # Get all critical alarms
        alarms = client.get_alarms(limit=0, severity="CRITICAL")

        # Acknowledge an alarm
        client.ack_alarm(42)

        # List nodes
        nodes = client.get_nodes(limit=25)

        # Create a requisition node
        client.create_requisition_node("Servers", {
            "foreign-id": "web01",
            "node-label": "web01.example.com",
            "interface": [
                {
                    "ip-addr": "10.0.0.1",
                    "snmp-primary": "P",
                    "status": 1,
                    "monitored-service": [{"service-name": "ICMP"}, {"service-name": "HTTP"}],
                }
            ],
        })
        client.import_requisition("Servers")

    Args:
        url: Base URL of the OpenNMS instance, e.g. ``"http://opennms:8980"``.
            Do not include the ``/opennms`` context path.
        username: OpenNMS username (needs at minimum the ``rest`` role).
        password: OpenNMS password.
        verify_ssl: Whether to verify SSL certificates.  Set to ``False`` for
            self-signed certs in dev/test environments (not recommended in
            production).
        timeout: Socket timeout in seconds for all HTTP requests.
            Defaults to ``30``.  Pass ``None`` to disable.
    """

    def __init__(self, url: str, username: str, password: str,
                 verify_ssl: bool = True, timeout: int = 30):
        """Initialize the OpenNMS client."""
        super().__init__(url, username, password, verify_ssl, timeout)
