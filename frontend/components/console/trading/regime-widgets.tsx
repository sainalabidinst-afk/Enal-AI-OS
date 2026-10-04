"use client";

import { Activity, Gauge, Radio } from "lucide-react";
import { LineChart, CHART_PALETTE } from "@/components/console/charts/charts";
import { Pill } from "@/components/console/ui/states";
import { formatNumber, formatPercent } from "@/lib/format";
import type { FeedStatusResponse, MarketRegimeLive } from "@/types/trading";
import type { RegimeHistoryPoint, StreamStatus } from "@/store/console-store";

const REGIME_TONE: Record<string, "good" | "bad" | "warn" | "info" | "neutral"> = {
  bull: "good",
  bear: "bad",
  high_volatility: "warn",
  sideways: "info",
};

export function RegimeCard({
  regime,
  streamStatus,
  symbol,
}: {
  regime: MarketRegimeLive | null;
  streamStatus: StreamStatus;
  symbol: string;
}) {
  if (!regime) {
    return (
      <div className="rounded-lg border border-dashed border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-3 py-6 text-center">
        <Activity className="mx-auto h-5 w-5 text-[var(--ecp-text-dim)]" />
        <p className="mt-2 text-xs text-[var(--ecp-text-muted)]">
          {streamStatus === "connecting"
            ? "Connecting to the market feed…"
            : streamStatus === "live"
              ? `Waiting for the first ${symbol} tick…`
              : "Start the feed to detect the live market regime"}
        </p>
      </div>
    );
  }

  const tone = REGIME_TONE[regime.regime] ?? "neutral";

  return (
    <div className="space-y-3 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] p-3">
      <div className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-1.5 text-xs font-medium">
          <Radio
            className={`h-3.5 w-3.5 ${
              streamStatus === "live" ? "text-[var(--ecp-gov)]" : "text-[var(--ecp-text-dim)]"
            }`}
          />
          {regime.symbol || symbol}
        </span>
        <Pill tone={tone}>{regime.regime.replace(/_/g, " ")}</Pill>
      </div>

      <div>
        <div className="flex items-center justify-between text-[11px]">
          <span className="flex items-center gap-1 text-[var(--ecp-text-dim)]">
            <Gauge className="h-3 w-3" />
            Confidence
          </span>
          <span className="font-mono text-[var(--ecp-text)]">
            {formatPercent(regime.confidence)}
          </span>
        </div>
        <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-[var(--ecp-surface-3)]">
          <div
            className="h-full rounded-full bg-[var(--ecp-gov)] transition-all"
            style={{ width: `${Math.min(Math.max(regime.confidence * 100, 0), 100)}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 text-[11px]">
        <Stat label="Volatility" value={regime.volatility} capitalize />
        <Stat label="Trend strength" value={formatPercent(regime.trend_strength)} />
        <Stat label="Source" value={regime.source ?? "—"} />
        <Stat
          label="Detected"
          value={
            regime.timestamp
              ? new Date(regime.timestamp * 1000).toLocaleTimeString()
              : "—"
          }
        />
      </div>

      {regime.error && (
        <p className="rounded-md border border-[var(--ecp-alert)]/40 bg-[var(--ecp-alert-soft)] px-2 py-1.5 text-[11px] text-[var(--ecp-alert)]">
          {regime.error}
        </p>
      )}
    </div>
  );
}

export function FeedStatusCard({ status }: { status: FeedStatusResponse | null }) {
  const running = status?.running ?? false;
  return (
    <div className="space-y-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] p-3 text-[11px]">
      <Stat
        label="State"
        value={running ? "Running" : "Stopped"}
        tone={running ? "var(--ecp-gov)" : "var(--ecp-text-muted)"}
      />
      <Stat label="Symbol" value={status?.symbol ?? "—"} />
      <Stat label="Timeframes" value={status?.timeframes?.join(", ") || "—"} />
      <Stat
        label="Fallback"
        value={status?.fallback_active ? "Active" : "Inactive"}
        tone={status?.fallback_active ? "var(--ecp-alert)" : "var(--ecp-gov)"}
      />
      <Stat label="Poll errors" value={String(status?.error_count ?? 0)} />
      <Stat
        label="Last update"
        value={
          status?.last_update
            ? new Date(status.last_update * 1000).toLocaleTimeString()
            : "—"
        }
      />
    </div>
  );
}

export function RegimeHistoryChart({
  history,
  height = 200,
}: {
  history: RegimeHistoryPoint[];
  height?: number;
}) {
  if (history.length < 2) {
    return (
      <p className="rounded-lg border border-dashed border-[var(--ecp-border)] px-3 py-6 text-center text-[11px] text-[var(--ecp-text-dim)]">
        Confidence trend appears after two streamed ticks.
      </p>
    );
  }

  return (
    <LineChart
      height={height}
      labels={history.map((point) =>
        new Date(point.timestamp * 1000).toLocaleTimeString()
      )}
      series={[
        {
          label: "confidence",
          values: history.map((point) => point.confidence),
          color: CHART_PALETTE.gov,
        },
        {
          label: "trend strength",
          values: history.map((point) => point.trend_strength),
          color: CHART_PALETTE.sky,
          dashed: true,
        },
      ]}
      yTitle="0–1"
    />
  );
}

export function RegimeTickTable({ history }: { history: RegimeHistoryPoint[] }) {
  if (history.length === 0) {
    return (
      <p className="text-[11px] text-[var(--ecp-text-dim)]">No regime ticks recorded yet.</p>
    );
  }
  return (
    <ul className="max-h-40 space-y-1 overflow-y-auto">
      {history
        .slice()
        .reverse()
        .map((point) => (
          <li
            key={`${point.sequence}-${point.timestamp}`}
            className="flex items-center justify-between rounded-md bg-[var(--ecp-surface-2)] px-2 py-1 text-[11px]"
          >
            <span className="text-[var(--ecp-text-muted)]">
              {new Date(point.timestamp * 1000).toLocaleTimeString()}
            </span>
            <span className="flex items-center gap-2">
              <Pill tone={REGIME_TONE[point.regime] ?? "neutral"}>{point.regime}</Pill>
              <span className="font-mono text-[var(--ecp-text)]">
                {formatNumber(point.confidence)}
              </span>
            </span>
          </li>
        ))}
    </ul>
  );
}

function Stat({
  label,
  value,
  tone,
  capitalize = false,
}: {
  label: string;
  value: string;
  tone?: string;
  capitalize?: boolean;
}) {
  return (
    <div className="flex items-baseline justify-between gap-2 border-b border-[var(--ecp-border)]/60 pb-1">
      <span className="text-[var(--ecp-text-dim)]">{label}</span>
      <span
        className={`truncate font-medium ${capitalize ? "capitalize" : ""}`}
        style={tone ? { color: tone } : undefined}
      >
        {value}
      </span>
    </div>
  );
}