export const QUALITY_GATES = {
  build: {
    frontendBuild: true,
    typescript: true,
    lint: true,
  },
  testing: {
    unitTestCoverage: 0.95,
    integrationTestCoverage: 0.95,
    e2eTestCoverage: 0.95,
  },
  performance: {
    maxRenderTime: 16,
    maxInteractionLatency: 100,
    maxAnalysisLatency: 500,
    maxDecisionLatency: 1000,
    maxMemoryUsage: 100 * 1024 * 1024,
  },
  security: {
    xssProtected: true,
    noSecretsExposed: true,
    cspCompatible: true,
  },
  accessibility: {
    wcagLevel: "AA",
    keyboardNavigable: true,
    screenReaderCompatible: true,
    contrastRatio: 4.5,
  },
} as const;

export interface QualityGateResults {
  build: boolean;
  testing: boolean;
  performance: boolean;
  security: boolean;
  accessibility: boolean;
}

export function validateQualityGates(results: Partial<QualityGateResults>): QualityGateResults {
  const validated = {} as QualityGateResults;

  for (const key of Object.keys(QUALITY_GATES) as (keyof typeof QUALITY_GATES)[]) {
    const gateResults = results[key];
    if (gateResults !== undefined) {
      validated[key] = gateResults as boolean;
    }
  }

  return validated;
}

export function isProductionReady(gateResults: QualityGateResults): boolean {
  return Object.values(gateResults).every((result) => result === true);
}
