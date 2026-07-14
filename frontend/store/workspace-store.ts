import { create } from "zustand";
import type { Workspace, WorkspaceFile } from "@/types/workspace";
import {
  listWorkspaces,
  createWorkspace as apiCreateWorkspace,
  getWorkspace as apiGetWorkspace,
  deleteWorkspace as apiDeleteWorkspace,
  listWorkspaceFiles,
  getWorkspaceFile,
  deleteWorkspaceFile,
  addWorkspaceFile,
  setWorkspaceMemory,
  getWorkspaceMemory,
} from "@/services/workspace";

interface WorkspaceState {
  workspaces: Workspace[];
  activeWorkspaceId: string | null;
  isLoading: boolean;
  error: string | null;
  loadWorkspaces: () => Promise<void>;
  createWorkspace: (name: string, description?: string) => Promise<Workspace>;
  setActiveWorkspace: (workspaceId: string | null) => Promise<void>;
  deleteWorkspace: (workspaceId: string) => Promise<void>;
  refreshWorkspace: (workspaceId: string) => Promise<void>;
  files: WorkspaceFile[];
  loadFiles: (workspaceId: string) => Promise<void>;
  createFile: (workspaceId: string, file: { filename: string; path: string; size: number; metadata?: Record<string, any> }) => Promise<void>;
  removeFile: (workspaceId: string, filename: string) => Promise<void>;
  memory: Record<string, any>;
  loadMemory: (workspaceId: string, key?: string) => Promise<void>;
  setMemory: (workspaceId: string, key: string, value: any) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useWorkspaceStore = create<WorkspaceState>()((set, get) => ({
  workspaces: [],
  activeWorkspaceId: null,
  isLoading: false,
  error: null,
  files: [],
  memory: {},

  loadWorkspaces: async () => {
    set({ isLoading: true, error: null });
    try {
      const workspaces = await listWorkspaces();
      set({ workspaces, isLoading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load workspaces", isLoading: false });
    }
  },

  createWorkspace: async (name: string, description?: string) => {
    const workspace = await apiCreateWorkspace({ name, description });
    set((state) => ({
      workspaces: [...state.workspaces, workspace],
    }));
    return workspace;
  },

  setActiveWorkspace: async (workspaceId: string | null) => {
    set({ activeWorkspaceId: workspaceId });
    if (workspaceId) {
      await get().refreshWorkspace(workspaceId);
    }
  },

  deleteWorkspace: async (workspaceId: string) => {
    await apiDeleteWorkspace(workspaceId);
    set((state) => ({
      workspaces: state.workspaces.filter((w) => w.id !== workspaceId),
      activeWorkspaceId: state.activeWorkspaceId === workspaceId ? null : state.activeWorkspaceId,
      files: state.activeWorkspaceId === workspaceId ? [] : state.files,
      memory: state.activeWorkspaceId === workspaceId ? {} : state.memory,
    }));
  },

  refreshWorkspace: async (workspaceId: string) => {
    try {
      const workspace = await apiGetWorkspace(workspaceId);
      set((state) => ({
        workspaces: state.workspaces.find((w) => w.id === workspaceId)
          ? state.workspaces.map((w) => (w.id === workspaceId ? workspace : w))
          : [...state.workspaces, workspace],
        activeWorkspaceId: workspaceId,
        files: workspace.files,
        memory: workspace.memory,
      }));
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load workspace", isLoading: false });
    }
  },

  loadFiles: async (workspaceId: string) => {
    try {
      const data = await listWorkspaceFiles(workspaceId);
      set({ files: (data.files || []) as WorkspaceFile[] });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load files", isLoading: false });
    }
  },

  createFile: async (workspaceId: string, file: { filename: string; path: string; size: number; metadata?: Record<string, any> }) => {
    await addWorkspaceFile(workspaceId, file);
    await get().refreshWorkspace(workspaceId);
  },

  removeFile: async (workspaceId: string, filename: string) => {
    await deleteWorkspaceFile(workspaceId, filename);
    await get().refreshWorkspace(workspaceId);
  },

  loadMemory: async (workspaceId: string, key?: string) => {
    try {
      const workspace = await apiGetWorkspace(workspaceId);
      if (workspace) {
        set({ memory: key ? { [key]: workspace.memory[key] } : workspace.memory });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load memory" });
    }
  },

  setMemory: async (workspaceId: string, key: string, value: any) => {
    await setWorkspaceMemory(workspaceId, { key, value });
    set((state) => ({
      memory: { ...state.memory, [key]: value },
    }));
  },

  setError: (error: string | null) => set({ error }),
}));
