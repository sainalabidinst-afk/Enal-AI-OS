export interface BenchmarkResult {
  case_id: string;
  passed: boolean;
  score: number;
  findings: string[];
  risk_score: number;
  confidence: number;
  capability_score: number;
  capability_breakdown: {
    vendor: string;
    parser: number;
    reasoning: number;
    evidence: number;
    compliance: number;
    executive_report: number;
    total: number;
  };
}

export interface BenchmarkSummary {
  total: number;
  passed: number;
  failed: number;
  avg_score: number;
  avg_capability_score: number;
}

export interface BenchmarkResponse {
  suite_id: string;
  results: BenchmarkResult[];
  summary: BenchmarkSummary;
}

export interface BenchmarkDashboardEntry {
  vendor: string;
  cases: number;
  passed: number;
  failed: number;
  avg_score: number;
  avg_capability_score: number;
  parser: number;
  reasoning: number;
  evidence: number;
  compliance: number;
  executive_report: number;
}
