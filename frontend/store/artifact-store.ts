import { create } from "zustand";
import type { Artifact } from "@/types/artifact";
import {
  listArtifacts,
  createArtifact,
  getArtifact,
  getArtifactVersion,
  addArtifactVersion,
  restoreArtifactVersion,
  deleteArtifact,
} from "@/services/artifact";

interface ArtifactState {
  artifacts: Artifact[];
  activeArtifactId: string | null;
  isLoading: boolean;
  error: string | null;
  loadArtifacts: (workspaceId?: string, artifactType?: string) => Promise<void>;
  createArtifact: (request: { workspace_id: string; name: string; type: string; description?: string; content?: string; metadata?: Record<string, any> }) => Promise<Artifact | null>;
  selectArtifact: (artifactId: string | null) => void;
  refreshArtifact: (artifactId: string) => Promise<void>;
  addVersion: (artifactId: string, request: { content?: string; metadata?: Record<string, any> }) => Promise<void>;
  restoreVersion: (artifactId: string, version: number) => Promise<void>;
  deleteArtifact: (artifactId: string) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useArtifactStore = create<ArtifactState>()((set, get) => ({
  artifacts: [],
  activeArtifactId: null,
  isLoading: false,
  error: null,

  loadArtifacts: async (workspaceId?: string, artifactType?: string) => {
    set({ isLoading: true, error: null });
    try {
      const artifacts = await listArtifacts(workspaceId, artifactType);
      set({ artifacts, isLoading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load artifacts", isLoading: false });
    }
  },

  createArtifact: async (request) => {
    set({ isLoading: true, error: null });
    try {
      const artifact = await createArtifact(request);
      set((state) => ({
        artifacts: [...state.artifacts, artifact],
        isLoading: false,
      }));
      return artifact;
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to create artifact", isLoading: false });
      return null;
    }
  },

  selectArtifact: (artifactId: string | null) => set({ activeArtifactId: artifactId }),

  refreshArtifact: async (artifactId: string) => {
    try {
      const artifact = await getArtifact(artifactId);
      set((state) => ({
        artifacts: state.artifacts.find((a) => a.id === artifactId)
          ? state.artifacts.map((a) => (a.id === artifactId ? artifact : a))
          : [...state.artifacts, artifact],
      }));
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load artifact" });
    }
  },

  addVersion: async (artifactId: string, request: { content?: string; metadata?: Record<string, any> }) => {
    await addArtifactVersion(artifactId, request);
    await get().refreshArtifact(artifactId);
  },

  restoreVersion: async (artifactId: string, version: number) => {
    await restoreArtifactVersion(artifactId, version);
    await get().refreshArtifact(artifactId);
  },

  deleteArtifact: async (artifactId: string) => {
    await deleteArtifact(artifactId);
    set((state) => ({
      artifacts: state.artifacts.filter((a) => a.id !== artifactId),
      activeArtifactId: state.activeArtifactId === artifactId ? null : state.activeArtifactId,
    }));
  },

  setError: (error: string | null) => set({ error }),
}));
