import { api } from "@/services/api";

export interface BlueprintResponse {
  id: string;
  name: string;
  description: string;
  model: string;
  tools: string[];
  knowledge_base_ids: string[];
  prompt: string;
  temperature: number;
  max_tokens: number;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface CreateAgentBlueprintPayload {
  name: string;
  description?: string;
  model?: string;
  tools?: string[];
  knowledge_base_ids?: string[];
  prompt?: string;
  temperature?: number;
  max_tokens?: number;
  metadata?: Record<string, unknown>;
}

export function listAgentBlueprints() {
  return api.get<BlueprintResponse[]>("/api/v1/blueprints/agent");
}

export function getAgentBlueprint(blueprintId: string) {
  return api.get<BlueprintResponse>(
    `/api/v1/blueprints/agent/${encodeURIComponent(blueprintId)}`
  );
}

export function createAgentBlueprint(payload: CreateAgentBlueprintPayload) {
  return api.post<BlueprintResponse>("/api/v1/blueprints/agent", payload);
}

export function updateAgentBlueprint(
  blueprintId: string,
  payload: Partial<CreateAgentBlueprintPayload>
) {
  return api.put<BlueprintResponse>(
    `/api/v1/blueprints/agent/${encodeURIComponent(blueprintId)}`,
    payload
  );
}

export function deleteAgentBlueprint(blueprintId: string) {
  return api.delete<{ message: string }>(
    `/api/v1/blueprints/agent/${encodeURIComponent(blueprintId)}`
  );
}

export function listMcpServers() {
  return api.get<Record<string, unknown>[]>("/api/v1/mcp/servers");
}