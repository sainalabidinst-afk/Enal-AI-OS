'use client';

import { create } from 'zustand';

interface ExecutionPhase {
  phaseId: string;
  name: string;
  status: string;
}

interface Artifact {
  artifactId: string;
  name: string;
  type: string;
  path?: string;
}

interface LogEntry {
  level: string;
  message: string;
  timestamp: string;
}

interface ExecutionSession {
  executionId: string;
  goal: string;
  status: string;
  progress: number;
  conversationId?: string;
  workspaceId?: string;
  phases: ExecutionPhase[];
  artifacts: Artifact[];
  logs: LogEntry[];
}

interface ExecutionState {
  executions: ExecutionSession[];
  addExecution: (execution: ExecutionSession) => void;
  updatePhase: (executionId: string, phaseId: string, status: string) => void;
  addLog: (executionId: string, log: LogEntry) => void;
}

export const useExecutionStore = create<ExecutionState>((set) => ({
  executions: [],
  addExecution: (execution) => set((state) => ({ executions: [execution, ...state.executions] })),
  updatePhase: (executionId, phaseId, status) =>
    set((state) => ({
      executions: state.executions.map((ex) =>
        ex.executionId === executionId
          ? {
              ...ex,
              phases: ex.phases.map((p) => (p.phaseId === phaseId ? { ...p, status } : p)),
            }
          : ex
      ),
    })),
  addLog: (executionId, log) =>
    set((state) => ({
      executions: state.executions.map((ex) =>
        ex.executionId === executionId ? { ...ex, logs: [...ex.logs, log] } : ex
      ),
    })),
}));
