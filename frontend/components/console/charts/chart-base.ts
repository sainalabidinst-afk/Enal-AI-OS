"use client";

import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  RadialLinearScale,
  Tooltip,
  type ChartOptions,
} from "chart.js";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  RadialLinearScale,
  Tooltip
);

export const CHART_PALETTE = {
  gov: "#2dd4bf",
  sky: "#38bdf8",
  blue: "#3b82f6",
  alert: "#f59e0b",
  danger: "#ef4444",
  success: "#22c55e",
  muted: "#6b7890",
};

const GRID = "rgba(255,255,255,0.06)";
const TICK = "#93a1b8";

export const TOOLTIP_STYLE = {
  backgroundColor: "#0e1420",
  borderColor: "#202b3d",
  borderWidth: 1,
  titleColor: "#e7ecf6",
  bodyColor: "#93a1b8",
  padding: 10,
};

export function baseOptions(overrides?: ChartOptions<"line">): ChartOptions<"line"> {
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: "index", intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: { ...TOOLTIP_STYLE, displayColors: false },
    },
    scales: {
      x: { grid: { color: GRID }, ticks: { color: TICK, font: { size: 10 } } },
      y: { grid: { color: GRID }, ticks: { color: TICK, font: { size: 10 } } },
    },
    ...overrides,
  };
}

export function axis(title?: string) {
  return {
    grid: { color: GRID },
    ticks: { color: TICK, font: { size: 10 } },
    title: title ? { display: true, text: title, color: TICK, font: { size: 10 } } : undefined,
  };
}

export function seriesColor(index: number, override?: string): string {
  if (override) return override;
  const palette = Object.values(CHART_PALETTE);
  return palette[index % palette.length];
}