# Infrastructure Design: zero_trust_network_access

## Architecture Overview
- Multi-tier network design with VPC isolation
- Transit Gateway for cross-VPC routing
- Direct Connect for on-prem connectivity

## Components
- VPC with private and public subnets
- NAT Gateway for outbound traffic
- VPN/Direct Connect hybrid connectivity
- WAF and Shield for protection

## Security
- Network ACLs at subnet level
- Security Groups at instance level
- TLS 1.3 enforcement
- CloudTrail and Config enabled
