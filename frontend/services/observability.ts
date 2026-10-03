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

export async function getTrace(traceId: string): Promise<TraceSpan[]> {
  return api.get<TraceSpan[]>(`/api/v1/observability/traces/${encodeURIComponent(traceId)}`);
}

export async function getObservabilityMetrics(): Promise<Record<string, unknown>> {
  return api.get<Record<string, unknown>>("/api/v1/observability/metrics");
}
