/**
 * Console API contracts.
 * Shapes mirror backend response payloads; the frontend never derives them.
 */

export type PackStatus =
  | "draft"
  | "testing"
  | "approved"
  | "rejected"
  | "registered"
  | "deprecated";

export interface GovernancePack {
  pack_id: string;
  name: string;
  domain: string;
  status: PackStatus;
  benchmark_score: number;
  coverage: number;
  tests_passed: number;
  tests_total: number;
  updated_at?: string;
  created_at?: string;
  metadata?: Record<string, unknown>;
}

export interface GovernancePackList {
  packs: GovernancePack[];
}

export interface AuditEntry {
  entry_id: string;
  actor: string;
  action: string;
  pack_id: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface AuditTrail {
  entries: AuditEntry[];
  count: number;
}

export interface QualityGateResult {
  pack_id: string;
  passed: boolean;
  benchmark_score: number;
  coverage: number;
  tests_passed: number;
  tests_total: number;
  test_pass_rate: number;
  min_benchmark_score: number;
  min_coverage: number;
  min_test_pass_rate: number;
}

export interface SandboxRecord {
  sandbox_id: string;
  pack_id: string;
  isolated: boolean;
  environment: string;
  allowed_operations: string[];
  blocked_operations: string[];
}

export type CapabilityState =
  | "loaded"
  | "unloaded"
  | "suspended"
  | "upgrading"
  | "error";

export type CapabilityHealth = "healthy" | "degraded" | "unhealthy";

export interface CapabilityVersionInfo {
  major: number;
  minor: number;
  patch: number;
  build: string;
  contract_version: string;
  display: string;
}

export interface CapabilityMetrics {
  execution_count: number;
  success_count: number;
  failure_count: number;
  success_rate: number;
  avg_latency_ms: number;
  last_executed_at: string | null;
  last_success_at: string | null;
  last_failure_at: string | null;
  last_error: string | null;
}

export interface CapabilityLifecycleRecord {
  id: string;
  name: string;
  category: string;
  state: CapabilityState;
  health: CapabilityHealth;
  version: CapabilityVersionInfo;
  dependencies: string[];
  dependents: string[];
  metrics: CapabilityMetrics;
  loaded_at: string | null;
  updated_at: string | null;
  metadata: Record<string, unknown>;
}

export interface CapabilityLifecycleSummary {
  total: number;
  loaded: number;
  unloaded: number;
  suspended: number;
  upgrading: number;
  error: number;
  healthy: number;
  degraded: number;
  unhealthy: number;
}

export interface CapabilityLifecycleResponse {
  capabilities: CapabilityLifecycleRecord[];
  summary: CapabilityLifecycleSummary;
}

export interface CapabilityDependencies {
  capability_id: string;
  dependencies: string[];
  dependents: string[];
  satisfied: boolean;
  missing: string[];
}

export interface CapabilityCompatibility {
  capability_id: string;
  required_contract: string;
  compatible: boolean;
  message: string;
}

export interface BenchmarkCaseSummary {
  case_id: string;
  vendor: string;
  filename: string;
  category: string;
  tags: string[];
}

export interface BenchmarkSuite {
  suite_id: string;
  name: string;
  case_count: number;
  cases: BenchmarkCaseSummary[];
}

export interface CapabilityBreakdown {
  vendor: string;
  parser: number;
  reasoning: number;
  evidence: number;
  compliance: number;
  executive_report: number;
  total: number;
}

export interface BenchmarkResult {
  case_id: string;
  passed: boolean;
  score: number;
  findings: number;
  risk_score: number;
  confidence: number;
  capability_score: number;
  capability_breakdown: CapabilityBreakdown;
  details: Record<string, unknown>;
}

export interface BenchmarkSummary {
  total: number;
  passed: number;
  failed: number;
  avg_score: number;
  avg_capability_score: number;
}

export interface BenchmarkRunResult {
  suite_id: string;
  results: BenchmarkResult[];
  summary: BenchmarkSummary;
}

export interface VendorCapabilityScore {
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

export interface CapabilityScores {
  capabilities: Record<string, VendorCapabilityScore>;
}

export interface CceStatus {
  status: "ok" | "no_data" | "error";
  message?: string;
  run_id?: string;
  timestamp?: string;
  total_cases?: number;
  passed_cases?: number;
  failed_cases?: number;
  avg_score?: number;
  avg_capability_score?: number;
  regression_count?: number;
  regressions?: unknown[];
  capabilities?: Record<string, unknown>;
  calibration?: Record<string, unknown>;
}

export interface MarketplaceTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  tags: string[];
  type: string;
  config: Record<string, unknown>;
  author: string;
  version: string;
  rating: number;
  clones: number;
  created_at: string;
  updated_at: string;
}

export interface MarketplaceListing {
  id: string;
  agent_id: string;
  name: string;
  description: string;
  category: string;
  author: string;
  tags: string[];
  rating: number;
  status: string;
  created_at: string;
}

export interface CloneReceipt {
  id: string;
  agent_id: string;
  project: string;
  cloned_at: string;
}

export interface ListingAnalytics {
  agent_id: string;
  clones: number;
  views: number;
}

export interface EvaluationDimensionScore {
  dimension: string;
  score: number;
  weight: number;
  feedback: string;
}

export interface EvaluationResult {
  score: number;
  dimensions: EvaluationDimensionScore[];
  vendor_violations: unknown[];
  insights: string[];
  feedback: string[];
  passed: boolean;
  threshold: number;
  case_id: string | null;
  scenario: string | null;
  vendor: string | null;
}

export interface EvaluationResultsResponse {
  results: EvaluationResult[];
  count: number;
}

export interface ScheduleJob {
  job_id: string;
  cron: string;
  next_run: string | null;
  last_run: string | null;
}

export interface ModelProviderStatus {
  name?: string;
  provider?: string;
  available?: boolean;
  healthy?: boolean;
  status?: string;
  models?: string[];
  latency_ms?: number;
  detail?: string;
}

export interface VoiceProviderInfo {
  stt_provider: string;
  tts_provider: string;
  tts_voice: string;
  tts_voice_name: string;
  tts_voice_gender: string;
  tts_voice_tone: string;
  tts_voice_attitude: string;
  stt_language: string;
  supported_languages: string[];
}

export interface VoiceTranscription {
  text: string;
  confidence: number;
  language: string;
  duration_ms: number;
  alternatives?: string[] | null;
}

export interface ServiceHealth {
  status: string;
  service: string;
  version: string;
}

export interface ChatMessagePayload {
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
  conversation_id?: string;
  latency_ms?: number;
}

export interface ChatResponse {
  conversation_id?: string;
  message?: string;
  response?: string;
  content?: string;
  role?: string;
  latency_ms?: number;
  model?: string;
}