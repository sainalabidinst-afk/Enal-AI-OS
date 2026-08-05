export interface EvidencePayload {
  summary: string;
  evidence: EvidenceItem[];
  reasoning: string;
  confidence: number;
  alternative?: string;
  nextAction?: string;
}

export interface EvidenceItem {
  type: "data" | "indicator" | "news" | "knowledge" | "tool";
  label: string;
  value: string | number | boolean;
  source?: string;
}

