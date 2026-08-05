"use client";

import { ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";
import { WorkspaceHeader } from "./workspace-header";
import { WorkspaceSidebar } from "./workspace-sidebar";
import { WorkspaceMain } from "./workspace-main";
import { WorkspaceRightPanel } from "./workspace-right-panel";
import { WorkspaceBottomPanel } from "./workspace-bottom-panel";
import { WorkspaceDock } from "./workspace-dock";
import { WorkspaceStatusBar } from "./workspace-status-bar";

const MIN_RIGHT = 240;
const MAX_RIGHT = 600;
const MIN_BOTTOM = 120;
const MAX_BOTTOM = 400;
const ANIM_DURATION = 200;

export function WorkspaceLayout({ children }: { children: React.ReactNode }) {
  const activeApp = useWorkspaceEngineStore((s) => s.activeApp);
  const panel = useWorkspaceEngineStore((s) => s.panel);
  const toggleRightPanel = useWorkspaceEngineStore((s) => s.toggleRightPanel);
  const toggleBottomPanel = useWorkspaceEngineStore((s) => s.toggleBottomPanel);
  const setPanelSize = useWorkspaceEngineStore((s) => s.setPanelSize);

  const containerRef = useRef<HTMLDivElement>(null);
  const [isResizingRight, setIsResizingRight] = useState(false);
  const [isResizingBottom, setIsResizingBottom] = useState(false);

  const [rightWidth, setRightWidth] = useState(panel.right.size);
  const [bottomHeight, setBottomHeight] = useState(panel.bottom.size);
  const [rightMounted, setRightMounted] = useState(panel.right.open);
  const [bottomMounted, setBottomMounted] = useState(panel.bottom.open);

  useEffect(() => {
    if (panel.right.open) {
      setRightMounted(true);
      setRightWidth(panel.right.size);
    } else {
      setRightWidth(0);
      const timer = setTimeout(() => setRightMounted(false), ANIM_DURATION);
      return () => clearTimeout(timer);
    }
  }, [panel.right.open, panel.right.size]);

  useEffect(() => {
    if (panel.bottom.open) {
      setBottomMounted(true);
      setBottomHeight(panel.bottom.size);
    } else {
      setBottomHeight(0);
      const timer = setTimeout(() => setBottomMounted(false), ANIM_DURATION);
      return () => clearTimeout(timer);
    }
  }, [panel.bottom.open, panel.bottom.size]);

  const handleRightMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizingRight(true);
  }, []);

  const handleBottomMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizingBottom(true);
  }, []);

  useEffect(() => {
    if (!isResizingRight && !isResizingBottom) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      if (isResizingRight) {
        const width = rect.right - e.clientX;
        setPanelSize("right", Math.max(MIN_RIGHT, Math.min(width, MAX_RIGHT)));
      }
      if (isResizingBottom) {
        const height = rect.bottom - e.clientY;
        setPanelSize("bottom", Math.max(MIN_BOTTOM, Math.min(height, MAX_BOTTOM)));
      }
    };

    const handleMouseUp = () => {
      setIsResizingRight(false);
      setIsResizingBottom(false);
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizingRight, isResizingBottom, setPanelSize]);

  return (
    <div
      ref={containerRef}
      className="flex h-screen w-screen flex-col overflow-hidden bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]"
    >
      <WorkspaceHeader onToggleRight={toggleRightPanel} onToggleBottom={toggleBottomPanel} />

      <div className="flex flex-1 overflow-hidden">
        <WorkspaceSidebar activeApp={activeApp} />

        <div className="flex flex-1 flex-col overflow-hidden">
          <div className="flex flex-1 overflow-hidden">
            <WorkspaceMain app={activeApp}>{children}</WorkspaceMain>

            {rightMounted && (
              <div
                style={{ width: rightWidth }}
                className="shrink-0 overflow-hidden transition-[width] duration-200 ease-in-out"
              >
                <div
                  onMouseDown={handleRightMouseDown}
                  className="w-1 cursor-col-resize bg-transparent hover:bg-[var(--color-accent)] transition-colors"
                />
                <WorkspaceRightPanel />
              </div>
            )}
          </div>

          {bottomMounted && (
            <div
              style={{ height: bottomHeight }}
              className="shrink-0 overflow-hidden transition-[height] duration-200 ease-in-out"
            >
              <div
                onMouseDown={handleBottomMouseDown}
                className="h-1 cursor-row-resize bg-transparent hover:bg-[var(--color-accent)] transition-colors"
              />
              <WorkspaceBottomPanel />
            </div>
          )}
        </div>
      </div>

      <WorkspaceDock />
      <WorkspaceStatusBar />
    </div>
  );
}
