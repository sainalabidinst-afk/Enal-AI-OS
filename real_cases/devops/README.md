# DevOps Real Cases

Real infrastructure scenarios encountered while using ECP.

## Case Template

Create a folder for each case:

```
<case_name>/
├── input/
│   └── requirements.md or infra_spec/
├── output/
│   ├── dockerfile
│   ├── ci_cd_config/
│   └── documentation.md
└── evaluation.md
```

## Example Cases

- `microservice_deploy/` — Microservice deployment pipeline
- `monitoring_setup/` — Monitoring and alerting configuration
- `kubernetes_migration/` — Kubernetes migration plan
- `cost_optimization/` — Infrastructure cost optimization

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the infrastructure scenario.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing configuration 1
- Missing best practice 2

## Improvement Actions
- [ ] Update knowledge base for X
- [ ] Improve configuration generation for Y
- [ ] Add multi-cloud pattern for Z

Benchmark Reference: ________
```
