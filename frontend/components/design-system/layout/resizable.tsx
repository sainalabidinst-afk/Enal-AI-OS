"use client";

import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface ResizableProps {
  children: ReactNode;
  direction?: "horizontal" | "vertical";
  defaultSize?: number;
  minSize?: number;
  maxSize?: number;
  className?: string;
  onResize?: (size: number) => void;
}

export function Resizable({
  children,
  direction = "horizontal",
  defaultSize = 320,
  minSize = 240,
  maxSize = 600,
  className,
  onResize,
}: ResizableProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState(defaultSize);
  const [isResizing, setIsResizing] = useState(false);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

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

  return (
    <div ref={containerRef} style={style} className={cn("shrink-0 overflow-hidden", className)}>
      {children}
      <div
        onMouseDown={handleMouseDown}
        className={cn(
          "bg-transparent hover:bg-[var(--color-primary-500)] transition-colors",
          direction === "horizontal" ? "w-1 cursor-col-resize" : "h-1 cursor-row-resize"
        )}
      />
    </div>
  );
}
