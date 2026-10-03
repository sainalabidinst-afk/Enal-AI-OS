import { create } from "zustand";

export type WorkspaceApp = "trading" | "network" | "code" | "security" | "research" | "database" | "cognitive";

export interface PanelState {
  main: { open: boolean; size: number };
  right: { open: boolean; size: number };
  bottom: { open: boolean; size: number };
}

export interface WorkspaceInfo {
  id: string;
  name: string;
  active: boolean;
}

export interface ConsentRequest {
  id: string;
  title: string;
  description: string;
  severity: "low" | "medium" | "high";
  timestamp: string;
}

export interface TaskInfo {
  id: string;
  label: string;
  status: "running" | "pending" | "completed" | "failed";
}

export interface SystemStatus {
  online: boolean;
  model: string;
  latencyMs: number;
}

export interface WorkspaceState {
  activeApp: WorkspaceApp;
  panel: PanelState;
  sidebarCollapsed: boolean;
  workspaces: WorkspaceInfo[];
  activeWorkspace: string;
  consents: ConsentRequest[];
  tasks: TaskInfo[];
  system: SystemStatus;
  setActiveApp: (app: WorkspaceApp) => void;
  toggleRightPanel: () => void;
  toggleBottomPanel: () => void;
  toggleSidebar: () => void;
  setPanelSize: (panel: keyof PanelState, size: number) => void;
  resetLayout: () => void;
  setActiveWorkspace: (id: string) => void;
  addConsent: (req: ConsentRequest) => void;
  dismissConsent: (id: string) => void;
  addTask: (task: TaskInfo) => void;
  updateTask: (id: string, status: TaskInfo["status"]) => void;
  setLatency: (ms: number) => void;
}

const DEFAULT_PANEL: PanelState = {
  main: { open: true, size: 0 },
  right: { open: true, size: 320 },
  bottom: { open: false, size: 200 },
};

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeApp: "trading",
  panel: DEFAULT_PANEL,
  sidebarCollapsed: false,
  workspaces: [
    { id: "ws-main", name: "Main Workspace", active: true },
    { id: "ws-research", name: "Research Lab", active: false },
    { id: "ws-trading", name: "Trading Desk", active: false },
  ],
  activeWorkspace: "ws-main",
  consents: [],
  tasks: [],
  system: { online: true, model: "Qwen 3.5-9B", latencyMs: 0 },

  setActiveApp: (activeApp) => set({ activeApp }),

  toggleRightPanel: () =>
    set((state) => ({
      panel: {
        ...state.panel,
        right: {
          ...state.panel.right,
          open: !state.panel.right.open,
          size: state.panel.right.open ? 0 : 320,
        },
      },
    })),

  toggleBottomPanel: () =>
    set((state) => ({
      panel: {
        ...state.panel,
        bottom: {
          ...state.panel.bottom,
          open: !state.panel.bottom.open,
          size: state.panel.bottom.open ? 0 : 200,
        },
      },
    })),

  toggleSidebar: () =>
    set((state) => ({
      sidebarCollapsed: !state.sidebarCollapsed,
    })),

  setPanelSize: (panel, size) =>
    set((state) => ({
      panel: {
        ...state.panel,
        [panel]: {
          ...state.panel[panel],
          size: Math.max(0, Math.min(size, 800)),
        },
      },
    })),

  resetLayout: () => set({ panel: DEFAULT_PANEL, sidebarCollapsed: false }),

  setActiveWorkspace: (id) =>
    set((state) => ({
      workspaces: state.workspaces.map((w) => ({ ...w, active: w.id === id })),
      activeWorkspace: id,
    })),

  addConsent: (req) =>
    set((state) => ({ consents: [req, ...state.consents] })),

  dismissConsent: (id) =>
    set((state) => ({ consents: state.consents.filter((c) => c.id !== id) })),

  addTask: (task) =>
    set((state) => ({ tasks: [task, ...state.tasks] })),

  updateTask: (id, status) =>
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === id ? { ...t, status } : t)),
    })),

  setLatency: (ms) =>
    set((state) => ({
      system: { ...state.system, latencyMs: ms },
    })),
}));
