"use client";

import { type ReactNode, useContext } from "react";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import type { WorkspaceApp, WorkspaceState } from "@/components/workspace/stores/workspace-store";

export const WorkspaceContext = createContext<WorkspaceState | null>(null);

export function useWorkspaceContext() {
  const ctx = useContext(WorkspaceContext);
  if (!ctx) {
    throw new Error("Workspace components must be used within WorkspaceProvider");
  }
  return ctx;
}

export function useActiveApp(): WorkspaceApp {
  const ctx = useWorkspaceContext();
  return ctx.activeApp;
}

export function usePanel() {
  const ctx = useWorkspaceContext();
  return ctx.panel;
}

export function useSidebarCollapsed() {
  const ctx = useWorkspaceContext();
  return ctx.sidebarCollapsed;
}

import { createContext } from "react";
