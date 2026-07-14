# Core Agents (Phase 1)

These are the 10 core agents implemented in Phase 1:

1. **Planner** - Analyzes requests and creates structured plans
2. **Coding Agent** - Writes and reviews code in multiple languages
3. **Research Agent** - Gathers information from web and documents
4. **Data Agent** - Handles databases, data analysis, and migrations
5. **UI Agent** - Designs and builds user interfaces
6. **Trading Agent** - Analyzes markets and executes trades
7. **Network Agent** - Configures networking and security
8. **Writer Agent** - Creates documentation and content
9. **QA Agent** - Tests and validates outputs
10. **Security Agent** - Audits code and infrastructure
11. **Reviewer** - Reviews and merges results

## Usage

```python
from backend.app.agents.orchestrator import orchestrator

result = await orchestrator.run("Build me a full-stack todo app", "conv-123")
print(result["final_result"])
```
