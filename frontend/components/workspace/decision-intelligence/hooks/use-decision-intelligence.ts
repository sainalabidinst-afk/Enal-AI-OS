import { useMemo } from "react";
import { useDecisionHistoryStore } from "../stores/decision-history-store";
import { decisionEngine } from "../engine/decision-engine";
import { ExplainabilityBuilder } from "../explainability/explainability-builder";
import type { DecisionRequest, DecisionOutcome, ExplainabilityChain } from "../models/decision-models";

export function useDecisionIntelligence() {
  const addEntry = useDecisionHistoryStore((s) => s.addEntry);

  const evaluate = (request: DecisionRequest): DecisionOutcome => {
    const outcome = decisionEngine.evaluate(request);
    return outcome;
  };

  const evaluateWithHistory = (request: DecisionRequest, evidence: { label: string; value: string | number | boolean }[]): DecisionOutcome => {
    const outcome = decisionEngine.evaluate(request);
    addEntry(outcome, evidence);
    return outcome;
  };

  const getExplainability = (outcome: DecisionOutcome): ExplainabilityChain => {
    return ExplainabilityBuilder.build(outcome);
  };

  const formatExplainability = (chain: ExplainabilityChain): string => {
    return ExplainabilityBuilder.formatChain(chain);
  };

  return {
    evaluate,
    evaluateWithHistory,
    getExplainability,
    formatExplainability,
  };
}
