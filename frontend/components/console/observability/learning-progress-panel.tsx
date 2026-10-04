"use client";

import { useCallback, useEffect, useState } from "react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { MetricCard, MetricGrid } from "@/components/console/ui/metric-card";
import { EmptyBlock } from "@/components/console/ui/states";
import { BarChart, CHART_PALETTE } from "@/components/console/charts/charts";
import {
  getGrowthProgress,
  type GrowthProgress,
} from "@/services/observability";

const GRANULARITIES = [
  { id: "week", label: "Weekly" },
  { id: "month", label: "Monthly" },
] as const;

type Granularity = (typeof GRANULARITIES)[number]["id"];

export function LearningProgressPanel() {
  const [granularity, setGranularity] = useState<Granularity>("week");
  const [data, setData] = useState<GrowthProgress | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setData(await getGrowthProgress(granularity, 12));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load growth progress");
    } finally {
      setLoading(false);
    }
  }, [granularity]);

  useEffect(() => {
    load();
  }, [load]);

  const series = data?.series;
  const hasActivity = (series?.activities ?? []).some((value) => value > 0);

  return (
    <Panel>
      <PanelHeader
        title="Learning progress"
        subtitle="Self Development growth engine — hours invested, projects and new skills"
        actions={
          <div className="flex items-center gap-1">
            {GRANULARITIES.map((option) => (
              <button
                key={option.id}
                type="button"
                onClick={() => setGranularity(option.id)}
                className={`rounded-md px-2 py-1 text-[11px] font-medium transition ${
                  granularity === option.id
                    ? "bg-[var(--ecp-surface-3)] text-[var(--ecp-text)]"
                    : "text-[var(--ecp-text-muted)] hover:text-[var(--ecp-text)]"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        }
      />
      <PanelBody>
        <div className="space-y-4">
          <MetricGrid>
            <MetricCard
              label="Hours invested"
              value={data ? data.total_hours.toFixed(1) : "—"}
              hint="all tracked activities"
              tone="sky"
              loading={loading && !data}
            />
            <MetricCard
              label="Projects"
              value={data ? String(data.total_projects) : "—"}
              hint={`${data?.total_activities ?? 0} activities`}
              tone="gov"
              loading={loading && !data}
            />
            <MetricCard
              label="Active skills"
              value={data ? String(data.active_skills) : "—"}
              hint="with recorded practice"
              tone="blue"
              loading={loading && !data}
            />
            <MetricCard
              label="Goal alignment"
              value={data ? `${Math.round(data.alignment_rate * 100)}%` : "—"}
              hint={
                data
                  ? `${data.unaligned_activities} unrelated / ${data.aligned_activities} aligned`
                  : "—"
              }
              tone={data && data.alignment_rate < 0.3 ? "alert" : "gov"}
              loading={loading && !data}
            />
          </MetricGrid>

          {!hasActivity ? (
            <EmptyBlock
              title="No learning activity yet"
              hint={
                error ??
                "Record an activity via POST /api/v1/self-development/activities to see progress."
              }
            />
          ) : (
            <BarChart
              labels={series?.labels ?? []}
              series={[
                {
                  label: "hours",
                  values: series?.hours ?? [],
                  color: CHART_PALETTE.sky,
                },
                {
                  label: "projects",
                  values: series?.projects ?? [],
                  color: CHART_PALETTE.gov,
                },
              ]}
              height={240}
              yTitle="count"
            />
          )}

          {data && data.skills.length > 0 ? (
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Skill levels
              </h3>
              <ul className="mt-2 space-y-1">
                {data.skills.slice(0, 8).map((skill) => (
                  <li
                    key={skill.skill}
                    className="flex items-center justify-between rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-1.5"
                  >
                    <span className="text-xs font-medium text-[var(--ecp-text)]">{skill.skill}</span>
                    <span className="text-[11px] text-[var(--ecp-text-muted)]">
                      {skill.level} · {skill.projects_completed} projects ·{" "}
                      {Math.round(skill.minutes_spent / 6) / 10}h
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      </PanelBody>
    </Panel>
  );
}
