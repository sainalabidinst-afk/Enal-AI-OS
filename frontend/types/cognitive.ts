export enum CognitiveLayer {
  REACTIVE = "reactive",
  ANALYTICAL = "analytical",
  META_COGNITIVE = "meta_cognitive",
}

export interface ThinkingMode {
  mode: CognitiveLayer;
  confidence: number;
  alternatives: string[];
  reasoning_chain: ReasoningStep[];
  started_at: string;
  completed_at?: string;
}

export interface ReasoningStep {
  step_id: string;
  service: string;
  input: Record<string, any>;
  output: Record<string, any>;
  duration_ms: number;
  status: "pending" | "running" | "completed" | "failed";
}

export interface CognitiveState {
  current_layer: CognitiveLayer;
  active_capability: string | null;
  execution_context: ExecutionContext | null;
  thinking_mode: ThinkingMode | null;
  meta_cognitive_flags: MetaCognitiveFlags;
}

export interface ExecutionContext {
  execution_id: string;
  goal: string;
  workspace_id: string;
  phase: string;
  progress: number;
}

export interface MetaCognitiveFlags {
  uncertainty: boolean;
  alternatives_considered: number;
  confidence_trend: "increasing" | "stable" | "decreasing";
  last_reflection: string | null;
}

export type MemoryLayerType =
  | "working"
  | "conversation"
  | "knowledge"
  | "long_term"
  | "episodic"
  | "session"
  | "project";

export interface MemoryLayerData {
  type: MemoryLayerType;
  name: string;
  description: string;
  capacity: number;
  used: number;
  utilization: number;
  last_access: string;
  color: string;
}

export type InsightPriority = "high" | "medium" | "low";

export interface LearningInsight {
  id: string;
  text: string;
  priority: InsightPriority;
  source_capability: string;
  created_at: string;
  applied?: boolean;
}

export type CapabilityRunStatus = "ready" | "running" | "idle" | "failed" | "pending";

export interface CapabilityStatusInfo {
  id: string;
  name: string;
  domain: string;
  status: CapabilityRunStatus;
  last_active: string;
  success_rate: number;
  executions: number;
}

export interface CrossCapabilityMetric {
  capability_id: string;
  metric: string;
  value: number;
}

export interface OrchestrationState {
  capabilities: CapabilityStatusInfo[];
  active_execution: string | null;
  cross_capability_metrics: CrossCapabilityMetric[];
  last_sync: string;
}
