import { create } from "zustand";
import { CognitiveLayer, type ThinkingMode, type ReasoningStep, type CognitiveState, type MetaCognitiveFlags, type MemoryLayerData, type LearningInsight, type OrchestrationState, type CapabilityRunStatus } from "@/types/cognitive";

interface CognitiveStore extends CognitiveState {
  thinkingHistory: ThinkingMode[];
  layerTransitionCount: Record<CognitiveLayer, number>;
  memoryLayers: MemoryLayerData[];
  learningInsights: LearningInsight[];
  orchestration: OrchestrationState;
  setLayer: (layer: CognitiveLayer) => void;
  setActiveCapability: (capability: string | null) => void;
  setExecutionContext: (context: CognitiveState["execution_context"]) => void;
  startThinkingMode: (mode: Omit<ThinkingMode, "started_at">) => void;
  completeThinkingMode: () => void;
  addReasoningStep: (step: Omit<ReasoningStep, "step_id">) => void;
  setMetaCognitiveFlags: (flags: Partial<MetaCognitiveFlags>) => void;
  setMemoryLayers: (layers: MemoryLayerData[]) => void;
  updateMemoryLayer: (type: MemoryLayerData["type"], patch: Partial<MemoryLayerData>) => void;
  setLearningInsights: (insights: LearningInsight[]) => void;
  addLearningInsight: (insight: Omit<LearningInsight, "id" | "created_at">) => void;
  dismissInsight: (id: string) => void;
  applyInsight: (id: string) => void;
  setOrchestration: (data: OrchestrationState) => void;
  setCapabilityStatus: (id: string, status: CapabilityRunStatus) => void;
  reset: () => void;
}

const initialMetaCognitiveFlags: MetaCognitiveFlags = {
  uncertainty: false,
  alternatives_considered: 0,
  confidence_trend: "stable",
  last_reflection: null,
};

const MEMORY_LAYERS: MemoryLayerData[] = [
  { type: "working", name: "Working Memory", description: "Active context and immediate goals", capacity: 100, used: 0, utilization: 0, last_access: "", color: "#3b82f6" },
  { type: "conversation", name: "Conversation", description: "Current session dialogue history", capacity: 500, used: 0, utilization: 0, last_access: "", color: "#10b981" },
  { type: "knowledge", name: "Knowledge", description: "Learned facts and domain rules", capacity: 5000, used: 0, utilization: 0, last_access: "", color: "#f59e0b" },
  { type: "long_term", name: "Long-term", description: "Persistent accumulated memories", capacity: 10000, used: 0, utilization: 0, last_access: "", color: "#8b5cf6" },
  { type: "episodic", name: "Episodic", description: "Past execution episodes and outcomes", capacity: 2000, used: 0, utilization: 0, last_access: "", color: "#ec4899" },
  { type: "session", name: "Session", description: "Short-lived per-task scratch data", capacity: 200, used: 0, utilization: 0, last_access: "", color: "#06b6d4" },
  { type: "project", name: "Project", description: "Project-scoped preferences and conventions", capacity: 1000, used: 0, utilization: 0, last_access: "", color: "#a16207" },
];

const initialOrchestration: OrchestrationState = {
  capabilities: [],
  active_execution: null,
  cross_capability_metrics: [],
  last_sync: "",
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
  memoryLayers: MEMORY_LAYERS,
  learningInsights: [] as LearningInsight[],
  orchestration: initialOrchestration,
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

  setMemoryLayers: (layers: MemoryLayerData[]) => {
    set({ memoryLayers: layers });
  },

  updateMemoryLayer: (type: MemoryLayerData["type"], patch: Partial<MemoryLayerData>) => {
    set((state) => ({
      memoryLayers: state.memoryLayers.map((l) => {
        if (l.type !== type) return l;
        const capacity = patch.capacity ?? l.capacity;
        const used = patch.used ?? l.used;
        const utilization = capacity > 0 ? used / capacity : l.utilization;
        return { ...l, ...patch, utilization };
      }),
    }));
  },

  setLearningInsights: (insights: LearningInsight[]) => {
    set({ learningInsights: insights });
  },

  addLearningInsight: (insight: Omit<LearningInsight, "id" | "created_at">) => {
    const newInsight: LearningInsight = {
      ...insight,
      id: `insight-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
      created_at: new Date().toISOString(),
    };
    set((state) => ({
      learningInsights: [newInsight, ...state.learningInsights],
    }));
  },

  dismissInsight: (id: string) => {
    set((state) => ({
      learningInsights: state.learningInsights.filter((i) => i.id !== id),
    }));
  },

  applyInsight: (id: string) => {
    set((state) => ({
      learningInsights: state.learningInsights.map((i) =>
        i.id === id ? { ...i, applied: true } : i
      ),
    }));
  },

  setOrchestration: (data: OrchestrationState) => {
    set({ orchestration: data });
  },

  setCapabilityStatus: (id: string, status: CapabilityRunStatus) => {
    set((state) => ({
      orchestration: {
        ...state.orchestration,
        capabilities: state.orchestration.capabilities.map((cap) =>
          cap.id === id ? { ...cap, status, last_active: new Date().toISOString() } : cap
        ),
      },
    }));
  },

  reset: () => set(initialState),
}));
