export interface ToolDefinition {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  execute: (params: Record<string, unknown>) => Promise<ToolResult>;
}

export interface ToolResult {
  success: boolean;
  data?: unknown;
  error?: string;
}

export interface ToolInvocation {
  toolId: string;
  params: Record<string, unknown>;
  result?: ToolResult;
  status: "pending" | "running" | "completed" | "failed";
}

