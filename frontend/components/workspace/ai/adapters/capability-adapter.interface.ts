import type { ToolDefinition, ToolResult } from "../tools/tool-types";
import type { EvidencePayload } from "../evidence/evidence-types";

export interface CapabilityContext {
  capabilityId: string;
  workspaceId: string;
  symbol?: string;
  timeframe?: string;
  state: Record<string, unknown>;
}

export interface CapabilityAdapter {
  capabilityId: string;

  provideContext(): Promise<CapabilityContext>;

  provideTools(): Promise<ToolDefinition[]>;

  provideKnowledge(query: string): Promise<EvidencePayload>;
}

