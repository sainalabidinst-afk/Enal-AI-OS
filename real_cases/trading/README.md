# Trading Real Cases

Real market analysis scenarios encountered while using ECP.

## Case Template

Create a folder for each case:

```
<case_name>/
├── input/
│   ├── market_data.csv
│   ├── chart_screenshot.png
│   └── context.md
├── output/
│   ├── analysis.md
│   ├── recommendation.md
│   └── risk_assessment.md
└── evaluation.md
```

## Example Cases

- `btc_breakout/` — Bitcoin breakout identification and analysis
- `gold_news/` — Gold price reaction to news event
- `eurusd_nfp/` — EUR/USD analysis around NFP release
- `portfolio_rebalance/` — Portfolio rebalancing scenario

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the market scenario.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing factor 1
- Missing risk factor 2

## Improvement Actions
- [ ] Improve reasoning for X
- [ ] Better risk explanation for Y
- [ ] Add knowledge pattern for Z

Benchmark Reference: ________
```
