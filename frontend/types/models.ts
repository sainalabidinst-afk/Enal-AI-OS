export interface ModelProvider {
  id: string;
  name: string;
  status: string;
  models?: Array<{
    id: string;
    name: string;
    provider: string;
  }>;
}

export interface ModelRouteRequest {
  taskType: string;
  capability?: string;
  context?: Record<string, any>;
}

export interface ModelRouteResponse {
  model: string;
  provider: string;
  reason?: string;
}

export interface HealthStatus {
  provider: string;
  status: string;
  latency_ms?: number;
  error?: string;
}
