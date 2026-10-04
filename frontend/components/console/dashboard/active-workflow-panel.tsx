"use client";

import Link from "next/link";
import { ExternalLink } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { WorkflowCanvas } from "@/components/console/builder/workflow-canvas";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { selectClass } from "@/components/console/ui/controls";

export function ActiveWorkflowPanel({
  blueprintId,
  onSelect,
}: {
  blueprintId?: string;
  onSelect?: (id: string) => void;
}) {
  useConsoleHydration("blueprints");
  const blueprints = useConsoleStore((s) => s.blueprints.data);
  const selected =
    blueprints?.find((item) => item.id === blueprintId) ?? blueprints?.[0] ?? null;

  return (
    <Panel className="h-full">
      <PanelHeader
        title="Active Workflow"
        subtitle={
          selected
            ? `${selected.name} · ${selected.tools.length} tools · ${selected.model}`
            : "Agent blueprints published through the builder API"
        }
        actions={
          <Link
            href="/console/builder"
            className="flex items-center gap-1 text-[11px] text-[var(--ecp-gov)] hover:underline"
          >
            Builder
            <ExternalLink className="h-3 w-3" />
          </Link>
        }
      />
      <PanelBody className="space-y-3">
        {blueprints && blueprints.length > 0 && (
          <select
            value={selected?.id ?? ""}
            onChange={(event) => onSelect?.(event.target.value)}
            className={selectClass()}
          >
            {blueprints.map((blueprint) => (
              <option key={blueprint.id} value={blueprint.id}>
                {blueprint.name || blueprint.id}
              </option>
            ))}
          </select>
        )}
        <WorkflowCanvas
          blueprint={selected}
          height={260}
          emptyLabel={
            blueprints && blueprints.length === 0
              ? "No blueprints yet — create one in the Builder to visualise a pipeline"
              : "Select a blueprint to render its pipeline"
          }
        />
      </PanelBody>
    </Panel>
  );
}