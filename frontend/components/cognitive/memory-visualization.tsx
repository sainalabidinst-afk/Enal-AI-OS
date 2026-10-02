"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import type { MemoryLayerData } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function MemoryVisualization() {
  const memoryLayers = useCognitiveStore((s) => s.memoryLayers);

  return (
    <div className="space-y-3">
      {memoryLayers.map((layer: MemoryLayerData) => (
        <MemoryLayerItem key={layer.type} layer={layer} />
      ))}
    </div>
  );
}

interface MemoryLayerItemProps {
  layer: MemoryLayerData;
}

function MemoryLayerItem({ layer }: MemoryLayerItemProps) {
  const pct = Math.round(layer.utilization * 100);

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div
            className="h-3 w-3 shrink-0 rounded"
            style={{ backgroundColor: layer.color }}
          />
          <span className="text-xs font-medium text-[var(--color-text-primary)]">{layer.name}</span>
          <span className="text-[10px] text-[var(--color-text-secondary)]">
            {layer.used.toLocaleString()} / {layer.capacity.toLocaleString()}
          </span>
        </div>
        <span className="text-xs text-[var(--color-text-secondary)]">{pct}%</span>
      </div>
      <div className="h-1.5 w-full rounded-full bg-[var(--color-bg-primary)] overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ backgroundColor: layer.color, width: `${Math.min(pct, 100)}%` }}
        />
      </div>
      <div className="flex items-center justify-between text-[10px] text-[var(--color-text-secondary)]">
        <span>{layer.description}</span>
        {layer.last_access && <span>Last: {new Date(layer.last_access).toLocaleTimeString()}</span>}
      </div>
    </div>
  );
}
