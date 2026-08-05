import type { EvidencePayload, EvidenceItem } from "../evidence/evidence-types";

export class EvidenceBuilder {
  static build(options: {
    summary: string;
    items: EvidenceItem[];
    reasoning: string;
    confidence: number;
    alternative?: string;
    nextAction?: string;
  }): EvidencePayload {
    return {
      summary: options.summary,
      evidence: options.items,
      reasoning: options.reasoning,
      confidence: Math.min(Math.max(options.confidence, 0), 100),
      alternative: options.alternative,
      nextAction: options.nextAction,
    };
  }

  static fromToolResult(toolName: string, result: { success: boolean; data?: unknown; error?: string }): EvidenceItem {
    return {
      type: "tool",
      label: toolName,
      value: result.success ? String(result.data ?? "No data") : result.error ?? "Unknown error",
      source: toolName,
    };
  }

  static fromData(label: string, value: string | number | boolean): EvidenceItem {
    return {
      type: "data",
      label,
      value,
    };
  }

  static fromIndicator(label: string, value: string | number | boolean): EvidenceItem {
    return {
      type: "indicator",
      label,
      value,
    };
  }

  static fromNews(label: string, value: string | number | boolean, source?: string): EvidenceItem {
    return {
      type: "news",
      label,
      value,
      source,
    };
  }

  static fromKnowledge(label: string, value: string | number | boolean): EvidenceItem {
    return {
      type: "knowledge",
      label,
      value,
    };
  }
}

