"use client";

import { create } from "zustand";
import * as governanceApi from "@/services/console/governance";
import * as benchmarkApi from "@/services/console/benchmark";
import * as marketplaceApi from "@/services/console/marketplace";
import * as evaluationApi from "@/services/console/evaluation";
import * as environmentApi from "@/services/console/environment";
import * as builderApi from "@/services/console/builder";
import * as settingsApi from "@/services/console/settings";
import { getMetrics, type MetricsResponse } from "@/services/metrics";
import * as tradingApi from "@/services/trading";
import type { FeedStatusResponse, MarketRegimeLive } from "@/types/trading";
import type {
  AuditEntry,
  BenchmarkRunResult,
  BenchmarkSuite,
  CapabilityLifecycleRecord,
  CapabilityLifecycleSummary,
  CapabilityScores,
  CceStatus,
  CloneReceipt,
  EvaluationResult,
  EvaluationResultsResponse,
  GovernancePack,
  MarketplaceListing,
  MarketplaceTemplate,
  ModelProviderStatus,
  QualityGateResult,
  ScheduleJob,
  ServiceHealth,
  VoiceProviderInfo,
} from "@/types/console";
import type { BlueprintResponse } from "@/services/console/builder";

export type RequestStatus = "idle" | "loading" | "success" | "error";

export interface Resource<T> {
  data: T | null;
  status: RequestStatus;
  error: string | null;
  updatedAt: string | null;
}

export const RESOURCE_KEYS = [
  "health",
  "modelProviders",
  "voiceProviders",
  "packs",
  "lifecycle",
  "lifecycleSummary",
  "audit",
  "gateResults",
  "benchmarkSuite",
  "benchmarkRun",
  "capabilityScores",
  "cceStatus",
  "templates",
  "listings",
  "evaluationResults",
  "evaluation",
  "schedules",
  "blueprints",
  "connectors",
  "guardrails",
  "policies",
  "telemetry",
  "observability",
  "feedStatus",
  "regime",
] as const;

export type ResourceKey = (typeof RESOURCE_KEYS)[number];

export function resource<T>(data: T | null = null): Resource<T> {
  return { data, status: "idle", error: null, updatedAt: null };
}

function errorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  return "Request failed";
}

function isLoading(loadings: string[], key: ResourceKey): boolean {
  return loadings.includes(key);
}

export interface ConsoleResources {
  health: Resource<ServiceHealth>;
  modelProviders: Resource<ModelProviderStatus[]>;
  voiceProviders: Resource<VoiceProviderInfo>;
  packs: Resource<GovernancePack[]>;
  lifecycle: Resource<CapabilityLifecycleRecord[]>;
  lifecycleSummary: Resource<CapabilityLifecycleSummary>;
  audit: Resource<AuditEntry[]>;
  gateResults: Resource<Record<string, QualityGateResult>>;
  benchmarkSuite: Resource<BenchmarkSuite>;
  benchmarkRun: Resource<BenchmarkRunResult>;
  capabilityScores: Resource<CapabilityScores>;
  cceStatus: Resource<CceStatus>;
  templates: Resource<MarketplaceTemplate[]>;
  listings: Resource<MarketplaceListing[]>;
  evaluation: Resource<EvaluationResult>;
  evaluationResults: Resource<EvaluationResultsResponse>;
  schedules: Resource<ScheduleJob[]>;
  blueprints: Resource<BlueprintResponse[]>;
  connectors: Resource<settingsApi.ConnectorRecord[]>;
  guardrails: Resource<settingsApi.GuardrailDescriptor[]>;
  policies: Resource<string[]>;
  telemetry: Resource<MetricsResponse>;
  observability: Resource<settingsApi.ObservabilitySnapshot>;
  feedStatus: Resource<FeedStatusResponse>;
  regime: Resource<MarketRegimeLive>;
}

export interface RegimeHistoryPoint {
  sequence: number;
  symbol: string;
  regime: string;
  confidence: number;
  volatility: string;
  trend_strength: number;
  timestamp: number;
}

export type StreamStatus = "idle" | "connecting" | "live" | "error";

export interface ConsoleState extends ConsoleResources {
  cloneReceipts: Resource<CloneReceipt[]>;
  regimeHistory: RegimeHistoryPoint[];
  streamStatus: StreamStatus;
  streamSymbol: string | null;
  lastSyncAt: string | null;
  loading: string[];
  loadEnvironment: () => Promise<void>;
  loadGovernance: () => Promise<void>;
  runQualityGate: (packId: string) => Promise<QualityGateResult | null>;
  loadBenchmark: () => Promise<void>;
  loadCapabilityScores: () => Promise<void>;
  executeBenchmarkRun: () => Promise<void>;
  loadMarketplace: () => Promise<void>;
  cloneTemplate: (templateId: string, project: string) => Promise<CloneReceipt | null>;
  loadEvaluation: () => Promise<void>;
  runEvaluation: (output: string) => Promise<EvaluationResult | null>;
  loadBlueprints: () => Promise<void>;
  saveBlueprint: (payload: builderApi.CreateAgentBlueprintPayload) => Promise<void>;
  loadSettings: () => Promise<void>;
  loadFeedStatus: () => Promise<void>;
  fetchLiveRegime: (symbol: string) => Promise<MarketRegimeLive | null>;
  startFeed: (symbol: string, timeframes?: string[], pollInterval?: number) => Promise<void>;
  stopFeed: () => Promise<void>;
  connectRegimeStream: (symbol: string, interval?: number) => Promise<void>;
  disconnectRegimeStream: () => void;
}

type Loaded<K extends ResourceKey> = Exclude<ConsoleResources[K]["data"], null>;

const HISTORY_LIMIT = 60;

function appendHistory(
  current: RegimeHistoryPoint[],
  point: RegimeHistoryPoint,
  replaceLast = false
): RegimeHistoryPoint[] {
  const next = replaceLast ? [point] : [...current, point];
  return next.slice(-HISTORY_LIMIT);
}

let streamController: AbortController | null = null;

export const useConsoleStore = create<ConsoleState>((set, get) => {
  async function load<K extends ResourceKey>(
    key: K,
    task: () => Promise<Loaded<K>>
  ): Promise<Loaded<K> | null> {
    const begin = (state: ConsoleState): Partial<ConsoleState> =>
      ({
        loading: [...state.loading, key],
        [key]: { ...state[key], status: "loading", error: null },
      }) as Partial<ConsoleState>;

    set(begin);

    try {
      const value = await task();
      set(
        (state) =>
          ({
            [key]: {
              ...state[key],
              data: value,
              status: "success",
              error: null,
              updatedAt: new Date().toISOString(),
            },
          }) as Partial<ConsoleState>
      );
      return value;
    } catch (error) {
      set(
        (state) =>
          ({
            [key]: { ...state[key], status: "error", error: errorMessage(error) },
          }) as Partial<ConsoleState>
      );
      return null;
    } finally {
      set((state) => ({ loading: state.loading.filter((item) => item !== key) }));
    }
  }

  function synced() {
    set({ lastSyncAt: new Date().toISOString() });
  }

  return {
    health: resource(),
    modelProviders: resource(),
    voiceProviders: resource(),
    packs: resource(),
    lifecycle: resource(),
    lifecycleSummary: resource(),
    audit: resource(),
    gateResults: resource(),
    benchmarkSuite: resource(),
    benchmarkRun: resource(),
    capabilityScores: resource(),
    cceStatus: resource(),
    templates: resource(),
    listings: resource(),
    cloneReceipts: resource(),
    feedStatus: resource(),
    regime: resource(),
    regimeHistory: [],
    streamStatus: "idle",
    streamSymbol: null,
    evaluation: resource(),
    evaluationResults: resource(),
    schedules: resource(),
    blueprints: resource(),
    connectors: resource(),
    guardrails: resource(),
    policies: resource(),
    telemetry: resource(),
    observability: resource(),
    lastSyncAt: null,
    loading: [],

    async loadEnvironment() {
      await Promise.all([
        load("health", () => environmentApi.getServiceHealth()),
        load("modelProviders", async () => {
          const response = await environmentApi.getModelProviders();
          return Array.isArray(response)
            ? response
            : Object.values(response ?? {});
        }),
        load("voiceProviders", () => environmentApi.getVoiceProviders()),
      ]);
      synced();
    },

    async loadGovernance() {
      await Promise.all([
        load("packs", async () => (await governanceApi.listGovernancePacks()).packs),
        load("lifecycle", async () =>
          (await governanceApi.listCapabilityLifecycle()).capabilities
        ),
        load("lifecycleSummary", async () =>
          (await governanceApi.listCapabilityLifecycle()).summary
        ),
        load("audit", async () => (await governanceApi.getAuditTrail()).entries),
      ]);
      synced();
    },

    async runQualityGate(packId) {
      try {
        const result = await governanceApi.evaluateQualityGate(packId);
        set((state) => ({
          gateResults: {
            ...state.gateResults,
            data: { ...(state.gateResults.data ?? {}), [packId]: result },
            status: "success",
            error: null,
            updatedAt: new Date().toISOString(),
          },
        }));
        return result;
      } catch (error) {
        set((state) => ({
          gateResults: {
            ...state.gateResults,
            status: "error",
            error: errorMessage(error),
          },
        }));
        return null;
      }
    },

    async loadBenchmark() {
      await Promise.all([
        load("benchmarkSuite", () => benchmarkApi.getBenchmarkSuite()),
        load("cceStatus", () => benchmarkApi.getCceStatus()),
      ]);
      synced();
    },

    async loadCapabilityScores() {
      await load("capabilityScores", () => benchmarkApi.getCapabilityScores());
    },

    async executeBenchmarkRun() {
      const previous = get().benchmarkRun;
      set((state) => ({
        loading: [...state.loading, "benchmarkRun"],
        benchmarkRun: { ...state.benchmarkRun, status: "loading", error: null },
      }));
      try {
        const result = await benchmarkApi.runBenchmark();
        set({
          benchmarkRun: {
            data: result,
            status: "success",
            error: null,
            updatedAt: new Date().toISOString(),
          },
        });
      } catch (error) {
        set((state) => ({
          benchmarkRun: {
            ...previous,
            status: "error",
            error: errorMessage(error),
          },
        }));
      } finally {
        set((state) => ({
          loading: state.loading.filter((item) => item !== "benchmarkRun"),
        }));
      }
    },

    async loadMarketplace() {
      await Promise.all([
        load("templates", () => marketplaceApi.listTemplates()),
        load("listings", () => marketplaceApi.listListings()),
      ]);
      synced();
    },

    async cloneTemplate(templateId, project) {
      try {
        const receipt = await marketplaceApi.cloneTemplate(templateId, project);
        set((state) => ({
          cloneReceipts: {
            data: [receipt, ...(state.cloneReceipts.data ?? [])],
            status: "success",
            error: null,
            updatedAt: new Date().toISOString(),
          },
        }));
        return receipt;
      } catch (error) {
        set((state) => ({
          cloneReceipts: {
            ...state.cloneReceipts,
            status: "error",
            error: errorMessage(error),
          },
        }));
        return null;
      }
    },

    async loadEvaluation() {
      await Promise.all([
        load("evaluationResults", () => evaluationApi.getEvaluationResults()),
        load("schedules", () => evaluationApi.listSchedules()),
      ]);
      synced();
    },

    async runEvaluation(output) {
      await load("evaluation", () => evaluationApi.evaluateOutput({ output }));
      return get().evaluation.data;
    },

    async loadBlueprints() {
      await load("blueprints", () => builderApi.listAgentBlueprints());
    },

    async saveBlueprint(payload) {
      await load("blueprints", async () => {
        const created = await builderApi.createAgentBlueprint(payload);
        const current = get().blueprints.data ?? [];
        return [created, ...current.filter((item) => item.id !== created.id)];
      });
    },

    async loadSettings() {
      await Promise.all([
        load("connectors", async () => (await settingsApi.listConnectors()).connectors),
        load("guardrails", async () => (await settingsApi.listGuardrails()).guardrails),
        load("policies", async () => (await settingsApi.listPolicies()).policies),
        load("telemetry", () => getMetrics()),
        load("observability", () => settingsApi.getObservabilityMetrics()),
      ]);
      synced();
    },

    async loadFeedStatus() {
      await load("feedStatus", () => tradingApi.getFeedStatus());
    },

    async fetchLiveRegime(symbol) {
      const pair = symbol.trim().toUpperCase();
      if (!pair) return null;
      const result = await load("regime", () => tradingApi.getLiveRegime(pair));
      if (result) {
        set((state) => ({
          regimeHistory: appendHistory(state.regimeHistory, {
            sequence: state.regimeHistory.length,
            symbol: result.symbol ?? pair,
            regime: result.regime,
            confidence: result.confidence,
            volatility: result.volatility,
            trend_strength: result.trend_strength,
            timestamp: result.timestamp ?? Date.now() / 1000,
          }),
        }));
      }
      return result;
    },

    async startFeed(symbol, timeframes, pollInterval) {
      await tradingApi.startLiveFeed({
        symbol: symbol.trim().toUpperCase(),
        timeframes,
        pollInterval,
      });
      await get().loadFeedStatus();
    },

    async stopFeed() {
      await tradingApi.stopLiveFeed();
      await get().loadFeedStatus();
    },

    async connectRegimeStream(symbol, interval = 5) {
      const pair = symbol.trim().toUpperCase();
      if (!pair) return;
      streamController.abort();
      streamController = new AbortController();
      set({ streamStatus: "connecting", streamSymbol: pair });
      try {
        await tradingApi.streamFeed({
          symbol: pair,
          interval,
          signal: streamController.signal,
          onTick: (tick, isSnapshot) => {
            set((state) => ({
              feedStatus: { ...state.feedStatus, data: tick.feed, status: "success", error: null },
              regime: {
                data: tick.regime,
                status: "success",
                error: null,
                updatedAt: new Date().toISOString(),
              },
              regimeHistory: appendHistory(state.regimeHistory, {
                sequence: tick.sequence,
                symbol: tick.symbol,
                regime: tick.regime.regime,
                confidence: tick.regime.confidence,
                volatility: tick.regime.volatility,
                trend_strength: tick.regime.trend_strength,
                timestamp: tick.regime.timestamp ?? tick.emitted_at,
              }, isSnapshot),
              streamStatus: "live",
            }));
          },
          onError: () => set({ streamStatus: "error" }),
        });
        if (!streamController.signal.aborted) set({ streamStatus: "idle" });
      } catch (error) {
        set({
          streamStatus: "error",
          regime: {
            data: null,
            status: "error",
            error: errorMessage(error),
            updatedAt: null,
          },
        });
      }
    },

    disconnectRegimeStream() {
      streamController.abort();
      streamController = null;
      set({ streamStatus: "idle" });
    },
  };
});

export function selectResource<K extends ResourceKey>(
  key: K
): (state: ConsoleState) => Resource<Loaded<K>> {
  return (state) => state[key] as Resource<Loaded<K>>;
}

export function selectIsLoading(key: ResourceKey) {
  return (state: ConsoleState) => isLoading(state.loading, key);
}