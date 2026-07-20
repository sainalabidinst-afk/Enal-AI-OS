# BENCHMARK FAILURE REPORT

## Summary
All 30 cases executed successfully. No crashes.

## Findings Discrepancy
| Metric | Actual | Expected | Notes |
|--------|--------|----------|-------|
| Total findings | 279 | - | All cases produce findings |
| Critical findings | 65 | 16 | High false positive rate |

## Key Issues Identified

### 1. Security Rules Trigger on All Vendor Configs
- Cisco configs contain "telnet disabled=no" → triggers CRITICAL
- MikroTik configs without "/user password" → triggers CRITICAL (even when config is incomplete)
- These rules work but produce higher severity than expected

### 2. Baseline Rules for Missing Configuration
Many INFO rules trigger because test configs are minimal snippets:
- Missing NTP: triggers on configs without ntp
- Missing logging: triggers on configs without log
- Missing loopback: triggers on configs without loopback interface
- These are correct but expected values are lower

### 3. Vendor-Agnostic Rules
New rules detect patterns across vendors:
- Telnet detection works on Cisco configs
- IPSec detection works on Cisco/Fortinet configs
- HSRP detection works on Cisco configs
- HA detection works on Fortinet configs

## Mismatch Examples

### mikrotik:security_insecure_defaults
- Actual critical: 4
- Expected critical: 1
- Reason: Multiple security issues detected (telnet, weak password, service exposure, default wireless)

### fortinet:firewall_policy_dmz
- Actual critical: 7
- Expected critical: 1
- Reason: Telnet pattern in config triggers multiple security rules

## No Crashes
- All 30 cases ran without exception
- All rules executed successfully
- No duplicate findings after fix