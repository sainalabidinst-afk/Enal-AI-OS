# Output

## Generated SDK Documentation

### Installation
```bash
pip install enal-business-analyst
```

### Quick Start
```python
from apps.business_analyst.engine import BusinessAnalystEngine
from apps.business_analyst.schemas import BusinessAnalysisRequest, OperationType

engine = BusinessAnalystEngine()
request = BusinessAnalysisRequest(
    operation=OperationType.requirement_gathering,
    business_context={"domain": "e-commerce", "project_name": "Online Shop"},
    inputs={"natural_language_requirements": ["Users must be able to create accounts"]},
)
report = engine.analyze(request)
print(f"Generated {len(report.requirements)} requirements")
```

### API Reference
- `BusinessAnalystEngine.analyze(request)`
- `BusinessAnalysisRequest`
- `BusinessAnalysisReport`
