import { create } from "zustand";
import type { ExecutionSession, ExecutionPhase, ExecutionArtifact, ExecutionStatus } from "@/types/execution";
import {
  startExecution as apiStartExecution,
  getExecution,
  listExecutions,
  addExecutionPhase,
  updateExecutionPhase,
  updateExecutionProgress,
  addExecutionLog,
  getExecutionLogs,
  cancelExecution,
  deleteExecution,
  listExecutionArtifacts,
} from "@/services/execution";

interface ExecutionState {
  executions: Record<string, ExecutionSession>;
  activeExecutionId: string | null;
  logs: Array<Record<string, any>>;
  isLoading: boolean;
  error: string | null;
  isRunning: (id: string) => boolean;
  startExecution: (goal: string, workspaceId: string, conversationId?: string) => Promise<ExecutionSession | null>;
  refreshExecution: (executionId: string) => Promise<void>;
  loadExecutions: (workspaceId?: string) => Promise<void>;
  cancelExecution: (executionId: string) => Promise<void>;
  deleteExecution: (executionId: string) => Promise<void>;
  appendPhase: (executionId: string, phase: { name: string }) => Promise<void>;
  updatePhase: (executionId: string, phaseId: string, updates: { status?: ExecutionStatus; progress?: number }) => Promise<void>;
  updateProgress: (executionId: string, progress: number, etaSeconds?: number) => Promise<void>;
  appendLog: (executionId: string, log: { message: string; level?: string; metadata?: Record<string, any> }) => Promise<void>;
  loadLogs: (executionId: string) => Promise<void>;
  loadArtifacts: (executionId: string) => Promise<ExecutionArtifact[]>;
  setActiveExecution: (executionId: string | null) => void;
  setError: (error: string | null) => void;
}

export const useExecutionStore = create<ExecutionState>()((set, get) => ({
  executions: {},
  activeExecutionId: null,
  logs: [],
  isLoading: false,
  error: null,

  isRunning: (id: string) => {
    const execution = get().executions[id];
    if (!execution) return false;
    return ["pending", "planning", "running", "waiting_approval", "paused"].includes(execution.status);
  },

  startExecution: async (goal: string, workspaceId: string, conversationId?: string) => {
    set({ isLoading: true, error: null });
    try {
      const result = await apiStartExecution({ goal, workspace_id: workspaceId, conversation_id: conversationId });
      const execution = result.execution;
      if (execution) {
        set((state) => ({
          executions: { ...state.executions, [execution.id]: execution },
          activeExecutionId: execution.id,
          isLoading: false,
        }));
      }
      return execution;
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to start execution", isLoading: false });
      return null;
    }
  },

  refreshExecution: async (executionId: string) => {
    try {
      const execution = await getExecution(executionId);
      set((state) => ({
        executions: { ...state.executions, [executionId]: execution },
      }));
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load execution" });
    }
  },

  loadExecutions: async (workspaceId?: string) => {
    set({ isLoading: true, error: null });
    try {
      const executions = await listExecutions(workspaceId);
      const map: Record<string, ExecutionSession> = {};
      for (const execution of executions) {
        map[execution.id] = execution;
      }
      set({ executions: map, isLoading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load executions", isLoading: false });
    }
  },

  cancelExecution: async (executionId: string) => {
    await cancelExecution(executionId);
    await get().refreshExecution(executionId);
  },

  deleteExecution: async (executionId: string) => {
    await deleteExecution(executionId);
    set((state) => {
      const { [executionId]: _, ...rest } = state.executions;
      return {
        executions: rest,
        activeExecutionId: state.activeExecutionId === executionId ? null : state.activeExecutionId,
      };
    });
  },

  appendPhase: async (executionId: string, phase: { name: string }) => {
    await addExecutionPhase(executionId, phase);
    await get().refreshExecution(executionId);
  },

  updatePhase: async (executionId: string, phaseId: string, updates: { status?: ExecutionStatus; progress?: number }) => {
    await updateExecutionPhase(executionId, phaseId, updates);
    await get().refreshExecution(executionId);
  },

  updateProgress: async (executionId: string, progress: number, eta_seconds?: number) => {
    await updateExecutionProgress(executionId, { progress, eta_seconds });
    await get().refreshExecution(executionId);
  },

  appendLog: async (executionId: string, log: { message: string; level?: string; metadata?: Record<string, any> }) => {
    await addExecutionLog(executionId, log);
    await get().loadLogs(executionId);
  },

  loadLogs: async (executionId: string) => {
    try {
      const data = await getExecutionLogs(executionId);
      set({ logs: data.logs || [] });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load logs" });
    }
  },

  loadArtifacts: async (executionId: string) => {
    return listExecutionArtifacts(executionId);
  },

  setActiveExecution: (executionId: string | null) => set({ activeExecutionId: executionId }),
  setError: (error: string | null) => set({ error }),
}));
