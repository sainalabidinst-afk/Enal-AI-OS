# Evaluation

Scenario: cloud-001 - AWS Landing Zone Design

## Architecture Review
- VPC design with public/private subnets properly structured
- IAM roles and policies following least-privilege principle
- EKS cluster with managed node groups correctly configured
- ALB with WAF for edge security
- CloudFront for global content delivery

## Improvements
- Add GuardDuty for threat detection
- Implement SCPs for organizational guardrails
- Add centralized logging with CloudWatch
- Consider multi-account strategy for workload isolation
