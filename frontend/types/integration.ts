export interface UnifiedEvidence {
  id: string;
  source: string;
  type: string;
  content: string;
  confidence: number;
  strength: number;
  direction?: string;
  category?: string;
  claim_id?: string;
  contradicting_ids?: string[];
  metadata?: Record<string, unknown>;
  created_at: string;
}

export interface IntegrationResult {
  workflow_id: string;
  workflow_type: string;
  success: boolean;
  result: Record<string, unknown>;
  evidences: UnifiedEvidence[];
  reasoning_chain: string[];
  knowledge_updates: Array<{
    entity_id: string;
    action: string;
    domain: string;
  }>;
  error?: string;
  started_at: string;
  completed_at: string;
  latency_ms: number;
}

export interface IntegrationResponse {
  success: boolean;
  data?: IntegrationResult;
  error?: string;
}

export interface TradingIntegrationRequest {
  symbol: string;
  timeframes?: string[];
  exchange?: string;
}

export interface NetworkDesignReviewRequest {
  topology_description: string;
  requirements?: string;
}

export interface SelfImprovementRequest {
  project_path: string;
  analysis_type?: string;
}
