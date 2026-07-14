# Self Development Real Cases

Real project improvement scenarios encountered while using ECP.

## Case Template

Create a folder for each case:

```
<case_name>/
├── input/
│   ├── project_snapshot/
│   └── problem_description.md
├── output/
│   ├── analysis.md
│   ├── proposal.md
│   └── patch.diff
└── evaluation.md
```

## Example Cases

- `dead_code_removal/` — Dead code detection and removal
- `architecture_improvement/` — Architecture refactoring proposal
- `test_coverage/` — Test coverage improvement
- `performance_bottleneck/` — Performance bottleneck analysis

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the project and problem.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing problem 1
- Missing solution 2

## Improvement Actions
- [ ] Improve detection for X
- [ ] Better proposal quality for Y
- [ ] Enhance impact prediction for Z

Benchmark Reference: ________
```
