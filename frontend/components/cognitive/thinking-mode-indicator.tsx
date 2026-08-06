"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function ThinkingModeIndicator() {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

  const layerConfig = {
    [CognitiveLayer.REACTIVE]: { label: "L1", color: "bg-blue-500", name: "Reactive" },
    [CognitiveLayer.ANALYTICAL]: { label: "L2", color: "bg-yellow-500", name: "Analytical" },
    [CognitiveLayer.META_COGNITIVE]: { label: "L3", color: "bg-purple-500", name: "Meta" },
  };

  const config = layerConfig[currentLayer];

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-2">
        <div className={cn("w-2 h-2 rounded-full", config.color)} />
        <span className="text-xs font-medium text-[var(--color-text-primary)]">
          {config.label} — {config.name}
        </span>
      </div>

      {thinkingMode && (
        <div className="flex items-center gap-2">
          <div className="h-2 w-24 rounded-full bg-[var(--color-bg-primary)] overflow-hidden">
            <div
              className={cn("h-full rounded-full transition-all duration-300", config.color)}
              style={{ width: `${thinkingMode.confidence * 100}%` }}
            />
          </div>
          <span className="text-xs text-[var(--color-text-secondary)]">
            {Math.round(thinkingMode.confidence * 100)}%
          </span>
        </div>
      )}

      {metaFlags.uncertainty && (
        <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 text-yellow-700">
          Uncertainty
        </span>
      )}
    </div>
  );
}
