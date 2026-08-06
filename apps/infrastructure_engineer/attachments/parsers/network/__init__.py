from apps.infrastructure_engineer.attachments.parsers.network.aruba import ArubaParser
from apps.infrastructure_engineer.attachments.parsers.network.aruba_central import ArubaCentralParser
from apps.infrastructure_engineer.attachments.parsers.network.aruba_instant import ArubaInstantParser
from apps.infrastructure_engineer.attachments.parsers.network.cambium import CambiumParser
from apps.infrastructure_engineer.attachments.parsers.network.checkpoint import CheckPointParser
from apps.infrastructure_engineer.attachments.parsers.network.cisco import CiscoIOSParser
from apps.infrastructure_engineer.attachments.parsers.network.cisco_asa import CiscoASAParser
from apps.infrastructure_engineer.attachments.parsers.network.dell_networking import DellNetworkingParser
from apps.infrastructure_engineer.attachments.parsers.network.extreme import ExtremeNetworksParser
from apps.infrastructure_engineer.attachments.parsers.network.fortinet import FortinetParser
from apps.infrastructure_engineer.attachments.parsers.network.hpe_procurve import HPEProCurveParser
from apps.infrastructure_engineer.attachments.parsers.network.huawei import HuaweiParser
from apps.infrastructure_engineer.attachments.parsers.network.juniper import JuniperParser
from apps.infrastructure_engineer.attachments.parsers.network.meraki import MerakiParser
from apps.infrastructure_engineer.attachments.parsers.network.mikrotik import MikroTikParser
from apps.infrastructure_engineer.attachments.parsers.network.omada import OmadaParser
from apps.infrastructure_engineer.attachments.parsers.network.palo_alto import PaloAltoParser
from apps.infrastructure_engineer.attachments.parsers.network.ruckus import RuckusParser
from apps.infrastructure_engineer.attachments.parsers.network.ruijie import RuijieParser
from apps.infrastructure_engineer.attachments.parsers.network.ruijie_reyee import RuijieReyeeParser
from apps.infrastructure_engineer.attachments.parsers.network.sonicwall import SonicWallParser
from apps.infrastructure_engineer.attachments.parsers.network.sophos import SophosParser
from apps.infrastructure_engineer.attachments.parsers.network.text_config import TextConfigParser
from apps.infrastructure_engineer.attachments.parsers.network.unifi import UniFiParser
from apps.infrastructure_engineer.attachments.parsers.network.unifi_wireless import UniFiWirelessParser

__all__ = [
    "ArubaCentralParser",
    "ArubaInstantParser",
    "ArubaParser",
    "CambiumParser",
    "CheckPointParser",
    "CiscoASAParser",
    "CiscoIOSParser",
    "DellNetworkingParser",
    "ExtremeNetworksParser",
    "FortinetParser",
    "HPEProCurveParser",
    "HuaweiParser",
    "JuniperParser",
    "MerakiParser",
    "MikroTikParser",
    "OmadaParser",
    "PaloAltoParser",
    "RuijieParser",
    "RuijieReyeeParser",
    "RuckusParser",
    "SonicWallParser",
    "SophosParser",
    "TextConfigParser",
    "UniFiParser",
    "UniFiWirelessParser",
]
