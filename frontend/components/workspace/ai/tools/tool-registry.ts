import type { ToolDefinition, ToolResult } from "./tool-types";

class ToolRegistryImpl {
  private tools = new Map<string, ToolDefinition>();

  register(tool: ToolDefinition) {
    this.tools.set(tool.id, tool);
  }

  unregister(toolId: string) {
    this.tools.delete(toolId);
  }

  get(toolId: string) {
    return this.tools.get(toolId);
  }

  getAll() {
    return Array.from(this.tools.values());
  }

  async execute(toolId: string, params: Record<string, unknown>): Promise<ToolResult> {
    const tool = this.tools.get(toolId);
    if (!tool) {
      return { success: false, error: `Tool ${toolId} not found` };
    }
    return tool.execute(params);
  }
}

export const toolRegistry = new ToolRegistryImpl();

