## Pull Request

**Pack:** <!-- e.g., system_architect, trading_analyst -->
**Type:** <!-- enhancement | bugfix | knowledge | governance | benchmark -->

### Description
<!-- Explain what this PR changes and why -->

### Governance Checklist
- [ ] **ADR Reference** (if Core changes): Core modifications reference an approved ADR in `docs/adr/`
- [ ] **Capability First Rule**: No cross-capability imports — use Execution Runtime and shared contracts
- [ ] **Architecture Freeze**: Core changes have evidence from ≥2 capability packs
- [ ] **No Architecture Violations**: All existing boundary tests still pass
- [ ] **Golden Tests**: New golden test scenarios added if new knowledge area
- [ ] **Benchmark**: Benchmark impact assessed (run `python benchmarks/<pack>_benchmark.py`)

### Files Changed
<!-- Brief overview of what changed -->

### Test Plan
<!-- How was this tested? -->
