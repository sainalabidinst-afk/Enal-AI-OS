# Real-world Cases

This directory contains real-world cases collected while using ECP in actual work.
These are not golden tests. These are daily usage artifacts that drive Capability Pack improvement.

## Structure

Each Capability Pack has its own folder:

```
real_cases/
├── network/           # Real network configurations and audits
├── code/              # Real codebases reviewed or generated
├── research/          # Real research questions and sources
├── trading/           # Real market analysis scenarios
├── devops/            # Real infrastructure scenarios
└── self_development/  # Real project improvement cases
```

## What to Store

For each real-world case, create a folder with:

1. **Input**: What the user provided
2. **Output**: What ECP produced
3. **Evaluation**: What was good, what was wrong, what was missing
4. **Benchmark ID**: Link to associated benchmark if updated

Example:

```
network/isp_dual_wan_failover/
├── input/
│   └── config.rsc
├── output/
│   ├── analysis.md
│   └── recommendations.md
└── evaluation.md
```

## How to Use

1. Run ECP against a real case
2. Save input, output, and evaluation
3. If improvements are needed, update the Capability Pack
4. Reference this case in the Capability Benchmark

This is how Capability Packs become genuinely expert: through real-world iteration, not synthetic tests alone.
