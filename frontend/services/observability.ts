import { api } from "@/services/api";

export interface TraceSpan {
  id: string;
  trace_id: string;
  parent_id: string | null;
  type: string;
  name: string;
  agent: string;
  latency_ms: number;
  tokens: number;
  cost: number;
  success: boolean;
  error: string | null;
}

export interface TradingRegimeAlert {
  event_id: string;
  symbol: string;
  timeframe: string;
  regime: string;
  confidence: number;
  status: string;
  timestamp: string;
}

export interface CrossPackCorrelationAlert {
  event_id: string;
  source_pack: string;
  target_pack: string;
  correlation_type: string;
  confidence: number;
  details: string;
  status: string;
  timestamp: string;
}

export interface GrowthAlert {
  event_id: string;
  alert_type: string;
  severity: string;
  subject: string;
  message: string;
  details: Record<string, unknown>;
  status: string;
  source: string;
  timestamp: string;
}

export interface AlertFeedResponse {
  trading_regime: TradingRegimeAlert[];
  cross_pack_correlations: CrossPackCorrelationAlert[];
  growth_alerts: GrowthAlert[];
}

export interface GrowthSeries {
  granularity: string;
  labels: string[];
  hours: number[];
  projects: number[];
  activities: number[];
  new_skills: number[];
}

export interface GrowthSkill {
  skill: string;
  level: string;
  activities: number;
  projects_completed: number;
  minutes_spent: number;
  last_practiced: string | null;
}

export interface GrowthProgress {
  total_activities: number;
  total_projects: number;
  total_hours: number;
  active_skills: number;
  current_streak_weeks: number;
  alignment_rate: number;
  aligned_activities: number;
  unaligned_activities: number;
  generated_at: string;
  series: GrowthSeries;
  skills: GrowthSkill[];
}

export async function getTrace(traceId: string): Promise<TraceSpan[]> {
  return api.get<TraceSpan[]>(`/api/v1/observability/traces/${encodeURIComponent(traceId)}`);
}

export async function getObservabilityMetrics(): Promise<Record<string, unknown>> {
  return api.get<Record<string, unknown>>("/api/v1/observability/metrics");
}

export async function getTelemetryMetrics(): Promise<Record<string, unknown>> {
  return api.get<Record<string, unknown>>("/api/v1/metrics");
}

export async function getTelemetryAlerts(): Promise<AlertFeedResponse> {
  return api.get<AlertFeedResponse>("/api/v1/metrics/alerts");
}

export async function getPrometheusMetrics(): Promise<string> {
  const response = await api.get<string>("/api/v1/metrics/prometheus");
  return response;
}

export async function getGrowthProgress(
  granularity: "week" | "month" = "week",
  periods: number = 12,
): Promise<GrowthProgress> {
  return api.get<GrowthProgress>(
    `/api/v1/self-development/progress?granularity=${granularity}&weeks=${periods}`,
  );
}
