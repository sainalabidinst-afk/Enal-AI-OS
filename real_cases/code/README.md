# Code Real Cases

Real codebases reviewed or generated while using ECP.

## Case Template

Create a folder for each case:

```
<case_name>/
├── input/
│   └── <source_code_or_requirements>
├── output/
│   ├── review.md or generated_code/
│   └── recommendations.md
└── evaluation.md
```

## Example Cases

- `legacy_php/` — Legacy PHP codebase review
- `fastapi_microservice/` — FastAPI microservice generation
- `react_dashboard/` — React dashboard from requirements
- `database_refactor/` — Database schema refactoring

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
- [ ] Update architecture knowledge for X
- [ ] Improve code generation for Y
- [ ] Add new pattern detection for Z

Benchmark Reference: ________
```
