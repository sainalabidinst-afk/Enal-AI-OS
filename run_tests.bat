@echo off
py -m pytest tests/test_workflow_catalog.py tests/test_workflow_executor.py -v --tb=short
