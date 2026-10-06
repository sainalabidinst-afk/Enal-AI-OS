export interface ADR {
  id: string;
  title: string;
  status: 'draft' | 'accepted' | 'rejected' | 'superseded';
  created_at: string;
  updated_at: string;
  content?: string;
}

export interface QualityGateSummary {
  gate_id: string;
  pack_id: string;
  status: 'pass' | 'fail';
  benchmark_score: number;
  coverage: number;
  test_pass_rate: number;
}

export interface GovernanceStatus {
  total_packs: number;
  registered_packs: number;
  approved_packs: number;
  deprecated_packs: number;
}
