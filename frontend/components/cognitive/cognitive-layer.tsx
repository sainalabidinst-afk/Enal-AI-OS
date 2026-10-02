"use client";

import { type ReactNode, Children } from "react";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer as CognitiveLayerEnum } from "@/types/cognitive";
import { cn } from "@/lib/utils";

interface CognitiveLayerProps {
  children: ReactNode;
  fallback?: ReactNode;
}

const LAYER_CONFIG = {
  [CognitiveLayerEnum.REACTIVE]: {
    label: "System 1 — Fast Thinking",
    description: "Reactive, instant responses",
    className: "border-l-4 border-l-[var(--color-primary-500)]",
  },
  [CognitiveLayerEnum.ANALYTICAL]: {
    label: "System 2 — Deliberate Thinking",
    description: "Analytical, step-by-step reasoning",
    className: "border-l-4 border-l-[var(--color-secondary-500)]",
  },
  [CognitiveLayerEnum.META_COGNITIVE]: {
    label: "System 3 — Strategic Thinking",
    description: "Meta-cognitive, cross-capability insights",
    className: "border-l-4 border-l-[var(--color-accent)]",
  },
} as const;

const LAYER_ORDER = [CognitiveLayerEnum.REACTIVE, CognitiveLayerEnum.ANALYTICAL, CognitiveLayerEnum.META_COGNITIVE];

export function CognitiveLayer({ children, fallback }: CognitiveLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const config = LAYER_CONFIG[currentLayer];
  const childArray = Children.toArray(children);

  return (
    <div className={cn("flex flex-col h-full w-full", config.className)}>
      <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-[var(--color-text-primary)] uppercase tracking-wide">
            {config.label}
          </span>
          <span className="text-xs text-[var(--color-text-secondary)]">
            {config.description}
          </span>
        </div>
        <CognitiveLayerTabs />
      </div>
      <div className="flex-1 overflow-hidden">
        {childArray.map((child, index) => {
          const layer = LAYER_ORDER[index];
          return (
            <div
              key={index}
              hidden={layer !== currentLayer}
              className="h-full"
            >
              {child}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function CognitiveLayerTabs() {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);

  const tabs = [
    { id: CognitiveLayerEnum.REACTIVE, label: "L1" },
    { id: CognitiveLayerEnum.ANALYTICAL, label: "L2" },
    { id: CognitiveLayerEnum.META_COGNITIVE, label: "L3" },
  ];

  return (
    <div className="flex gap-1 rounded-lg bg-[var(--color-bg-primary)] p-1">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setLayer(tab.id)}
          className={cn(
            "px-2 py-1 rounded text-xs font-medium transition-colors",
            currentLayer === tab.id
              ? "bg-[var(--color-primary-500)] text-white"
              : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]",
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
