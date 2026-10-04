"use client";

import { useMemo } from "react";
import { Field, Toggle, inputClass } from "@/components/console/ui/controls";
import { EmptyBlock } from "@/components/console/ui/states";
import { BarChart, ChartLegend } from "@/components/console/charts/charts";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";

export function ObservabilityTab() {
  const telemetry = useConsoleStore((s) => s.telemetry);
  const prefs = useConsolePreferences();
  const setPref = useConsolePreferences((s) => s.set);

  const data = telemetry.data;
  const subsystems = useMemo(() => {
    if (!data) return { labels: [], values: [] };
    const rows: { label: string; value: number }[] = [
      { label: "analysis", value: data.analysis.count },
      { label: "chat", value: data.chat.count },
      { label: "parser", value: data.parser.count },
      { label: "reasoning", value: data.reasoning.count },
    ];
    return { labels: rows.map((row) => row.label), values: rows.map((row) => row.value) };
  }, [data]);

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="space-y-3">
        <Field label="Latency alert threshold (ms)">
          <input
            type="number"
            value={prefs.alertLatencyMs}
            onChange={(event) => setPref("alertLatencyMs", Number(event.target.value))}
            className={inputClass()}
          />
        </Field>
        <Field label="Error rate alert threshold (%)">
          <input
            type="number"
            value={prefs.alertErrorRate}
            onChange={(event) => setPref("alertErrorRate", Number(event.target.value))}
            className={inputClass()}
          />
        </Field>
        <Toggle
          checked={prefs.alertThrottle}
          onChange={(next) => setPref("alertThrottle", next)}
          label="Throttle repeated alerts"
          description="Collapse duplicate alerts within the same window"
        />
        <Toggle
          checked={prefs.autoTranscribe}
          onChange={(next) => setPref("autoTranscribe", next)}
          label="Auto-transcribe voice input"
          description="Transcribe recorded audio before sending to the chat pipeline"
        />
      </div>

      <div className="space-y-3">
        <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Runtime counters
        </h3>
        {subsystems.labels.length === 0 ? (
          <EmptyBlock
            title="No telemetry"
            hint={telemetry.error ?? "The telemetry endpoint returned no counters."}
          />
        ) : (
          <div className="grid gap-4 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-3 sm:grid-cols-[1fr_140px]">
            <BarChart
              labels={subsystems.labels}
              series={[{ label: "runs", values: subsystems.values }]}
              height={180}
              yTitle="runs"
            />
            <ChartLegend
              items={subsystems.labels.map((label, index) => ({
                label,
                color: ["#2dd4bf", "#38bdf8", "#3b82f6", "#f59e0b"][index % 4],
                value: String(subsystems.values[index]),
              }))}
            />
          </div>
        )}
      </div>
    </div>
  );
}