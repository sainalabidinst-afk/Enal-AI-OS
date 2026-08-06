import { create } from "zustand";
import { CognitiveLayer, type ThinkingMode, type ReasoningStep, type CognitiveState, type MetaCognitiveFlags } from "@/types/cognitive";

interface CognitiveStore extends CognitiveState {
  thinkingHistory: ThinkingMode[];
  layerTransitionCount: Record<CognitiveLayer, number>;
  setLayer: (layer: CognitiveLayer) => void;
  setActiveCapability: (capability: string | null) => void;
  setExecutionContext: (context: CognitiveState["execution_context"]) => void;
  startThinkingMode: (mode: Omit<ThinkingMode, "started_at">) => void;
  completeThinkingMode: () => void;
  addReasoningStep: (step: Omit<ReasoningStep, "step_id">) => void;
  setMetaCognitiveFlags: (flags: Partial<MetaCognitiveFlags>) => void;
  reset: () => void;
}

const initialMetaCognitiveFlags: MetaCognitiveFlags = {
  uncertainty: false,
  alternatives_considered: 0,
  confidence_trend: "stable",
  last_reflection: null,
};

const initialState = {
  current_layer: CognitiveLayer.REACTIVE,
  active_capability: null,
  execution_context: null,
  thinking_mode: null,
  meta_cognitive_flags: initialMetaCognitiveFlags,
  thinkingHistory: [] as ThinkingMode[],
  layerTransitionCount: {
    [CognitiveLayer.REACTIVE]: 0,
    [CognitiveLayer.ANALYTICAL]: 0,
    [CognitiveLayer.META_COGNITIVE]: 0,
  },
};

export const useCognitiveStore = create<CognitiveStore>()((set, get) => ({
  ...initialState,

  setLayer: (layer: CognitiveLayer) => {
    const current = get().current_layer;
    if (current !== layer) {
      set((state) => ({
        current_layer: layer,
        layerTransitionCount: {
          ...state.layerTransitionCount,
          [layer]: state.layerTransitionCount[layer] + 1,
        },
      }));
    }
  },

  setActiveCapability: (capability: string | null) => {
    set({ active_capability: capability });
  },

  setExecutionContext: (context: CognitiveState["execution_context"]) => {
    set({ execution_context: context });
  },

  startThinkingMode: (mode: Omit<ThinkingMode, "started_at">) => {
    const thinkingMode: ThinkingMode = {
      ...mode,
      started_at: new Date().toISOString(),
    };
    set((state) => ({
      thinking_mode: thinkingMode,
      thinkingHistory: [...state.thinkingHistory, thinkingMode],
    }));
  },

  completeThinkingMode: () => {
    set((state) => {
      if (!state.thinking_mode) return state;
      const completed: ThinkingMode = {
        ...state.thinking_mode,
        completed_at: new Date().toISOString(),
      };
      return {
        thinking_mode: completed,
        thinkingHistory: state.thinkingHistory.map((t) =>
          t.started_at === completed.started_at ? completed : t
        ),
      };
    });
  },

  addReasoningStep: (step: Omit<ReasoningStep, "step_id">) => {
    const stepId = `step-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    const newStep: ReasoningStep = { ...step, step_id: stepId };
    set((state) => {
      if (!state.thinking_mode) return state;
      return {
        thinking_mode: {
          ...state.thinking_mode,
          reasoning_chain: [...state.thinking_mode.reasoning_chain, newStep],
        },
      };
    });
  },

  setMetaCognitiveFlags: (flags: Partial<MetaCognitiveFlags>) => {
    set((state) => ({
      meta_cognitive_flags: { ...state.meta_cognitive_flags, ...flags },
    }));
  },

  reset: () => set(initialState),
}));
