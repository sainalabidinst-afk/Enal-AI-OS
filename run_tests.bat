@echo off
py -m pytest tests/test_workflow_catalog.py tests/test_workflow_executor.py tests/test_intent_resolver.py tests/test_ai_planner.py tests/test_multi_agent.py tests/test_reasoning_engine.py -v --tb=short
