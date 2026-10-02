# Cloud Architect Capability Pack

**Version:** 1.0.0  
**Target Grade:** A (≥90%)  
**Status:** Implemented  

## Ringkasan

Cloud Architect Capability Pack menyediakan desain arsitektur cloud untuk AWS, Azure, dan GCP, termasuk landing zone design, multi-region strategy, cost optimization, dan disaster recovery planning.

## Kemampuan Inti

1. **Cloud Landing Zone Design** — VPC, IAM, security groups untuk AWS, Azure, GCP
2. **Multi-Region Strategy** — active-active, active-passive, disaster recovery
3. **Cost Optimization** — reserved instances, spot, autoscaling, right-sizing
4. **Security Architecture** — zero-trust, private endpoints, network segmentation

## Supported Providers

- **AWS**: VPC, EC2, S3, RDS, Lambda, EKS, CloudTrail, GuardDuty, WAF
- **Azure**: Virtual Network, VM, Storage, AKS, Azure AD, Defender
- **GCP**: VPC, Compute Engine, Cloud Storage, GKE, IAM
- **Hybrid**: ExpressRoute, Direct Connect, Interconnect

## Integration

- **Konsumsi dari**: Infrastructure Engineer (HA/DR patterns), Security Engineer (threat models)
- **Digunakan oleh**: DevOps Assistant, System Architect

## Benchmark

- 10 scenarios across 6 dimensions
- Overall score: A (≥90%)
- Scenarios: AWS Landing Zone, Azure Hybrid, GCP Multi-Region DR, Cost Optimization, Zero-Trust, Serverless, Multi-Cloud, Containerized K8s, Compliance LZ, Global CDN

## Real Cases

10 real cases in `real_cases/cloud_architect/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0026, ADR-005)
