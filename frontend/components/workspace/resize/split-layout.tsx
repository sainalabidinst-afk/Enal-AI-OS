"use client";

import { type ReactNode, useState } from "react";

interface SplitLayoutProps {
  left: ReactNode;
  right: ReactNode;
  bottom?: ReactNode;
  rightOpen?: boolean;
  bottomOpen?: boolean;
  rightSize?: number;
  bottomSize?: number;
  onRightResize?: (size: number) => void;
  onBottomResize?: (size: number) => void;
}

export function SplitLayout({
  left,
  right,
  bottom,
  rightOpen = true,
  bottomOpen = false,
  rightSize = 320,
  bottomSize = 200,
  onRightResize,
  onBottomResize,
}: SplitLayoutProps) {
  const [showRight, setShowRight] = useState(rightOpen);
  const [showBottom, setShowBottom] = useState(bottomOpen);

  return (
    <div className="flex h-full w-full">
      <div className="flex-1 overflow-hidden">{left}</div>

      {showRight && (
        <div style={{ width: rightSize }} className="shrink-0 border-l border-[var(--color-border)]">
          {right}
        </div>
      )}

      {bottom && showBottom && (
        <div style={{ height: bottomSize }} className="shrink-0 border-t border-[var(--color-border)]">
          {bottom}
        </div>
      )}
    </div>
  );
}
