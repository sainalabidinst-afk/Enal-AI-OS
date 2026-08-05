"use client";

import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface SplitViewProps {
  left: ReactNode;
  right: ReactNode;
  direction?: "horizontal" | "vertical";
  defaultLeftSize?: number;
  minLeftSize?: number;
  maxLeftSize?: number;
  className?: string;
}

export function SplitView({
  left,
  right,
  direction = "horizontal",
  defaultLeftSize = 320,
  minLeftSize = 240,
  maxLeftSize = 600,
  className,
}: SplitViewProps) {
  const [leftSize, setLeftSize] = useState(defaultLeftSize);
  const [isResizing, setIsResizing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();

      let newSize: number;
      if (direction === "horizontal") {
        newSize = e.clientX - rect.left;
      } else {
        newSize = e.clientY - rect.top;
      }
      newSize = Math.max(minLeftSize, Math.min(newSize, maxLeftSize));
      setLeftSize(newSize);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing, direction, minLeftSize, maxLeftSize]);

  const leftStyle =
    direction === "horizontal" ? { width: leftSize } : { height: leftSize };

  return (
    <div
      ref={containerRef}
      className={cn(
        "flex",
        direction === "horizontal" ? "flex-row" : "flex-col",
        className
      )}
    >
      <div style={leftStyle} className="shrink-0 overflow-hidden">
        {left}
      </div>
      <div
        onMouseDown={handleMouseDown}
        className={cn(
          "shrink-0 bg-transparent hover:bg-[var(--color-primary-500)] transition-colors",
          direction === "horizontal"
            ? "w-1 cursor-col-resize"
            : "h-1 cursor-row-resize"
        )}
      />
      <div className="flex-1 overflow-hidden">{right}</div>
    </div>
  );
}
