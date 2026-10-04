"use client";

import { useMemo } from "react";
import { Doughnut, Radar } from "react-chartjs-2";
import type { ChartData, ChartOptions } from "chart.js";
import { CHART_PALETTE, TOOLTIP_STYLE, seriesColor } from "./chart-base";
import type { Series } from "./cartesian-charts";

export function DoughnutChart({
  labels,
  values,
  colors,
  height = 200,
  centerLabel,
  centerValue,
}: {
  labels: string[];
  values: number[];
  colors?: string[];
  height?: number;
  centerLabel?: string;
  centerValue?: string;
}) {
  const data = useMemo<ChartData<"doughnut">>(
    () => ({
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: colors ?? Object.values(CHART_PALETTE),
          borderColor: "#121a28",
          borderWidth: 2,
          hoverOffset: 6,
        },
      ],
    }),
    [labels, values, colors]
  );

  const options: ChartOptions<"doughnut"> = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "68%",
    plugins: {
      legend: { display: false },
      tooltip: TOOLTIP_STYLE,
    },
  };

  return (
    <div className="relative w-full" style={{ height }}>
      <Doughnut data={data} options={options} />
      {(centerValue || centerLabel) && (
        <div className="pointer-events-none absolute inset-0 grid place-items-center text-center">
          <div>
            {centerValue && (
              <p className="text-2xl font-bold leading-none text-[var(--ecp-text)]">
                {centerValue}
              </p>
            )}
            {centerLabel && (
              <p className="mt-1 text-[10px] uppercase tracking-wide text-[var(--ecp-text-dim)]">
                {centerLabel}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function RadarChart({
  labels,
  series,
  height = 260,
  max = 1,
}: {
  labels: string[];
  series: Series[];
  height?: number;
  max?: number;
}) {
  const data = useMemo<ChartData<"radar">>(
    () => ({
      labels,
      datasets: series.map((item, index) => {
        const color = seriesColor(index, item.color);
        return {
          label: item.label,
          data: item.values,
          borderColor: color,
          backgroundColor: `${color}20`,
          borderWidth: 1.8,
          pointBackgroundColor: color,
          pointRadius: 3,
        };
      }),
    }),
    [labels, series]
  );

  const options: ChartOptions<"radar"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: TOOLTIP_STYLE,
    },
    scales: {
      r: {
        min: 0,
        max,
        grid: { color: "rgba(255,255,255,0.06)" },
        angleLines: { color: "rgba(255,255,255,0.06)" },
        pointLabels: { color: "#93a1b8", font: { size: 10 } },
        ticks: { display: false },
      },
    },
  };

  return (
    <div style={{ height }} className="w-full">
      <Radar data={data} options={options} />
    </div>
  );
}