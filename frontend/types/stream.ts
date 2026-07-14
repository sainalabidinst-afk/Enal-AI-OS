export type StreamEventType =
  | "final"
  | "execution_started"
  | "phase"
  | "task"
  | "log"
  | "artifact"
  | "progress"
  | "execution_complete"
  | "error";

export interface StreamEvent {
  type: StreamEventType;
  [key: string]: any;
}

export interface FinalEvent {
  type: "final";
  message: string;
  conversation_id: string;
  domain?: string;
  intent?: Record<string, any>;
}

export interface ExecutionStartedEvent {
  type: "execution_started";
  execution_id: string;
  goal: string;
}

export interface PhaseEvent {
  type: "phase";
  phase_id: string;
  name: string;
  status: string;
}

export interface TaskEvent {
  type: "task";
  task_id: string;
  name: string;
  status: string;
}

export interface LogEvent {
  type: "log";
  level: string;
  message: string;
}

export interface ArtifactEvent {
  type: "artifact";
  artifact_id: string;
  name: string;
  artifact_type: string;
}

export interface ProgressEvent {
  type: "progress";
  progress: number;
  eta_seconds?: number;
}

export interface ExecutionCompleteEvent {
  type: "execution_complete";
  execution_id: string;
  progress: number;
}

export interface ErrorEvent {
  type: "error";
  message: string;
}
