import { api } from "./api";
import type { Workspace, WorkspaceCreateRequest, WorkspaceAddFileRequest, WorkspaceMemoryRequest } from "@/types/workspace";

export async function listWorkspaces(): Promise<Workspace[]> {
  return api.get<Workspace[]>("/api/v1/workspaces");
}

export async function createWorkspace(request: WorkspaceCreateRequest): Promise<Workspace> {
  return api.post<Workspace>("/api/v1/workspaces", request);
}

export async function getWorkspace(workspaceId: string): Promise<Workspace> {
  return api.get<Workspace>(`/api/v1/workspaces/${workspaceId}`);
}

export async function deleteWorkspace(workspaceId: string): Promise<{ deleted: boolean }> {
  return api.delete<{ deleted: boolean }>(`/api/v1/workspaces/${workspaceId}`);
}

export async function addWorkspaceFile(
  workspaceId: string,
  request: WorkspaceAddFileRequest
): Promise<{ workspaceId: string; filename: string; path: string }> {
  return api.post(`/api/v1/workspaces/${workspaceId}/files`, request);
}

export async function listWorkspaceFiles(workspaceId: string): Promise<{ workspaceId: string; files: Array<Record<string, any>> }> {
  return api.get(`/api/v1/workspaces/${workspaceId}/files`);
}

export async function getWorkspaceFile(
  workspaceId: string,
  filename: string
): Promise<{ workspaceId: string; filename: string; path: string; size: number; uploaded_at: string; metadata?: Record<string, any> }> {
  return api.get(`/api/v1/workspaces/${workspaceId}/files/${filename}`);
}

export async function deleteWorkspaceFile(workspaceId: string, filename: string): Promise<{ workspaceId: string; filename: string; deleted: boolean }> {
  return api.delete(`/api/v1/workspaces/${workspaceId}/files/${filename}`);
}

export async function setWorkspaceMemory(workspaceId: string, request: WorkspaceMemoryRequest): Promise<{ workspaceId: string; key: string }> {
  return api.post(`/api/v1/workspaces/${workspaceId}/memory`, { ...request, workspace_id: workspaceId });
}

export async function getWorkspaceMemory(
  workspaceId: string,
  key: string
): Promise<{ workspaceId: string; key: string; value: any }> {
  return api.get(`/api/v1/workspaces/${workspaceId}/memory/${encodeURIComponent(key)}`);
}
