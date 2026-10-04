"use client";

import { useEffect, useMemo } from "react";
import { useConsoleStore, type ConsoleState, type Resource } from "@/store/console-store";
import { average } from "@/lib/format";
import type { CapabilityLifecycleRecord, GovernancePack } from "@/types/console";

type LoaderKey =
  | "environment"
  | "governance"
  | "benchmark"
  | "marketplace"
  | "evaluation"
  | "blueprints"
  | "settings";

const LOADERS: Record<LoaderKey, (state: ConsoleState) => void> = {
  environment: (state) => void state.loadEnvironment(),
  governance: (state) => void state.loadGovernance(),
  benchmark: (state) => void state.loadBenchmark(),
  marketplace: (state) => void state.loadMarketplace(),
  evaluation: (state) => void state.loadEvaluation(),
  blueprints: (state) => void state.loadBlueprints(),
  settings: (state) => void state.loadSettings(),
};

/** Ensures the requested console slices are hydrated from the backend once. */
export function useConsoleHydration(...targets: LoaderKey[]) {
  const signature = targets.join("|");

  useEffect(() => {
    if (!signature) return;
    const state = useConsoleStore.getState();
    signature.split("|").forEach((target) => LOADERS[target as LoaderKey]?.(state));
  }, [signature]);
}

export interface PackCatalogEntry {
  id: string;
  name: string;
  domain: string;
  status: string | null;
  state: string | null;
  health: string | null;
  successRate: number | null;
  avgLatencyMs: number | null;
  benchmarkScore: number | null;
  coverage: number | null;
  tests: { passed: number; total: number } | null;
}

/** Projects governance packs and lifecycle records into one catalog view. */
export function usePackCatalog(): PackCatalogEntry[] {
  const packs = useConsoleStore((s) => s.packs.data);
  const lifecycle = useConsoleStore((s) => s.lifecycle.data);

  return useMemo(() => {
    const byId = new Map<string, PackCatalogEntry>();
    (packs ?? []).forEach((pack) => {
      byId.set(pack.pack_id, {
        id: pack.pack_id,
        name: pack.name,
        domain: pack.domain,
        status: pack.status,
        state: null,
        health: null,
        successRate: null,
        avgLatencyMs: null,
        benchmarkScore: pack.benchmark_score,
        coverage: pack.coverage,
        tests: { passed: pack.tests_passed, total: pack.tests_total },
      });
    });
    (lifecycle ?? []).forEach((record: CapabilityLifecycleRecord) => {
      const existing = byId.get(record.id);
      byId.set(record.id, {
        id: record.id,
        name: existing?.name ?? record.name,
        domain: existing?.domain ?? record.category,
        status: existing?.status ?? null,
        state: record.state,
        health: record.health,
        successRate: record.metrics.success_rate,
        avgLatencyMs: record.metrics.avg_latency_ms,
        benchmarkScore: existing?.benchmarkScore ?? null,
        coverage: existing?.coverage ?? null,
        tests: existing?.tests ?? null,
      });
    });
    return Array.from(byId.values()).sort((a, b) => a.name.localeCompare(b.name));
  }, [packs, lifecycle]);
}

export interface GovernanceMetricsModel {
  acceptanceRate: number | null;
  acceptedPacks: number;
  totalPacks: number;
  remediationSuccess: number | null;
  complianceCoverage: number | null;
  healthyCapabilities: number;
  totalCapabilities: number;
  avgResponseMs: number | null;
}

/**
 * Aggregates governance indicators for display.
 * Every value is a reduction over backend payloads; no new judgement is made here.
 */
export function useGovernanceMetrics(): GovernanceMetricsModel {
  const packs = useConsoleStore((s) => s.packs.data);
  const lifecycle = useConsoleStore((s) => s.lifecycle.data);
  const gateResults = useConsoleStore((s) => s.gateResults.data);

  return useMemo(() => {
    const registered = packs ?? [];
    const accepted = registered.filter((pack) =>
      ["approved", "registered"].includes(pack.status)
    ).length;
    const gated = Object.values(gateResults ?? {});
    const acceptanceRate = gated.length
      ? gated.filter((gate) => gate.passed).length / gated.length
      : registered.length
        ? accepted / registered.length
        : null;

    const capabilities = lifecycle ?? [];
    const remediationSuccess = average(
      capabilities.map((record) => record.metrics.success_rate)
    );
    const healthy = capabilities.filter((record) => record.health === "healthy").length;
    const complianceCoverage = capabilities.length ? healthy / capabilities.length : null;

    return {
      acceptanceRate,
      acceptedPacks: accepted,
      totalPacks: registered.length,
      remediationSuccess,
      complianceCoverage,
      healthyCapabilities: healthy,
      totalCapabilities: capabilities.length,
      avgResponseMs: average(
        capabilities.map((record) => record.metrics.avg_latency_ms).filter((value) => value > 0)
      ),
    };
  }, [packs, lifecycle, gateResults]);
}

export interface LatencySeriesModel {
  labels: string[];
  values: number[];
  unit: string;
}

/** Latency profile across loaded capabilities, highest first. */
export function useCapabilityLatency(limit = 8): LatencySeriesModel {
  const lifecycle = useConsoleStore((s) => s.lifecycle.data);

  return useMemo(() => {
    const rows = (lifecycle ?? [])
      .filter((record) => record.metrics.avg_latency_ms > 0)
      .map((record) => ({ label: record.id, value: record.metrics.avg_latency_ms }))
      .sort((a, b) => b.value - a.value)
      .slice(0, limit);
    return {
      labels: rows.map((row) => row.label),
      values: rows.map((row) => row.value),
      unit: "ms",
    };
  }, [lifecycle, limit]);
}

export function useGovernancePacks(): Resource<GovernancePack[]> {
  return useConsoleStore((s) => s.packs);
}