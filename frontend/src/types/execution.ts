export interface ExecutionSession {
  executionId: string;
  goal: string;
  status: string;
  progress: number;
  conversationId?: string;
  workspaceId?: string;
  phases: ExecutionPhase[];
  artifacts: Artifact[];
  logs: LogEntry[];
}

export interface ExecutionPhase {
  phaseId: string;
  name: string;
  status: string;
}

export interface Artifact {
  artifactId: string;
  name: string;
  type: string;
  path?: string;
}

export interface LogEntry {
  level: string;
  message: string;
  timestamp: string;
}
