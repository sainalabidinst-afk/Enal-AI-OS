export interface Provider {
  name: string;
  status: string;
  models?: string[];
  latency_ms?: number;
  last_checked?: string;
}

export interface ProviderHealth {
  status: string;
  latency_ms: number;
  last_checked: string;
}

export interface ModelRouteRequest {
  taskType: string;
  capability: string;
  context?: Record<string, unknown>;
}

export interface ModelRouteResponse {
  provider: string;
  model: string;
  reason?: string;
}
