# ECP Testing Strategy

ECP uses four levels of testing to ensure platform quality and application reliability.

## Test Levels

### Level 1: Unit Tests

**Focus**: Individual functions and classes in isolation.

**Scope**:
- Core algorithms (reasoning, decision engine, simulation)
- Data structures (RouterOS parser, topology model)
- Utility functions (prompt compiler, cost optimizer)

**Location**: `tests/unit/`

**Example**:
```python
def test_routeros_parser():
    config = "/interface\nadd name=ether1 type=ether\n"
    result = parse_routeros_config(config)
    assert len(result.interfaces) == 1
    assert result.interfaces[0].name == "ether1"
```

**Coverage Target**: ≥80%

---

### Level 2: Integration Tests

**Focus**: Interaction between ECP components.

**Scope**:
- SDK → Runtime communication
- Plugin → Kernel contracts
- Memory → RAG → World Model
- Event Bus → Task Queue → Workers
- Studio → Observability

**Location**: `tests/integration/`

**Example**:
```python
async def test_plugin_contract_compliance():
    plugin = load_plugin("mikrotik")
    assert plugin.validate_contract(ToolContract)
    result = await plugin.invoke({"action": "list_interfaces"})
    assert "interfaces" in result
```

**Coverage Target**: All contract boundaries

---

### Level 3: Workflow Tests

**Focus**: Complete cognitive pipelines end-to-end.

**Scope**:
- Perception → Planning → Reasoning → Decision → Action
- Debate engine with multiple agents
- Simulation → Verification → Reflection loop
- Meta-cognition pipeline selection

**Location**: `tests/workflow/`

**Example**:
```python
async def test_network_analysis_workflow():
    app = NetworkEngineerApp()
    result = await app.run("Analyze this MikroTik config", {
        "config": sample_config,
        "project_id": "test-001"
    })
    assert result["result"]["analysis"]["issues"] is not None
    assert result["result"]["documentation"] is not None
```

**Coverage Target**: All reference app workflows

---

### Level 4: Reference Application Tests

**Focus**: Real-world use cases from user perspective.

**Scope**:
- Complete user journeys
- Multi-step workflows
- Cross-component integration
- Performance under realistic load

**Location**: `tests/reference/`

**Example**:
```python
async def test_network_engineer_e2e():
    app = NetworkEngineerApp()
    
    # 1. Upload config
    config = await load_test_config("isp-backbone.rsc")
    
    # 2. Analyze
    analysis = await app.analyze_config(config)
    assert len(analysis["issues"]) > 0
    
    # 3. Generate improved config
    improved = await app.generate_config(analysis)
    
    # 4. Simulate
    sim = await app.simulate_config(improved)
    assert sim["status"] == "success"
    
    # 5. Document
    docs = await app.generate_documentation(improved)
    assert "# Network Configuration" in docs
    
    # 6. Verify artifacts
    artifacts = await get_artifacts("network-engineer")
    assert len(artifacts) >= 3  # config, analysis, docs
```

**Coverage Target**: 100% of reference app user journeys

---

## Golden Test Suite

The golden test suite is the **canonical quality gate** for ECP.

**Location**: `benchmarks/golden_test_set.py`

**Categories**:
1. **Simple Tasks** (50 tests) — Basic reasoning, coding, explanation
2. **Medium Tasks** (50 tests) — API design, database schema, configuration
3. **Complex Tasks** (50 tests) — Full-stack apps, distributed systems
4. **Domain-Specific** (50 tests) — Networking, trading, DevOps, research

**Pass Threshold**: ≥80% (160/200 tests)

**Execution**:
- Runs on every PR via CI/CD
- Must pass before merge
- Must pass before any release

---

## Test Execution Order

```
Unit Tests
  ↓
Integration Tests
  ↓
Workflow Tests
  ↓
Golden Test Suite
  ↓
Reference Application Tests
```

Any failure at any level blocks progression.

---

## Performance Benchmarks

**Location**: `benchmarks/performance_benchmark.py`

**Metrics**:
| Metric | Target | Measurement |
|--------|--------|-------------|
| Latency (avg) | <2s | Simple tasks |
| Latency (p95) | <5s | Medium tasks |
| Token Efficiency | <500 tokens/response | All tasks |
| Determinism | >0.8 | Same input → same output |
| Success Rate | >0.9 | All tasks |

---

## Adding New Tests

1. **Unit**: Add to `tests/unit/test_<module>.py`
2. **Integration**: Add to `tests/integration/test_<integration>.py`
3. **Workflow**: Add to `tests/workflow/test_<workflow>.py`
4. **Golden**: Add to `benchmarks/golden_test_set.py` in appropriate category
5. **Reference**: Add to `tests/reference/test_<app>.py`

All new tests must:
- Have clear pass/fail criteria
- Run in <30 seconds
- Be deterministic (no flaky tests)
- Include error cases
