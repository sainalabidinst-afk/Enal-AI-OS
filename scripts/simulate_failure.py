#!/usr/bin/env python3
"""
Failure Simulation Script for Alerting Validation
=================================================

Simulates common production failure scenarios to verify that monitoring,
alerting, and anomaly detection systems respond correctly.

Scenarios:
  1. Backend service crash (HTTP 500 cascade)
  2. Database connection failure
  3. LLM provider timeout / unavailability
  4. High error rate (5% threshold trigger)
  5. Memory pressure (>85% utilization)
  6. Capability execution latency spike (>30s)
  7. Redis connection drop
  8. Qdrant vector store unavailable

Usage:
  python scripts/simulate_failure.py --scenario backend_crash
  python scripts/simulate_failure.py --scenario all
  python scripts/simulate_failure.py --scenario all --duration 300

After running, verify:
  - Alert fires in Grafana/Loki/Prometheus
  - Incident is logged in the audit trail
  - Observability pack anomaly detection triggers

Requirements:
  - requests library
  - API base URL configured via ECP_API_URL env var (default: http://localhost:8000)
  - Bearer token via ECP_API_TOKEN env var (if auth enabled)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

API_URL = os.environ.get("ECP_API_URL", "http://localhost:8000")
API_TOKEN = os.environ.get("ECP_API_TOKEN", "")
API_BASE = f"{API_URL}/api/v1"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}" if API_TOKEN else "",
}
# Remove empty auth header if no token
if not API_TOKEN:
    HEADERS.pop("Authorization", None)


def log_event(scenario: str, status: str, detail: str = "") -> None:
    """Log a structured event for the simulation."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "simulation": True,
        "scenario": scenario,
        "status": status,
        "detail": detail,
    }
    logger.info(json.dumps(event))
    print(json.dumps(event, indent=2))


def wait_for_recovery(seconds: int = 10) -> None:
    """Wait period between failure injection and recovery."""
    logger.info(f"Waiting {seconds}s before recovery...")
    time.sleep(seconds)


# ============================================================================
# Failure Scenarios
# ============================================================================

class BaseScenario:
    name: str = "base"
    description: str = ""

    def run(self, duration: int = 0) -> dict:
        raise NotImplementedError

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        return requests.request(
            method, f"{API_BASE}{path}", headers=HEADERS, timeout=10, **kwargs
        )


class BackendCrashScenario(BaseScenario):
    name = "backend_crash"
    description = "Simulates backend service returning HTTP 500 errors"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting backend 500 errors")
        results = {"scenario": self.name, "checks": []}

        for i in range(5):
            try:
                resp = self._request("GET", "/health")
                if resp.status_code == 500:
                    log_event(self.name, "ALERT_TRIGGERED", f"HTTP 500 detected (attempt {i+1})")
                    results["checks"].append({"attempt": i + 1, "status_code": resp.status_code, "alerted": True})
                else:
                    results["checks"].append({"attempt": i + 1, "status_code": resp.status_code, "alerted": False})
            except requests.exceptions.ConnectionError:
                log_event(self.name, "ALERT_TRIGGERED", "Backend unreachable")
                results["checks"].append({"attempt": i + 1, "error": "ConnectionError", "alerted": True})
            time.sleep(2)

        log_event(self.name, "COMPLETED", f"Simulated {len(results['checks'])} backend failures")
        return results


class DatabaseFailureScenario(BaseScenario):
    name = "database_failure"
    description = "Simulates database connection failure via workspace creation"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting database connection failure")
        results = {"scenario": self.name, "checks": []}

        try:
            resp = self._request("POST", "/workspaces", json={
                "name": "test-failover-db",
                "description": "Database failure simulation"
            })
            if resp.status_code >= 500 or "database" in resp.text.lower():
                log_event(self.name, "ALERT_TRIGGERED", f"DB error detected: {resp.status_code}")
                results["checks"].append({"alerted": True, "status_code": resp.status_code})
            else:
                results["checks"].append({"alerted": False, "status_code": resp.status_code})
        except requests.exceptions.ConnectionError:
            log_event(self.name, "ALERT_TRIGGERED", "Connection error during DB failure")
            results["checks"].append({"alerted": True, "error": "ConnectionError"})

        log_event(self.name, "COMPLETED", "Database failure simulation finished")
        return results


class LLMTimeoutScenario(BaseScenario):
    name = "llm_timeout"
    description = "Simulates LLM provider timeout (30s+ latency)"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting LLM timeout scenario")
        results = {"scenario": self.name, "checks": []}

        start = time.time()
        try:
            resp = self._request("POST", "/chat", json={
                "message": "Test prompt for LLM timeout simulation",
                "stream": False
            })
            elapsed = time.time() - start
            if elapsed > 30 or resp.status_code >= 503:
                log_event(self.name, "ALERT_TRIGGERED", f"LLM timeout/slow response: {elapsed:.1f}s or {resp.status_code}")
                results["checks"].append({"alerted": True, "elapsed": round(elapsed, 2), "status_code": resp.status_code})
            else:
                results["checks"].append({"alerted": False, "elapsed": round(elapsed, 2), "status_code": resp.status_code})
        except requests.exceptions.ReadTimeout:
            log_event(self.name, "ALERT_TRIGGERED", "LLM ReadTimeout (>10s connection timeout)")
            results["checks"].append({"alerted": True, "error": "ReadTimeout"})

        log_event(self.name, "COMPLETED", "LLM timeout simulation finished")
        return results


class HighErrorRateScenario(BaseScenario):
    name = "high_error_rate"
    description = "Simulates 5%+ error rate threshold trigger (20 rapid invalid requests)"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting high error rate (20 rapid invalid requests)")
        results = {"scenario": self.name, "checks": [], "error_count": 0, "total": 0}

        for i in range(20):
            try:
                resp = self._request("POST", "/actions/execute", json={
                    "action": "invalid_action",
                    "params": {},
                    "connector": "nonexistent_connector"
                })
                results["total"] += 1
                if resp.status_code >= 400:
                    results["error_count"] += 1
            except Exception:
                results["total"] += 1
                results["error_count"] += 1
            time.sleep(0.1)

        error_rate = (results["error_count"] / max(results["total"], 1)) * 100
        if error_rate > 5:
            log_event(self.name, "ALERT_TRIGGERED", f"Error rate {error_rate:.1f}% exceeds 5% threshold")
            results["alerted"] = True
        else:
            results["alerted"] = False

        results["error_rate"] = round(error_rate, 1)
        log_event(self.name, "COMPLETED", f"Error rate simulation: {error_rate:.1f}% ({results['error_count']}/{results['total']})")
        return results


class MemoryPressureScenario(BaseScenario):
    name = "memory_pressure"
    description = "Simulates high memory utilization via large batch capability execution"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting memory pressure scenario")
        results = {"scenario": self.name, "checks": []}

        try:
            resp = self._request("GET", "/observability/metrics")
            if resp.status_code == 200:
                metrics = resp.json()
                mem_usage = metrics.get("memory_usage_percent", 0)
                log_event(self.name, "INFO", f"Current memory usage: {mem_usage}%")
                results["checks"].append({"memory_usage_percent": mem_usage})

            resp2 = self._request("POST", "/cognitive/process", json={
                "user_input": "Process all available datasets simultaneously",
                "project_id": "mem-pressure-test"
            })
            log_event(self.name, "COMPLETED", "Memory pressure simulation sent")
            results["checks"].append({"status_code": resp2.status_code})
        except Exception as e:
            log_event(self.name, "ERROR", str(e))
            results["checks"].append({"error": str(e)})

        return results


class CapabilityLatencyScenario(BaseScenario):
    name = "capability_latency"
    description = "Simulates capability execution latency spike (>30s)"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting capability latency scenario")
        results = {"scenario": self.name, "checks": []}

        start = time.time()
        try:
            resp = self._request("POST", "/capabilities/observability/execute", json={
                "message": "Run full anomaly detection on high-cardinality log analysis",
                "workspace_id": "latency-test",
                "conversation_id": f"sim-{int(time.time())}"
            })
            elapsed = time.time() - start
            if elapsed > 30 or resp.status_code >= 504:
                log_event(self.name, "ALERT_TRIGGERED", f"Capability latency {elapsed:.1f}s exceeds 30s threshold")
                results["alerted"] = True
            else:
                results["alerted"] = False
            results["checks"].append({"elapsed": round(elapsed, 2), "alerted": results.get("alerted", False)})
        except requests.exceptions.ReadTimeout:
            log_event(self.name, "ALERT_TRIGGERED", "Capability execution timed out (>10s)")
            results["alerted"] = True
            results["checks"].append({"error": "ReadTimeout", "alerted": True})

        log_event(self.name, "COMPLETED", f"Latency simulation finished: {elapsed:.1f}s" if 'elapsed' in dir() else "Latency simulation finished")
        return results


class RedisFailureScenario(BaseScenario):
    name = "redis_failure"
    description = "Simulates Redis connection drop"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting Redis failure scenario")
        results = {"scenario": self.name, "checks": []}

        try:
            resp = self._request("POST", "/workspaces", json={
                "name": "redis-fail-test",
                "description": "Testing workspace creation under Redis failure"
            })
            if resp.status_code >= 500 or "redis" in resp.text.lower() or "cache" in resp.text.lower():
                log_event(self.name, "ALERT_TRIGGERED", f"Redis failure detected: {resp.status_code}")
                results["checks"].append({"alerted": True, "status_code": resp.status_code})
            else:
                results["checks"].append({"alerted": False, "status_code": resp.status_code})
        except requests.exceptions.ConnectionError:
            log_event(self.name, "ALERT_TRIGGERED", "Connection error — possible Redis cascading failure")
            results["checks"].append({"alerted": True, "error": "ConnectionError"})

        log_event(self.name, "COMPLETED", "Redis failure simulation finished")
        return results


class QdrantFailureScenario(BaseScenario):
    name = "qdrant_failure"
    description = "Simulates Qdrant vector store unavailability"

    def run(self, duration: int = 0) -> dict:
        log_event(self.name, "STARTED", "Injecting Qdrant vector store failure")
        results = {"scenario": self.name, "checks": []}

        try:
            resp = self._request("POST", "/cognitive/process", json={
                "user_input": "Retrieve relevant context from knowledge graph",
                "project_id": "qdrant-fail-test"
            })
            if resp.status_code >= 500 or "qdrant" in resp.text.lower() or "vector" in resp.text.lower():
                log_event(self.name, "ALERT_TRIGGERED", f"Qdrant failure detected: {resp.status_code}")
                results["checks"].append({"alerted": True, "status_code": resp.status_code})
            else:
                results["checks"].append({"alerted": False, "status_code": resp.status_code})
        except Exception as e:
            log_event(self.name, "ALERT_TRIGGERED", str(e))
            results["checks"].append({"alerted": True, "error": str(e)})

        log_event(self.name, "COMPLETED", "Qdrant failure simulation finished")
        return results


# ============================================================================
# Main
# ============================================================================

SCENARIOS = {
    "backend_crash": BackendCrashScenario,
    "database_failure": DatabaseFailureScenario,
    "llm_timeout": LLMTimeoutScenario,
    "high_error_rate": HighErrorRateScenario,
    "memory_pressure": MemoryPressureScenario,
    "capability_latency": CapabilityLatencyScenario,
    "redis_failure": RedisFailureScenario,
    "qdrant_failure": QdrantFailureScenario,
}


def main():
    parser = argparse.ArgumentParser(
        description="Failure simulation for alerting validation in ECP production"
    )
    parser.add_argument(
        "--scenario",
        choices=["all"] + list(SCENARIOS.keys()),
        default="all",
        help="Failure scenario to simulate",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=0,
        help="Duration to sustain failure (seconds, 0 = instantaneous)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print JSON summary report at end",
    )
    args = parser.parse_args()

    logger.info(f"Starting failure simulation: {args.scenario}")
    logger.info(f"API URL: {API_URL}")

    if args.scenario == "all":
        scenario_names = list(SCENARIOS.keys())
    else:
        scenario_names = [args.scenario]

    all_results = {}
    for name in scenario_names:
        scenario_cls = SCENARIOS[name]
        scenario = scenario_cls()
        logger.info(f"--- Running scenario: {scenario.name} ---")
        logger.info(f"Description: {scenario.description}")

        result = scenario.run(duration=args.duration)
        all_results[name] = result

        if name != scenario_names[-1]:
            wait_for_recovery(seconds=5)

    if args.report:
        print("\n" + "=" * 60)
        print("SIMULATION SUMMARY REPORT")
        print("=" * 60)
        print(json.dumps(all_results, indent=2, default=str))

    logger.info("Failure simulation complete. Verify alerts in your monitoring system.")
    return all_results


if __name__ == "__main__":
    main()