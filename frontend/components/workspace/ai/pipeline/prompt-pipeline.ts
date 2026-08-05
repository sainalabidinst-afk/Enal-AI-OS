import type { PromptPipelineInput, PromptPipelineOutput } from "./pipeline-types";

export class PromptPipelineBuilder {
  build(input: PromptPipelineInput): PromptPipelineOutput {
    const systemPrompt = this.buildSystemPrompt(input);
    const prompt = this.buildUserPrompt(input);
    const context = this.buildContext(input);

    return {
      prompt,
      systemPrompt,
      context,
    };
  }

  private buildSystemPrompt(input: PromptPipelineInput): string {
    const capabilityName = input.capabilityContext.capabilityId;
    const toolsList = input.tools.map((t) => `- ${t.name}: ${t.description}`).join("\n");

    return `You are an AI assistant for ${capabilityName} workspace.

You have access to the following tools:
${toolsList}

When answering:
1. Use tools when you need data
2. Provide structured evidence
3. Be concise and actionable
4. Show your reasoning

Response format:
- Summary: Brief conclusion
- Evidence: Supporting data
- Reasoning: Why you reached this conclusion
- Confidence: How confident you are (0-100%)
- Alternative: Other possibilities to consider`;
  }

  private buildUserPrompt(input: PromptPipelineInput): string {
    const context = input.capabilityContext;
    const memory = input.memory;

    let prompt = `User: ${input.userMessage}\n\n`;

    if (context.symbol) {
      prompt += `Current Symbol: ${context.symbol}\n`;
    }
    if (context.timeframe) {
      prompt += `Current Timeframe: ${context.timeframe}\n`;
    }

    if (memory.lastSymbol && memory.lastSymbol !== context.symbol) {
      prompt += `Previous Symbol: ${memory.lastSymbol}\n`;
    }

    if (memory.pinnedAnalysis) {
      prompt += `Pinned Analysis: ${memory.pinnedAnalysis}\n`;
    }

    return prompt;
  }

  private buildContext(input: PromptPipelineInput): Record<string, unknown> {
    return {
      capabilityId: input.capabilityContext.capabilityId,
      workspaceId: input.capabilityContext.workspaceId,
      symbol: input.capabilityContext.symbol,
      timeframe: input.capabilityContext.timeframe,
      state: input.capabilityContext.state,
      tools: input.tools.map((t) => t.id),
    };
  }
}

export const promptPipelineBuilder = new PromptPipelineBuilder();

