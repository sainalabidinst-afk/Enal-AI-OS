"use client";

import { useChartEngineStore } from "../../stores/chart-engine-store";

export function DrawingLayer() {
  const drawings = useChartEngineStore((s) => s.drawings);

  return (
    <g>
      {drawings.map((drawing) => (
        <g key={drawing.id}>
          {drawing.type === "trendline" && drawing.points.length === 2 && (
            <line
              x1={drawing.points[0].x}
              y1={drawing.points[0].y}
              x2={drawing.points[1].x}
              y2={drawing.points[1].y}
              stroke="var(--color-primary-500)"
              strokeWidth="2"
            />
          )}
          {drawing.type === "horizontal" && drawing.points.length === 1 && (
            <line
              x1={0}
              y1={drawing.points[0].y}
              x2={1000}
              y2={drawing.points[0].y}
              stroke="var(--color-warning-500)"
              strokeWidth="2"
              strokeDasharray="6 4"
            />
          )}
          {drawing.type === "rectangle" && drawing.points.length === 2 && (
            <rect
              x={Math.min(drawing.points[0].x, drawing.points[1].x)}
              y={Math.min(drawing.points[0].y, drawing.points[1].y)}
              width={Math.abs(drawing.points[1].x - drawing.points[0].x)}
              height={Math.abs(drawing.points[1].y - drawing.points[0].y)}
              fill="var(--color-primary-500)"
              fillOpacity="0.1"
              stroke="var(--color-primary-500)"
              strokeWidth="2"
            />
          )}
        </g>
      ))}
    </g>
  );
}


