export interface WorkspaceFile {
  filename: string;
  path: string;
  size: number;
  uploaded_at: string;
  metadata?: Record<string, any>;
}

export interface WorkspaceMemory {
  [key: string]: any;
}

export interface Workspace {
  id: string;
  name: string;
  description?: string;
  conversation_ids: string[];
  execution_ids: string[];
  artifact_ids: string[];
  files: WorkspaceFile[];
  memory: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceApiResponse {
  id: string;
  name: string;
  description?: string;
  conversation_ids: string[];
  execution_ids: string[];
  artifact_ids: string[];
  files: Array<Record<string, any>>;
  memory: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceCreateRequest {
  name: string;
  description?: string;
}

export interface WorkspaceAddFileRequest {
  filename: string;
  path: string;
  size: number;
  metadata?: Record<string, any>;
}

export interface WorkspaceMemoryRequest {
  key: string;
  value: any;
}
