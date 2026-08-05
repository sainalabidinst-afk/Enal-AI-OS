"use client";

import { useCallback, useEffect, useRef } from "react";
import { useChartEngineStore } from "../stores/chart-engine-store";

export function useChartInteractions(containerRef: React.RefObject<HTMLDivElement | null>) {
  const setCrosshair = useChartEngineStore((s) => s.setCrosshair);
  const addDrawing = useChartEngineStore((s) => s.addDrawing);
  const activeDrawingTool = useChartEngineStore((s) => s.activeDrawingTool);
  const isDrawing = useRef(false);
  const currentDrawing = useRef<{ x: number; y: number }[]>([]);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!containerRef.current) return;

      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (activeDrawingTool !== "none") {
        if (!isDrawing.current) {
          isDrawing.current = true;
          currentDrawing.current = [{ x, y }];
        } else {
          currentDrawing.current = [currentDrawing.current[0], { x, y }];
        }
      }
    },
    [activeDrawingTool, containerRef]
  );

  const handleMouseUp = useCallback(() => {
    if (isDrawing.current && currentDrawing.current.length > 0 && activeDrawingTool !== "none") {
      addDrawing({
        id: `drawing-${Date.now()}`,
        type: activeDrawingTool as any,
        points: [...currentDrawing.current],
      });
    }
    isDrawing.current = false;
    currentDrawing.current = [];
  }, [activeDrawingTool, addDrawing]);

  return {
    handleMouseMove,
    handleMouseUp,
  };
}


