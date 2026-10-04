"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Play, Radio, RefreshCw, Square } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { Field } from "@/components/console/ui/controls";
import { Pill } from "@/components/console/ui/states";
import {
  FeedStatusCard,
  RegimeCard,
  RegimeHistoryChart,
  RegimeTickTable,
} from "@/components/console/trading/regime-widgets";
import { useToast } from "@/components/ui/toast";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";
import { formatPercent } from "@/lib/format";

const DEFAULT_SYMBOL = "BTCUSDT";
const TIMEFRAME_OPTIONS = ["15m", "1h", "4h", "1d"];

export function TradingPanel() {
  const { showWarning, showError, showInfo } = useToast();

  const feedStatus = useConsoleStore((s) => s.feedStatus);
  const regime = useConsoleStore((s) => s.regime);
  const history = useConsoleStore((s) => s.regimeHistory);
  const streamStatus = useConsoleStore((s) => s.streamStatus);
  const loadFeedStatus = useConsoleStore((s) => s.loadFeedStatus);
  const fetchLiveRegime = useConsoleStore((s) => s.fetchLiveRegime);
  const connectRegimeStream = useConsoleStore((s) => s.connectRegimeStream);
  const disconnectRegimeStream = useConsoleStore((s) => s.disconnectRegimeStream);
  const startFeed = useConsoleStore((s) => s.startFeed);
  const stopFeed = useConsoleStore((s) => s.stopFeed);

  const threshold = useConsolePreferences((s) => s.alertConfidence);
  const setPreference = useConsolePreferences((s) => s.set);

  const [symbol, setSymbol] = useState(DEFAULT_SYMBOL);
  const [timeframes, setTimeframes] = useState<string[]>(TIMEFRAME_OPTIONS);
  const [busy, setBusy] = useState(false);
  const [alerts, setAlerts] = useState<{ time: string; message: string }[]>([]);

  const streamRegime = useCallback(
    (pair: string) => {
      connectRegimeStream(pair, 5);
    },
    [connectRegimeStream]
  );

  useEffect(() => {
    loadFeedStatus();
    streamRegime(symbol);
    return () => disconnectRegimeStream();
    // stream lifecycle is tied to the console view, not to symbol edits
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loadFeedStatus, disconnectRegimeStream]);

  useEffect(() => {
    const latest = history[history.length - 1];
    if (!latest || latest.confidence < threshold) return;
    const message = `${latest.symbol}: ${latest.regime.replace(/_/g, " ")} at ${formatPercent(
      latest.confidence
    )} confidence`;
    setAlerts((current) =>
      current[0]?.message === message
        ? current
        : [{ time: new Date().toLocaleTimeString(), message }, ...current].slice(0, 20)
    );
    showWarning("Market regime alert", message);
  }, [history, threshold, showWarning]);

  async function handleStart() {
    if (!symbol.trim()) return;
    setBusy(true);
    try {
      await startFeed(symbol.trim(), timeframes, 5);
      showInfo("Live feed started", `${symbol.trim().toUpperCase()} · ${timeframes.join(", ")}`);
      streamRegime(symbol.trim());
    } catch (error) {
      showError(
        "Failed to start feed",
        error instanceof Error ? error.message : undefined
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleStop() {
    setBusy(true);
    try {
      await stopFeed();
      showInfo("Live feed stopped");
    } catch (error) {
      showError(
        "Failed to stop feed",
        error instanceof Error ? error.message : undefined
      );
    } finally {
      setBusy(false);
    }
  }

  const feedActive = feedStatus.data?.running ?? false;
  const streamLabel =
    streamStatus === "live"
      ? "streaming"
      : streamStatus === "connecting"
        ? "connecting"
        : streamStatus === "error"
          ? "stream error"
          : "idle";

  return (
    <Panel className="h-full">
      <PanelHeader
        title="Market Regime · Live Feed"
        subtitle={`${symbol.trim().toUpperCase() || DEFAULT_SYMBOL} · ${
          feedStatus.data?.timeframes?.join(", ") || timeframes.join(", ")
        }`}
        actions={
          <div className="flex items-center gap-2">
            <Pill tone={streamStatus === "live" ? "good" : streamStatus === "error" ? "bad" : "neutral"}>
              <Radio className="h-2.5 w-2.5" />
              {streamLabel}
            </Pill>
            <button
              type="button"
              onClick={() => {
                loadFeedStatus();
                fetchLiveRegime(symbol.trim());
              }}
              disabled={busy}
              className="flex items-center gap-1 rounded-lg border border-[var(--ecp-border)] px-2 py-1 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:bg-[var(--ecp-surface-2)] disabled:opacity-50"
            >
              <RefreshCw className="h-3 w-3" />
              Refresh
            </button>
            {feedActive ? (
              <button
                type="button"
                onClick={handleStop}
                disabled={busy}
                className="flex items-center gap-1 rounded-lg bg-[var(--ecp-alert)] px-2 py-1 text-[11px] font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                <Square className="h-3 w-3" />
                Stop
              </button>
            ) : (
              <button
                type="button"
                onClick={handleStart}
                disabled={busy || !symbol.trim()}
                className="flex items-center gap-1 rounded-lg bg-[var(--ecp-gov)] px-2 py-1 text-[11px] font-medium text-[#04121a] transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                <Play className="h-3 w-3" />
                Start
              </button>
            )}
          </div>
        }
      />

      <PanelBody className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Symbol">
            <input
              value={symbol}
              onChange={(event) => setSymbol(event.target.value.toUpperCase())}
              onKeyDown={(event) => {
                if (event.key === "Enter") streamRegime(symbol);
              }}
              placeholder="BTCUSDT"
              className="w-full rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-3 py-1.5 text-xs outline-none transition-colors focus:border-[var(--ecp-gov)]"
            />
          </Field>
          <Field label="Timeframes">
            <div className="flex flex-wrap gap-1.5">
              {TIMEFRAME_OPTIONS.map((timeframe) => (
                <button
                  key={timeframe}
                  type="button"
                  onClick={() =>
                    setTimeframes((current) =>
                      current.includes(timeframe)
                        ? current.filter((item) => item !== timeframe)
                        : [...current, timeframe]
                    )
                  }
                  className={`rounded-md border px-2 py-1 text-[11px] transition-colors ${
                    timeframes.includes(timeframe)
                      ? "border-[var(--ecp-gov)] bg-[var(--ecp-gov-soft)] text-[var(--ecp-gov)]"
                      : "border-[var(--ecp-border)] text-[var(--ecp-text-muted)] hover:bg-[var(--ecp-surface-2)]"
                  }`}
                >
                  {timeframe}
                </button>
              ))}
            </div>
          </Field>
        </div>

        <div className="grid gap-4 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)_minmax(0,0.9fr)]">
          <RegimeCard
            regime={regime.data}
            streamStatus={streamStatus}
            symbol={symbol.trim().toUpperCase() || DEFAULT_SYMBOL}
          />
          <div className="space-y-3">
            <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
              Confidence trend
            </h3>
            <RegimeHistoryChart history={history} />
          </div>
          <FeedStatusCard status={feedStatus.data} />
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          <div className="space-y-2">
            <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
              Streamed ticks
            </h3>
            <RegimeTickTable history={history} />
          </div>
          <div className="space-y-3">
            <h3 className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
              <AlertTriangle className="h-3 w-3 text-[var(--ecp-alert)]" />
              Confidence alerts
            </h3>
            <Field
              label={`Threshold ${formatPercent(threshold)}`}
              hint="Fires a console notification when a streamed tick exceeds it"
            >
              <input
                type="range"
                min={0}
                max={100}
                step={5}
                value={threshold * 100}
                onChange={(event) =>
                  setPreference("alertConfidence", Number(event.target.value) / 100)
                }
                className="w-full accent-[var(--ecp-gov)]"
              />
            </Field>
            {alerts.length === 0 ? (
              <p className="text-[11px] text-[var(--ecp-text-dim)]">No alerts yet.</p>
            ) : (
              <ul className="max-h-32 space-y-1 overflow-y-auto">
                {alerts.map((alert) => (
                  <li
                    key={`${alert.time}-${alert.message}`}
                    className="flex items-center justify-between gap-2 rounded-md bg-[var(--ecp-surface-2)] px-2 py-1 text-[11px]"
                  >
                    <span className="truncate text-[var(--ecp-text-muted)]">{alert.message}</span>
                    <span className="shrink-0 text-[var(--ecp-text-dim)]">{alert.time}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </PanelBody>
    </Panel>
  );
}