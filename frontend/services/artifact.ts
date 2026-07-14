import { api } from "./api";
import type { Artifact, ArtifactCreateRequest, ArtifactAddVersionRequest } from "@/types/artifact";

export async function listArtifacts(workspaceId?: string, artifactType?: string): Promise<Artifact[]> {
  const qs = new URLSearchParams();
  if (workspaceId) qs.set("workspaceId", workspaceId);
  if (artifactType) qs.set("artifactType", artifactType);
  const query = qs.toString() ? `?${qs.toString()}` : "";
  return api.get<Artifact[]>(`/api/v1/artifacts${query}`);
}

export async function createArtifact(request: ArtifactCreateRequest): Promise<Artifact> {
  return api.post<Artifact>("/api/v1/artifacts", request);
}

export async function getArtifact(artifactId: string): Promise<Artifact> {
  return api.get<Artifact>(`/api/v1/artifacts/${artifactId}`);
}

export async function getArtifactVersion(
  artifactId: string,
  version: number
): Promise<{ version: number; created_at: string; content?: string; path?: string; metadata: Record<string, any> }> {
  return api.get(`/api/v1/artifacts/${artifactId}/versions/${version}`);
}

export async function addArtifactVersion(
  artifactId: string,
  request: ArtifactAddVersionRequest
): Promise<Artifact> {
  return api.post(`/api/v1/artifacts/${artifactId}/versions`, request);
}

export async function restoreArtifactVersion(
  artifactId: string,
  version: number
): Promise<Artifact> {
  return api.post(`/api/v1/artifacts/${artifactId}/restore/${version}`);
}

export async function deleteArtifact(artifactId: string): Promise<{ deleted: boolean }> {
  return api.delete(`/api/v1/artifacts/${artifactId}`);
}
