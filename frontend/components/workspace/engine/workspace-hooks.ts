import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";

export function useWorkspace() {
  return useWorkspaceStore();
}

export function useActiveApp() {
  const activeApp = useWorkspaceStore((s) => s.activeApp);
  const setActiveApp = useWorkspaceStore((s) => s.setActiveApp);
  return [activeApp, setActiveApp] as const;
}

export function usePanelState() {
  const panel = useWorkspaceStore((s) => s.panel);
  const toggleRightPanel = useWorkspaceStore((s) => s.toggleRightPanel);
  const toggleBottomPanel = useWorkspaceStore((s) => s.toggleBottomPanel);
  const setPanelSize = useWorkspaceStore((s) => s.setPanelSize);
  return { panel, toggleRightPanel, toggleBottomPanel, setPanelSize };
}

export function useSidebar() {
  const sidebarCollapsed = useWorkspaceStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useWorkspaceStore((s) => s.toggleSidebar);
  return { sidebarCollapsed, toggleSidebar };
}
