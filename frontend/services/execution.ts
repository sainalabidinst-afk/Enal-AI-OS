import { api } from "./api";
import type { ExecutionSession, ExecutionPhase, ExecutionArtifact, ExecutionStatus } from "@/types/execution";

export interface StartExecutionRequest {
  goal: string;
  workspace_id: string;
  conversation_id?: string;
}

export async function startExecution(request: StartExecutionRequest): Promise<{ execution: ExecutionSession; artifacts: ExecutionArtifact[] }> {
  return api.post("/api/v1/executions/run", request);
}

export async function getExecution(executionId: string): Promise<ExecutionSession> {
  return api.get<ExecutionSession>(`/api/v1/executions/${executionId}`);
}

export async function listExecutions(workspaceId?: string): Promise<ExecutionSession[]> {
  const qs = workspaceId ? `?workspaceId=${encodeURIComponent(workspaceId)}` : "";
  return api.get<ExecutionSession[]>(`/api/v1/executions${qs}`);
}

export async function addExecutionPhase(
  executionId: string,
  phase: { name: string }
): Promise<ExecutionPhase> {
  return api.post<ExecutionPhase>(`/api/v1/executions/${executionId}/phases`, phase);
}

export async function updateExecutionPhase(
  executionId: string,
  phaseId: string,
  updates: { status?: ExecutionStatus; progress?: number }
): Promise<ExecutionPhase> {
  return api.patch<ExecutionPhase>(`/api/v1/executions/${executionId}/phases/${phaseId}`, updates);
}

export async function updateExecutionProgress(
  executionId: string,
  progress: { progress: number; eta_seconds?: number }
): Promise<{ progress: number; eta_seconds?: number }> {
  return api.post(`/api/v1/executions/${executionId}/progress`, progress);
}

export async function addExecutionLog(
  executionId: string,
  log: { message: string; level?: string; metadata?: Record<string, any> }
): Promise<{ executionId: string; log: Record<string, any> }> {
  return api.post(`/api/v1/executions/${executionId}/logs`, log);
}

export async function getExecutionLogs(executionId: string): Promise<{ logs: Array<Record<string, any>> }> {
  return api.get(`/api/v1/executions/${executionId}/logs`);
}

export async function cancelExecution(executionId: string): Promise<{ status: string; executionId: string }> {
  return api.post(`/api/v1/executions/${executionId}/cancel`);
}

export async function deleteExecution(executionId: string): Promise<{ deleted: boolean }> {
  return api.delete(`/api/v1/executions/${executionId}`);
}

export async function listExecutionArtifacts(executionId: string): Promise<ExecutionArtifact[]> {
  return api.get<ExecutionArtifact[]>(`/api/v1/executions/${executionId}/artifacts`);
}
