import { api } from "@/services/api";

export type MetricsResponse = {
  analysis: {
    count: number;
    success_count: number;
    error_count: number;
    avg_total_time_ms: number;
    avg_confidence: number;
    avg_findings: number;
    avg_compliance_score: number;
    vendor_distribution: Record<string, number>;
    parser_distribution: Record<string, number>;
  };
  chat: {
    count: number;
    success_count: number;
    error_count: number;
    avg_total_time_ms: number;
  };
  parser: {
    count: number;
    parser_distribution: Record<string, number>;
    vendor_distribution: Record<string, number>;
  };
  reasoning: {
    count: number;
    success_count: number;
    error_count: number;
  };
};

export async function getMetrics() {
  return api.get<MetricsResponse>("/api/v1/metrics");
}
