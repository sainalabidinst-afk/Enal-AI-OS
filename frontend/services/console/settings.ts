import { api } from "@/services/api";

export interface ConnectorRecord {
  name: string;
  description?: string;
  actions?: string[];
  connected?: boolean;
  status?: string;
}

export interface GuardrailDescriptor {
  name: string;
  description: string;
  enabled?: boolean;
}

export interface ObservabilitySnapshot {
  [key: string]: unknown;
}

export function listConnectors() {
  return api.get<{ connectors: ConnectorRecord[] }>("/api/v1/connectors");
}

export function connectConnector(connectorName: string, config?: Record<string, unknown>) {
  return api.post<{ connector: string; connected: boolean }>("/api/v1/connect", {
    connector_name: connectorName,
    config,
  });
}

export function disconnectConnector(connectorName: string) {
  return api.post<{ connector: string; connected: boolean }>("/api/v1/disconnect", {
    connector_name: connectorName,
  });
}

export function listGuardrails() {
  return api.get<{ guardrails: GuardrailDescriptor[] }>("/api/v1/guardrails");
}

export function listPolicies() {
  return api.get<{ policies: string[] }>("/api/v1/policy/policies");
}

export function getObservabilityMetrics(agent?: string) {
  const query = agent ? `?agent=${encodeURIComponent(agent)}` : "";
  return api.get<ObservabilitySnapshot>(`/api/v1/observability/metrics${query}`);
}

export function getStudioMetrics() {
  return api.get<ObservabilitySnapshot>("/api/v1/studio/metrics");
}

export function getTelemetryMetrics() {
  return api.get<ObservabilitySnapshot>("/api/v1/metrics");
}

export function getCluster() {
  return api.get<Record<string, unknown>[]>("/api/v1/distributed/cluster");
}