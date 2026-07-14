export interface ArtifactVersion {
  version: number;
  created_at: string;
  content?: string;
  path?: string;
  metadata: Record<string, any>;
}

export interface Artifact {
  id: string;
  workspace_id: string;
  name: string;
  type: string;
  description?: string;
  current_version: number;
  versions: ArtifactVersion[];
  created_at: string;
  updated_at: string;
}

export interface ArtifactCreateRequest {
  workspace_id: string;
  name: string;
  type: string;
  description?: string;
  content?: string;
  metadata?: Record<string, any>;
}

export interface ArtifactAddVersionRequest {
  content?: string;
  metadata?: Record<string, any>;
}
