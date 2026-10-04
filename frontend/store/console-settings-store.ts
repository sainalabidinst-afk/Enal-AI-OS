"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface ConsolePreferences {
  defaultProvider: string;
  defaultModel: string;
  autoTranscribe: boolean;
  alertLatencyMs: number;
  alertErrorRate: number;
  alertThrottle: boolean;
  rateLimitPerMinute: number;
  sandboxIsolation: boolean;
  guardrails: Record<string, boolean>;
  integrations: Record<string, boolean>;
  tradingAlertConfidenceThreshold: number;
  updatedAt: string | null;
}

interface ConsolePreferencesActions {
  set: <K extends keyof ConsolePreferences>(key: K, value: ConsolePreferences[K]) => void;
  toggleGuardrail: (name: string) => void;
  toggleIntegration: (name: string) => void;
  reset: () => void;
}

const DEFAULTS: ConsolePreferences = {
  defaultProvider: "",
  defaultModel: "",
  autoTranscribe: true,
  alertLatencyMs: 500,
  alertErrorRate: 5,
  alertThrottle: true,
  rateLimitPerMinute: 120,
  sandboxIsolation: true,
  guardrails: {},
  integrations: {},
  tradingAlertConfidenceThreshold: 80,
  updatedAt: null,
};

export const useConsolePreferences = create<ConsolePreferences & ConsolePreferencesActions>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      set: (key, value) => set({ [key]: value, updatedAt: new Date().toISOString() } as never),
      toggleGuardrail: (name) =>
        set((state) => ({
          guardrails: { ...state.guardrails, [name]: !state.guardrails[name] },
          updatedAt: new Date().toISOString(),
        })),
      toggleIntegration: (name) =>
        set((state) => ({
          integrations: { ...state.integrations, [name]: !state.integrations[name] },
          updatedAt: new Date().toISOString(),
        })),
      reset: () => set({ ...DEFAULTS, updatedAt: new Date().toISOString() }),
    }),
    { name: "ecp-console-preferences" }
  )
);