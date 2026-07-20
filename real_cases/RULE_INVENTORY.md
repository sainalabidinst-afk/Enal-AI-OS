# RULE INVENTORY
# Network Engineer Analyzer Rules
# Total: 47 rules

## MikroTik Rules Only (40 rules)

### Routing Domain (6 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| RT-01 | Route without gateway | WARNING | Static route missing gateway configuration |
| RT-02 | Default route missing | WARNING | No default route configured for internet access |
| RT-03 | Overlapping networks | WARNING | IP networks overlap in addressing |
| RT-04 | Duplicate IP addresses | CRITICAL | Same IP configured on multiple interfaces |
| RT-05 | Missing NTP | INFO | NTP service not configured for time sync |
| RT-06 | Missing loopback | SUGGESTION | No loopback interface defined |

### Firewall Domain (9 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| FW-01 | Missing input chain | CRITICAL | No firewall input chain rules found |
| FW-02 | Missing forward chain | CRITICAL | Forward chain missing when NAT configured |
| FW-03 | Missing ICMP accept | INFO | ICMP not explicitly allowed in firewall |
| FW-04 | No stateful inspection | WARNING | Missing connection-state firewall rules |
| FW-05 | Missing connection tracking | WARNING | No connection tracking rules |
| FW-06 | Firewall rule order | INFO | Rule order may allow unwanted traffic |
| FW-07 | Unrestricted winbox | CRITICAL | Winbox access open to 0.0.0.0/0 |
| FW-08 | Unrestricted SSH | WARNING | SSH access open to 0.0.0.0/0 |
| FW-09 | Unrestricted WWW/API | WARNING | Web/API access open to 0.0.0.0/0 |

### NAT Domain (3 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| NAT-01 | Missing masquerade | WARNING | No masquerade rule for internet access |
| NAT-02 | Duplicate NAT rules | WARNING | Multiple NAT rules may cause conflicts |
| NAT-03 | Masquerade on LAN | WARNING | Masquerade incorrectly on LAN interface |

### VPN Domain (2 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| VPN-01 | PPP without encryption | CRITICAL | PPP connection unencrypted |
| VPN-02 | Hotspot profile unsafe | WARNING | Hotspot using default profile |

### QoS Domain (4 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| QoS-01 | Missing FastTrack | SUGGESTION | FastTrack not enabled for performance |
| QoS-02 | Queue without limit | WARNING | Queue missing max-limit |
| QoS-03 | Queue duplicate target | WARNING | Duplicate queue targets |
| QoS-04 | MTU mismatch | SUGGESTION | No MTU configuration found |

### Wireless Domain (1 rule)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| WL-01 | Wireless default security | CRITICAL | Wireless using default security profile |

### Services Domain (4 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| SVC-01 | Open DNS | WARNING | DNS allows remote requests |
| SVC-02 | DNS without upstream | WARNING | No upstream DNS servers |
| SVC-03 | DHCP pool exhaustion | WARNING | DHCP server missing address pool |
| SVC-04 | Hotspot without profile | WARNING | Hotspot missing profile |

### Security Domain (14 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| SEC-01 | Default password | CRITICAL | Weak/default password detected |
| SEC-02 | Password in comment | WARNING | Password exposed in comment field |
| SEC-03 | Unencrypted protocols | CRITICAL | Telnet or HTTP enabled |
| SEC-04 | High-risk ports open | CRITICAL | Dangerous ports open to world |
| SEC-05 | Expired certificate | CRITICAL | Certificate marked expired |
| SEC-06 | RADIUS no backup | WARNING | RADIUS without backup server |
| SEC-07 | User without password | CRITICAL | User missing password |
| SEC-08 | Service unrestricted | WARNING | IP service open to all |
| SEC-09 | Management from anywhere | CRITICAL | Management service unrestricted |
| SEC-10 | Missing backup | WARNING | No backup configuration |

### Switching Domain (1 rule)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| SW-01 | Unused interfaces | INFO | Enabled interfaces with no IP |

### High Availability Domain (2 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| HA-01 | Bridge without STP | SUGGESTION | Bridge missing protocol mode |
| HA-02 | Bridge loop risk | WARNING | Bridge with >2 ports no STP |
| HA-03 | HSRP configured | INFO | Cisco HSRP detected |
| HA-04 | Fortinet HA | INFO | Fortinet HA cluster detected |

### Vendor-Agnostic VPN (2 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| VPN-01 | PPP without encryption | CRITICAL | PPP connection unencrypted |
| VPN-02 | Hotspot profile unsafe | WARNING | Hotspot using default profile |
| VPN-03 | Cisco IPSec | INFO | Cisco IPSec VPN detected |
| VPN-04 | Fortinet IPSec | INFO | Fortinet IPSec VPN detected |

### Vendor-Agnostic Wireless (3 rules)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| WL-01 | Wireless default security | CRITICAL | Wireless using default security profile |
| WL-02 | WPA not WPA2/3 | WARNING | Wireless using WPA (not WPA2/3) |
| WL-03 | WEP enabled | CRITICAL | WEP encryption enabled |

### Vendor-Agnostic Security (1 rule)
| Rule ID | Title | Severity | Description |
|---------|-------|----------|-------------|
| SEC-01 | Telnet enabled (Cisco) | CRITICAL | Telnet enabled in Cisco config |

### Severity Summary
| Severity | Count |
|----------|-------|
| CRITICAL | 22 |
| WARNING | 13 |
| INFO | 3 |
| SUGGESTION | 2 |