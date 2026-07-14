import { api } from "./api";
import type { ModelProvider, ModelRouteRequest, ModelRouteResponse, HealthStatus } from "@/types/models";

export async function listModelProviders(): Promise<ModelProvider[]> {
  return api.get<ModelProvider[]>("/api/v1/models/providers");
}

export async function checkProviderHealth(provider?: string): Promise<HealthStatus | HealthStatus[]> {
  const qs = provider ? `?provider=${encodeURIComponent(provider)}` : "";
  return api.get(`/api/v1/models/health${qs}`);
}

export async function routeModel(request: ModelRouteRequest): Promise<ModelRouteResponse> {
  return api.post<ModelRouteResponse>("/api/v1/models/route", request);
}
