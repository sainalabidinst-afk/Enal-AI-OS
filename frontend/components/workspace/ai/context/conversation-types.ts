export interface ConversationThread {
  id: string;
  workspaceId: string;
  capabilityId: string;
  messages: AIMessage[];
  createdAt: number;
  updatedAt: number;
}

import type { ToolInvocation } from "../tools/tool-types";
import type { EvidencePayload } from "../evidence/evidence-types";
import type { DecisionOutcome } from "../../decision-intelligence/models/decision-models";
import type { ExplainabilityChain } from "../../decision-intelligence/models/decision-models";

export interface AIMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: number;
  evidence?: EvidencePayload;
  decision?: DecisionOutcome;
  explainability?: ExplainabilityChain;
  toolInvocations?: ToolInvocation[];
}
