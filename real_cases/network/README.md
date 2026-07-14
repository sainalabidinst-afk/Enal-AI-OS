# Network Real Cases

Real network configurations and audit scenarios encountered while using ECP.

## Case Template

Create a folder for each case:

```
<case_name>/
├── input/
│   └── config.rsc
├── output/
│   ├── analysis.md
│   └── recommendations.md
└── evaluation.md
```

## Example Cases

- `isp_dual_wan_failover/` — Dual WAN with failover rules
- `mikrotik_hotspot_school/` — School hotspot with VLANs and user management
- `campus_vlan/` — Campus network with multiple VLANs and inter-VLAN routing
- `enterprise_firewall/` — Enterprise firewall policy review

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the case.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing finding 1
- Missing finding 2

## Improvement Actions
- [ ] Update analyzer for X
- [ ] Improve recommendation for Y
- [ ] Add new rule for Z

Benchmark Reference: ________
```
