export interface PackRecord {
  pack_id: string;
  name: string;
  domain: string;
  status: 'draft' | 'testing' | 'approved' | 'rejected' | 'registered' | 'deprecated';
  benchmark_score?: number;
  coverage?: number;
  tests_passed?: number;
  tests_total?: number;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface QualityGate {
  gate_id: string;
  pack_id: string;
  min_benchmark_score: number;
  min_coverage: number;
  min_test_pass_rate: number;
  passed: boolean;
}

export interface AuditEntry {
  id: string;
  action: string;
  user?: string;
  pack_id?: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}
