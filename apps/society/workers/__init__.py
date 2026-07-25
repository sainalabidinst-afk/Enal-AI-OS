"""
Workers
=======

Domain-specific workers that the Execution Runtime calls.
Each worker knows how to execute subtasks for its domain.
"""

from apps.society.workers.code_worker import CodeWorker, code_worker
from apps.society.workers.devops_worker import DevOpsWorker, devops_worker
from apps.society.workers.network_worker import NetworkWorker, network_worker
from apps.society.workers.research_worker import ResearchWorker, research_worker
from apps.society.workers.self_development_worker import (
    SelfDevelopmentWorker,
    self_development_worker,
)
from apps.society.workers.trading_worker import TradingWorker, trading_worker

__all__ = [
    "CodeWorker",
    "DevOpsWorker",
    "NetworkWorker",
    "ResearchWorker",
    "SelfDevelopmentWorker",
    "TradingWorker",
    "code_worker",
    "devops_worker",
    "network_worker",
    "research_worker",
    "self_development_worker",
    "trading_worker",
]
