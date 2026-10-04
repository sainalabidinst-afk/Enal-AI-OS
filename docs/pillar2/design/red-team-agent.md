# Red Team Agent (Adversarial Testing)

## Responsibility
Automatically discover vulnerabilities in plans and decisions via adversarial simulation.

## Components
- `RedTeamAgent`
- `HardeningLoop`
- `VulnerabilityReporter`

## Flow
1. Receive plan/decision from Planning Service.
2. Generate adversarial test cases.
3. Execute tests in sandbox.
4. Report vulnerabilities.
5. HardeningLoop feeds findings back to planner.
6. Repeat until no critical vulnerabilities remain.

## Data Contract
```json
{
  "test_id": "string",
  "plan_id": "string",
  "vulnerabilities": [
    {
      "type": "security | risk | logic",
      "severity": "low | medium | high | critical",
      "description": "string",
      "recommendation": "string"
    }
  ],
  "status": "pending | completed | hardened"
}
```

## VS Code Deliverables
- Add `apps/adversarial_testing/red_team_agent.py`
- Add `apps/adversarial_testing/hardening_loop.py`
- Add `apps/adversarial_testing/vulnerability_reporter.py`
