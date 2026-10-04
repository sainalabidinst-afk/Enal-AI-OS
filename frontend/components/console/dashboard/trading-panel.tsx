"use client";

import { useEffect, useCallback, useState } from "react";
import { Activity, AlertTriangle, Gauge, Play, Square, RefreshCw } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { Toggle, Field } from "@/components/console/ui/controls";
import { useToast } from "@/components/ui/toast";
import { useConsolePreferences } from "@/store/console-settings-store";
import { startLiveFeed, stopLiveFeed, getFeedStatus, getLiveRegime } from "@/services/trading";
import type { MarketRegimeLive, FeedStatusResponse } from "@/types/trading";

const DEFAULT_SYMBOL = "BTCUSDT";
const DEFAULT_TIMEFRAMES = ["15m", "1h", "4h", "1d"];

export function TradingPanel() {
  const { showWarning, showError, showInfo } = useToast();
  const confidenceThreshold = useConsolePreferences((s) => s.alertLatencyMs);
  const setConfidenceThreshold = useConsolePreferences((s) => s.set);

  const [symbol, setSymbol] = useState(DEFAULT_SYMBOL);
  const [timeframes, setTimeframes] = useState<string[]>(DEFAULT_TIMEFRAMES);
  const [status, setStatus] = useState<FeedStatusResponse | null>(null);
  const [regime, setRegime] = useState<MarketRegimeLive | null>(null);
  const [loading, setLoading] = useState(false);
  const [alertLog, setAlertLog] = useState<
    { time: string; message: string; confidence: number }[]
  >([]);

  const loadStatus = useCallback(async () => {
    try {
      const data = await getFeedStatus();
      setStatus(data);
    } catch (error) {
      // silent on periodic poll
    }
  }, []);

  const loadRegime = useCallback(async () => {
    if (!symbol.trim()) return;
    try {
      const data = await getLiveRegime(symbol.trim());
      setRegime(data);
    } catch (error) {
      // silent on periodic poll
    }
  }, [symbol]);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(() => {
      loadStatus();
      if (status?.running) {
        loadRegime();
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [loadStatus, loadRegime, status?.running]);

  useEffect(() => {
    if (!regime || !status?.running) return;
    if (regime.confidence >= confidenceThreshold) {
      const entry = {
        time: new Date().toLocaleTimeString(),
        message: `High confidence alert for ${regime.symbol}: ${regime.regime}`,
        confidence: regime.confidence,
      };
      setAlertLog((prev) => [entry, ...prev].slice(0, 50));
      showWarning(
        `Trading Alert: ${regime.symbol}`,
        `Confidence ${(regime.confidence * 100).toFixed(0)}% — ${regime.regime}`
      );
    }
  }, [regime, status?.running, confidenceThreshold, showWarning]);

  const handleStart = useCallback(async () => {
    if (!symbol.trim()) return;
    setLoading(true);
    try {
      await startLiveFeed({ symbol: symbol.trim(), timeframes });
      showInfo("Live feed started", `Streaming ${symbol.trim()} on ${timeframes.join(", ")}`);
      await loadStatus();
    } catch (error) {
      showError("Failed to start feed", error instanceof Error ? error.message : undefined);
    } finally {
      setLoading(false);
    }
  }, [symbol, timeframes, showInfo, showError, loadStatus]);

  const handleStop = useCallback(async () => {
    setLoading(true);
    try {
      await stopLiveFeed();
      showInfo("Live feed stopped");
      await loadStatus();
    } catch (error) {
      showError("Failed to stop feed", error instanceof Error ? error.message : undefined);
    } finally {
      setLoading(false);
    }
  }, [showInfo, showError, loadStatus]);

  const handleRefresh = useCallback(async () => {
    setLoading(true);
    try {
      await loadStatus();
      await loadRegime();
    } finally {
      setLoading(false);
    }
  }, [loadStatus, loadRegime]);

  const feedActive = status?.running ?? false;

  return (
    <Panel className="h-full">
      <PanelHeader
        title="Trading Live Feed"
        subtitle={
          feedActive
            ? `Streaming ${status?.symbol ?? symbol} · ${status?.timeframes?.join(", ") ?? timeframes.join(", ")}`
            : "Real-time market regime and confidence alerts"
        }
        actions={
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRefresh}
              disabled={loading}
              className="flex items-center gap-1 rounded-lg border border-[var(--ecp-border)] px-2 py-1 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:bg-[var(--ecp-surface-2)] disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </button>
            {feedActive ? (
              <button
                type="button"
                onClick={handleStop}
                disabled={loading}
                className="flex items-center gap-1 rounded-lg bg-[var(--ecp-alert)] px-2 py-1 text-[11px] font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                <Square className="h-3.5 w-3.5" />
                Stop
              </button>
            ) : (
              <button
                type="button"
                onClick={handleStart}
                disabled={loading || !symbol.trim()}
                className="flex items-center gap-1 rounded-lg bg-[var(--ecp-gov)] px-2 py-1 text-[11px] font-medium text-[#04121a] transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                <Play className="h-3.5 w-3.5" />
                Start
              </button>
            )}
          </div>
        }
      />
      <PanelBody className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-3">
            <Field label="Symbol">
              <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                placeholder="BTCUSDT"
                className="w-full rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-3 py-1.5 text-xs text-[var(--ecp-text)] outline-none transition-colors focus:border-[var(--ecp-gov)]"
              />
            </Field>
            <Field label="Timeframes">
              <div className="flex flex-wrap gap-1.5">
                {DEFAULT_TIMEFRAMES.map((tf) => (
                  <button
                    key={tf}
                    type="button"
                    onClick={() =>
                      setTimeframes((current) =>
                        current.includes(tf)
                          ? current.filter((item) => item !== tf)
                          : [...current, tf]
                      )
                    }
                    className={`rounded-md border px-2 py-1 text-[11px] transition-colors ${
                      timeframes.includes(tf)
                        ? "border-[var(--ecp-gov)] bg-[var(--ecp-gov)]/10 text-[var(--ecp-gov)]"
                        : "border-[var(--ecp-border)] text-[var(--ecp-text-muted)] hover:bg-[var(--ecp-surface-2)]"
                    }`}
                  >
                    {tf}
                  </button>
                ))}
              </div>
            </Field>
          </div>
          <div className="space-y-3">
            <Field label="Feed Status" hint={feedActive ? "Live" : "Stopped"}>
              <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-secondary)] p-3 space-y-2">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[var(--ecp-text-dim)]">State</span>
                  <span className={`font-medium ${feedActive ? "text-green-500" : "text-[var(--ecp-text-muted)]"}`}>
                    {feedActive ? "Running" : "Stopped"}
                  </span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[var(--ecp-text-dim)]">Errors</span>
                  <span className="font-medium text-[var(--ecp-text)]">{status?.error_count ?? 0}</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[var(--ecp-text-dim)]">Fallback</span>
                  <span className={`font-medium ${status?.fallback_active ? "text-[var(--ecp-alert)]" : "text-green-500"}`}>
                    {status?.fallback_active ? "Active" : "Inactive"}
                  </span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[var(--ecp-text-dim)]">Last update</span>
                  <span className="font-medium text-[var(--ecp-text)]">
                    {status?.last_update
                      ? new Date(status.last_update * 1000).toLocaleTimeString()
                      : "—"}
                  </span>
                </div>
              </div>
            </Field>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-[var(--ecp-gov)]" />
              <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Live Regime
              </h3>
            </div>
            {regime ? (
              <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-secondary)] p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-[var(--ecp-text)]">{regime.symbol}</span>
                  <span className="rounded-full border border-[var(--ecp-border)] px-2 py-0.5 text-[11px] font-medium capitalize">
                    {regime.regime}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Gauge className="h-3.5 w-3.5 text-[var(--ecp-text-dim)]" />
                  <div className="flex-1">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="text-[var(--ecp-text-dim)]">Confidence</span>
                      <span className="font-medium text-[var(--ecp-text)]">
                        {(regime.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="mt-1 h-1.5 rounded-full bg-[var(--ecp-surface-3)]">
                      <div
                        className="h-1.5 rounded-full bg-[var(--ecp-gov)] transition-all"
                        style={{ width: `${Math.min(regime.confidence * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div>
                    <span className="text-[var(--ecp-text-dim)]">Volatility</span>
                    <p className="font-medium text-[var(--ecp-text)] capitalize">{regime.volatility}</p>
                  </div>
                  <div>
                    <span className="text-[var(--ecp-text-dim)]">Trend strength</span>
                    <p className="font-medium text-[var(--ecp-text)]">
                      {(regime.trend_strength * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="rounded-lg border border-dashed border-[var(--ecp-border)] bg-[var(--ecp-bg-secondary)] p-6 text-center">
                <Activity className="mx-auto h-5 w-5 text-[var(--ecp-text-dim)]" />
                <p className="mt-2 text-xs text-[var(--ecp-text-muted)]">
                  {feedActive ? "Waiting for first regime update..." : "Start feed to see live regime"}
                </p>
              </div>
            )}
          </div>
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-[var(--ecp-alert)]" />
              <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Confidence Alert Pipeline
              </h3>
            </div>
            <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-secondary)] p-3 space-y-3">
              <Field
                label={`Alert threshold (current: ${(confidenceThreshold * 100).toFixed(0)}%)`}
                hint="Trigger toast + backend notification when confidence exceeds threshold"
              >
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  value={confidenceThreshold * 100}
                  onChange={(e) => setConfidenceThreshold("alertLatencyMs", Number(e.target.value) / 100)}
                  className="w-full"
                />
              </Field>
              <div className="space-y-2">
                <h4 className="text-[11px] font-medium text-[var(--ecp-text-dim)]">Recent Alerts</h4>
                {alertLog.length === 0 ? (
                  <p className="text-[11px] text-[var(--ecp-text-muted)]">No alerts yet</p>
                ) : (
                  <div className="max-h-32 space-y-1 overflow-y-auto">
                    {alertLog.map((alert, idx) => (
                      <div
                        key={`${alert.time}-${idx}`}
                        className="flex items-center justify-between rounded-md bg-[var(--ecp-surface)] px-2 py-1"
                      >
                        <span className="text-[11px] text-[var(--ecp-text-secondary)]">{alert.message}</span>
                        <span className="text-[10px] text-[var(--ecp-text-dim)]">
                          {(alert.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </PanelBody>
    </Panel>
  );
}
