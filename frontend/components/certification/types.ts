export interface CapabilityCertificate {
  schemaVersion: string;
  capabilityId: string;
  capabilityName: string;
  version: string;
  contractVersion: string;
  certificationLevel: "Certified" | "Provisional" | "Experimental" | "Deprecated";
  grade: "A" | "B" | "C" | "D" | "F";
  overallScore: number;
  status: "Active" | "Suspended" | "Revoked" | "Expired";
  audit: {
    score: number;
    passed: boolean;
    completedAt: string;
    findings: {
      critical: number;
      minor: number;
      correctiveActions: string[];
    };
  };
  benchmark: {
    score: number;
    passed: boolean;
    completedAt: string;
    metrics: {
      executionLatencyP50: number;
      executionLatencyP95: number;
      executionLatencyP99: number;
      memoryUsageMB: number;
      throughputPerSecond: number;
      determinismScore: number;
      repeatabilityScore: number;
      stabilityScore: number;
      successRate: number;
    };
  };
  goldenTests: {
    score: number;
    passed: boolean;
    completedAt: string;
    categories: GoldenTestCategory[];
  };
  realCases: {
    score: number;
    passed: boolean;
    completedAt: string;
    scenarios: RealCaseScenario[];
  };
  productionReadiness: {
    score: number;
    passed: boolean;
    completedAt: string;
    checks: ProductionReadinessCheck[];
  };
  certificationDate: string;
  reviewer: string;
  expirationDate: string;
}

export interface GoldenTestCategory {
  name: "Functional" | "Edge Cases" | "Invalid Input" | "Regression" | "Explainability" | "Performance" | "Contract Compliance";
  total: number;
  passed: number;
  failed: number;
  skipped: number;
}

export interface RealCaseScenario {
  name: string;
  status: "passed" | "failed" | "partial" | "skipped";
  score: number;
  notes: string;
}

export interface ProductionReadinessCheck {
  name: "Interoperability" | "Dependency" | "Lifecycle" | "Telemetry" | "Compatibility" | "Deployment";
  status: "passed" | "failed" | "partial" | "skipped";
  notes: string;
}

export interface CertificationDashboard {
  generatedAt: string;
  totalCapabilities: number;
  summary: {
    certified: number;
    provisional: number;
    experimental: number;
    active: number;
    averageScore: number;
    gradeDistribution: Record<string, number>;
  };
  capabilities: Array<{
    capabilityId: string;
    capabilityName: string;
    grade: string;
    certificationLevel: string;
    overallScore: number;
    status: string;
    certificationDate: string;
    expirationDate: string;
  }>;
}
