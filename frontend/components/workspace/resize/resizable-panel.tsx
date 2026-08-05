"use client";

import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";

interface ResizablePanelProps {
  children: ReactNode;
  direction?: "horizontal" | "vertical";
  defaultSize?: number;
  minSize?: number;
  maxSize?: number;
  resizerClassName?: string;
  onResize?: (size: number) => void;
}

export function ResizablePanel({
  children,
  direction = "horizontal",
  defaultSize = 320,
  minSize = 240,
  maxSize = 600,
  resizerClassName,
  onResize,
}: ResizablePanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState(defaultSize);
  const [isResizing, setIsResizing] = useState(false);

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault();
      setIsResizing(true);
    },
    []
  );

  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.parentElement?.getBoundingClientRect();
      if (!rect) return;

      let newSize: number;
      if (direction === "horizontal") {
        newSize = rect.right - e.clientX;
      } else {
        newSize = rect.bottom - e.clientY;
      }
      newSize = Math.max(minSize, Math.min(newSize, maxSize));
      setSize(newSize);
      onResize?.(newSize);
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
  }, [isResizing, direction, minSize, maxSize, onResize]);

  const style =
    direction === "horizontal"
      ? { width: size }
      : { height: size };

  const resizerStyle =
    direction === "horizontal"
      ? { width: 4, cursor: "col-resize" }
      : { height: 4, cursor: "row-resize" };

  return (
    <div ref={containerRef} style={style} className="shrink-0 overflow-hidden">
      {children}
      <div
        onMouseDown={handleMouseDown}
        style={resizerStyle}
        className={`bg-transparent hover:bg-[var(--color-accent)] transition-colors ${resizerClassName || ""}`}
      />
    </div>
  );
}
