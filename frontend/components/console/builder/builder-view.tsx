"use client";

import { useEffect, useMemo, useState } from "react";
import type { Edge, Node } from "reactflow";
import { PageHeader, Panel, PanelBody } from "@/components/console/ui/panel";
import {
  BuilderCanvasSurface,
  BuilderProvider,
  useBuilderGraph,
} from "@/components/console/builder/builder-canvas";
import {
  BlueprintConfigPanel,
  NodeInspector,
  NodePalette,
  blueprintSelectClass,
  type BlueprintForm,
} from "@/components/console/builder/builder-panels";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";

const EMPTY_FORM: BlueprintForm = {
  name: "",
  model: "",
  prompt: "",
  temperature: 0.7,
  maxTokens: 1024,
};

export function BuilderView() {
  return (
    <BuilderProvider>
      <BuilderWorkspace />
    </BuilderProvider>
  );
}

function BuilderWorkspace() {
  useConsoleHydration("blueprints", "governance");
  const blueprints = useConsoleStore((s) => s.blueprints.data);
  const saveBlueprint = useConsoleStore((s) => s.saveBlueprint);
  const loadBlueprints = useConsoleStore((s) => s.loadBlueprints);
  const models = useConsoleStore((s) => s.modelProviders.data);

  const graph = useBuilderGraph();
  const [form, setForm] = useState<BlueprintForm>(EMPTY_FORM);
  const [blueprintId, setBlueprintId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const modelOptions = useMemo(() => {
    const list = models?.flatMap((provider) => provider.models ?? []) ?? [];
    return Array.from(new Set(list));
  }, [models]);

  useEffect(() => {
    if (!blueprintId) return;
    const blueprint = blueprints?.find((item) => item.id === blueprintId);
    if (!blueprint) return;
    const stored = blueprint.metadata?.graph as
      | { nodes?: Node[]; edges?: Edge[] }
      | undefined;
    graph.load({
      nodes: stored?.nodes ?? [],
      edges: stored?.edges ?? [],
    });
    setForm({
      name: blueprint.name,
      model: blueprint.model,
      prompt: blueprint.prompt,
      temperature: blueprint.temperature,
      maxTokens: blueprint.max_tokens,
    });
    // graph.load is stable across renders
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [blueprintId, blueprints]);

  const counts = {
    tools: graph.nodes.filter((node) => node.type === "tool").length,
    knowledge: graph.nodes.filter((node) => node.type === "knowledge").length,
    nodes: graph.nodes.length,
  };

  async function handleSave() {
    if (graph.nodes.length === 0) return;
    setSaving(true);
    setNotice(null);
    try {
      await saveBlueprint({
        name: form.name || "Untitled blueprint",
        description: `${counts.tools} tools · ${counts.knowledge} knowledge sources`,
        model: form.model,
        tools: graph.nodes.filter((node) => node.type === "tool").map((node) => node.id),
        knowledge_base_ids: graph.nodes
          .filter((node) => node.type === "knowledge")
          .map((node) => node.id),
        prompt: form.prompt,
        temperature: form.temperature,
        max_tokens: form.maxTokens,
        metadata: { graph: { nodes: graph.nodes, edges: graph.edges } },
      });
      setNotice("Blueprint published to /api/v1/blueprints/agent");
      loadBlueprints();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-4">
      <PageHeader
        title="Builder"
        description="Compose agent, tool, knowledge and output nodes into a persisted blueprint"
        actions={
          <>
            <select
              value={blueprintId ?? ""}
              onChange={(event) => {
                setBlueprintId(event.target.value || null);
                if (!event.target.value) {
                  graph.reset();
                  setForm(EMPTY_FORM);
                }
              }}
              className={blueprintSelectClass()}
            >
              <option value="">New blueprint</option>
              {(blueprints ?? []).map((blueprint) => (
                <option key={blueprint.id} value={blueprint.id}>
                  {blueprint.name || blueprint.id}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={handleSave}
              disabled={saving || graph.nodes.length === 0}
              className="rounded-lg bg-[var(--ecp-gov)] px-3 py-2 text-xs font-semibold text-[#04121a] transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {saving ? "Publishing…" : "Publish blueprint"}
            </button>
          </>
        }
      />

      {notice && (
        <p className="rounded-lg border border-[var(--ecp-success)]/40 bg-[var(--ecp-success-soft)] px-3 py-2 text-[11px] text-[var(--ecp-success)]">
          {notice}
        </p>
      )}

      <div className="grid gap-4 xl:grid-cols-[220px_minmax(0,1fr)_300px]">
        <Panel className="h-fit">
          <PanelBody>
            <NodePalette />
          </PanelBody>
        </Panel>

        <Panel className="min-w-0">
          <BuilderCanvasSurface
            nodes={graph.nodes}
            edges={graph.edges}
            onNodesChange={graph.onNodesChange}
            onEdgesChange={graph.onEdgesChange}
            onConnect={graph.onConnect}
            onDrop={graph.onDrop}
            onSelect={graph.setSelectedId}
            onClearSelection={() => graph.setSelectedId(null)}
          />
        </Panel>

        <Panel className="h-fit">
          <PanelBody className="space-y-3">
            <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
              Configuration
            </h3>
            {graph.selected ? (
              <NodeInspector
                node={graph.selected}
                onRename={(label) => graph.renameNode(graph.selected!.id, label)}
                onDelete={() => graph.removeNode(graph.selected!.id)}
              />
            ) : (
              <p className="text-[11px] text-[var(--ecp-text-dim)]">
                Select a node on the canvas to edit its label.
              </p>
            )}
            <BlueprintConfigPanel
              form={form}
              models={modelOptions}
              counts={counts}
              onChange={setForm}
            />
          </PanelBody>
        </Panel>
      </div>
    </div>
  );
}