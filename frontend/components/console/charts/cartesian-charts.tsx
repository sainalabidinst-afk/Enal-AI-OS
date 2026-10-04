"use client";

import { useMemo } from "react";
import { Bar, Line } from "react-chartjs-2";
import type { ChartData, ChartOptions } from "chart.js";
import { axis, baseOptions, seriesColor } from "./chart-base";

export interface Series {
  label: string;
  values: number[];
  color?: string;
}

export function LineChart({
  labels,
  series,
  height = 220,
  fill = false,
  yTitle,
}: {
  labels: string[];
  series: Series[];
  height?: number;
  fill?: boolean;
  yTitle?: string;
}) {
  const data = useMemo<ChartData<"line">>(
    () => ({
      labels,
      datasets: series.map((item, index) => ({
        label: item.label,
        data: item.values,
        borderColor: seriesColor(index, item.color),
        borderWidth: 1.8,
        pointRadius: 0,
        pointHoverRadius: 4,
        tension: 0.35,
        fill: fill ? "origin" : false,
        backgroundColor: `${seriesColor(index, item.color)}22`,
      })),
    }),
    [labels, series, fill]
  );

  const options = baseOptions({
    scales: {
      x: {
        grid: { color: "rgba(255,255,255,0.06)" },
        ticks: { color: "#93a1b8", font: { size: 10 }, maxTicksLimit: 12 },
      },
      y: axis(yTitle),
    },
  });

  return (
    <div style={{ height }} className="w-full">
      <Line data={data} options={options} />
    </div>
  );
}

export function BarChart({
  labels,
  series,
  height = 220,
  stacked = false,
  horizontal = false,
  yTitle,
}: {
  labels: string[];
  series: Series[];
  height?: number;
  stacked?: boolean;
  horizontal?: boolean;
  yTitle?: string;
}) {
  const data = useMemo<ChartData<"bar">>(
    () => ({
      labels,
      datasets: series.map((item, index) => ({
        label: item.label,
        data: item.values,
        backgroundColor: seriesColor(index, item.color),
        borderRadius: 4,
        borderSkipped: false,
        barPercentage: 0.7,
        categoryPercentage: 0.75,
      })),
    }),
    [labels, series]
  );

  const valueScale = { ...axis(yTitle), stacked };
  const categoryScale = {
    grid: { display: false },
    ticks: { color: "#93a1b8", font: { size: 10 }, autoSkip: false },
    stacked,
  };

  const options = baseOptions({
    indexAxis: horizontal ? ("y" as const) : ("x" as const),
    scales: horizontal
      ? ({ x: valueScale, y: categoryScale } as never)
      : ({ x: categoryScale, y: valueScale } as never),
  }) as unknown as ChartOptions<"bar">;

  return (
    <div style={{ height }} className="w-full">
      <Bar data={data} options={options} />
    </div>
  );
}

export function ChartLegend({
  items,
}: {
  items: { label: string; color: string; value?: string }[];
}) {
  return (
    <ul className="space-y-1.5">
      {items.map((item) => (
        <li key={item.label} className="flex items-center gap-2 text-[11px]">
          <span
            className="h-2 w-2 shrink-0 rounded-sm"
            style={{ backgroundColor: item.color }}
          />
          <span className="flex-1 truncate text-[var(--ecp-text-muted)]">{item.label}</span>
          {item.value && (
            <span className="font-medium text-[var(--ecp-text)]">{item.value}</span>
          )}
        </li>
      ))}
    </ul>
  );
}