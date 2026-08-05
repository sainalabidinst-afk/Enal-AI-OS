import { create } from "zustand";

export type WorkspaceApp = "trading" | "network" | "code" | "security" | "research";

export interface PanelState {
  main: { open: boolean; size: number };
  right: { open: boolean; size: number };
  bottom: { open: boolean; size: number };
}

export interface WorkspaceState {
  activeApp: WorkspaceApp;
  panel: PanelState;
  setActiveApp: (app: WorkspaceApp) => void;
  toggleRightPanel: () => void;
  toggleBottomPanel: () => void;
  setPanelSize: (panel: keyof PanelState, size: number) => void;
  resetLayout: () => void;
}

const DEFAULT_PANEL: PanelState["main"] = { open: true, size: 100 };

const DEFAULT_PANELS: PanelState = {
  main: DEFAULT_PANEL,
  right: { open: true, size: 320 },
  bottom: { open: false, size: 200 },
};

export const useWorkspaceEngineStore = create<WorkspaceState>()((set) => ({
  activeApp: "trading",
  panel: DEFAULT_PANELS,

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

  resetLayout: () => set({ panel: DEFAULT_PANELS }),
}));
