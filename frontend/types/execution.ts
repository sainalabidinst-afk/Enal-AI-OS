export type ExecutionStatus = "pending" | "planning" | "running" | "waiting_approval" | "paused" | "completed" | "failed" | "cancelled";

export interface ExecutionTask {
  id: string;
  name: string;
  status: ExecutionStatus;
  progress: number;
  dependencies: string[];
  result?: Record<string, any>;
  started_at?: string;
  completed_at?: string;
}

export interface ExecutionGraph {
  tasks: Record<string, ExecutionTask>;
  edges: Array<Record<string, string>>;
  entry_point?: string;
}

export interface ExecutionSession {
  id: string;
  goal: string;
  status: ExecutionStatus;
  progress: number;
  eta_seconds?: number;
  phases: Array<Record<string, any>>;
  artifacts: string[];
  logs: Array<Record<string, any>>;
  workspace_id?: string;
  conversation_id?: string;
  graph?: Record<string, any>;
  error?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface ExecutionPhase {
  id: string;
  name: string;
  status: ExecutionStatus;
  progress: number;
  tasks: Array<Record<string, any>>;
  started_at?: string;
  completed_at?: string;
}

export interface ExecutionArtifact {
  id: string;
  execution_id: string;
  name: string;
  type: string;
  content?: string;
  path?: string;
  version: number;
  created_at: string;
  metadata: Record<string, any>;
}
