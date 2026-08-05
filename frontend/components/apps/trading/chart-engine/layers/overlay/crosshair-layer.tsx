"use client";

import { useChartEngineStore } from "../../stores/chart-engine-store";

export function CrosshairLayer() {
  const crosshair = useChartEngineStore((s) => s.crosshair);

  if (!crosshair) return null;

  return (
    <g>
      <line
        x1={crosshair.x}
        y1={0}
        x2={crosshair.x}
        y2={480}
        stroke="var(--color-secondary-500)"
        strokeWidth="1"
        strokeDasharray="4 4"
        opacity="0.5"
      />
      <line
        x1={0}
        y1={crosshair.y}
        x2={1000}
        y2={crosshair.y}
        stroke="var(--color-secondary-500)"
        strokeWidth="1"
        strokeDasharray="4 4"
        opacity="0.5"
      />
      <circle cx={crosshair.x} cy={crosshair.y} r="3" fill="var(--color-primary-500)" />
      <rect x={crosshair.x + 10} y={crosshair.y - 30} width="160" height="50" fill="var(--color-surface)" stroke="var(--color-border)" rx="4" />
      <text x={crosshair.x + 15} y={crosshair.y - 15} className="fill-[var(--color-secondary-500)] text-xs">
        {new Date(crosshair.timestamp).toLocaleString()}
      </text>
      <text x={crosshair.x + 15} y={crosshair.y} className="fill-[var(--color-foreground)] text-xs font-medium">
        Price: {crosshair.price.toFixed(2)}
      </text>
    </g>
  );
}


