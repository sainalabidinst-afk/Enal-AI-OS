import { create } from "zustand";
import type { DecisionHistoryEntry, DecisionOutcome } from "../models/decision-models";

interface DecisionHistoryState {
  entries: DecisionHistoryEntry[];
  addEntry: (outcome: DecisionOutcome, evidence: { label: string; value: string | number | boolean }[]) => void;
  resolveOutcome: (decisionId: string, success: boolean, feedback?: string) => void;
  getHistory: (capabilityId?: string) => DecisionHistoryEntry[];
  clearHistory: () => void;
}

export const useDecisionHistoryStore = create<DecisionHistoryState>((set, get) => ({
  entries: [],

  addEntry: (outcome, evidence) => {
    const entry: DecisionHistoryEntry = {
      decisionId: outcome.decisionId,
      capabilityId: outcome.capabilityId,
      action: outcome.action,
      confidence: outcome.confidence,
      evidence,
      timestamp: outcome.timestamp,
    };

    set((state) => ({
      entries: [entry, ...state.entries].slice(0, 100),
    }));
  },

  resolveOutcome: (decisionId, success, feedback) => {
    set((state) => ({
      entries: state.entries.map((entry) =>
        entry.decisionId === decisionId
          ? {
              ...entry,
              outcome: { success, feedback },
              resolvedAt: Date.now(),
            }
          : entry
      ),
    }));
  },

  getHistory: (capabilityId) => {
    if (!capabilityId) return get().entries;
    return get().entries.filter((e) => e.capabilityId === capabilityId);
  },

  clearHistory: () => set({ entries: [] }),
}));
