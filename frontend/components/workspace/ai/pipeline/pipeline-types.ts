import type { CapabilityContext } from "../adapters/capability-adapter.interface";
import type { ToolDefinition } from "../tools/tool-types";
import type { WorkspaceMemory } from "../memory/memory-types";
import type { EvidencePayload } from "../evidence/evidence-types";

export interface PromptPipelineInput {
  userMessage: string;
  capabilityContext: CapabilityContext;
  tools: ToolDefinition[];
  memory: WorkspaceMemory;
  knowledge: EvidencePayload;
}

export interface PromptPipelineOutput {
  prompt: string;
  systemPrompt: string;
  context: Record<string, unknown>;
}
