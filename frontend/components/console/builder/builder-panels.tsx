"use client";

import { Bot, CircleDot, Database, Wrench } from "lucide-react";
import { Field, inputClass, selectClass } from "@/components/console/ui/controls";
import { Pill } from "@/components/console/ui/states";
import type { Node } from "reactflow";
import type { ConsoleNodeData } from "./console-nodes";
import type { BuilderNodeKind } from "./builder-canvas";

export interface PaletteEntry {
  kind: BuilderNodeKind;
  label: string;
  hint: string;
  icon: React.ReactNode;
  color: string;
}

export const PALETTE: PaletteEntry[] = [
  {
    kind: "agent",
    label: "Agent",
    hint: "LLM step with model + temperature",
    icon: <Bot className="h-4 w-4" />,
    color: "#38bdf8",
  },
  {
    kind: "tool",
    label: "Tool",
    hint: "Capability or connector call",
    icon: <Wrench className="h-4 w-4" />,
    color: "#2dd4bf",
  },
  {
    kind: "knowledge",
    label: "Knowledge",
    hint: "Retrieval source",
    icon: <Database className="h-4 w-4" />,
    color: "#3b82f6",
  },
  {
    kind: "output",
    label: "Output",
    hint: "Terminal response",
    icon: <CircleDot className="h-4 w-4" />,
    color: "#f59e0b",
  },
];

export interface BlueprintForm {
  name: string;
  model: string;
  prompt: string;
  temperature: number;
  maxTokens: number;
}

export function NodePalette() {
  return (
    <div className="space-y-2">
      <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
        Node palette
      </h3>
      {PALETTE.map((entry) => (
        <div
          key={entry.kind}
          draggable
          onDragStart={(event) =>
            event.dataTransfer.setData("application/ecp-node", entry.kind)
          }
          className="flex cursor-grab items-start gap-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-2.5 py-2 transition-colors hover:border-[var(--ecp-border-strong)] active:cursor-grabbing"
        >
          <span style={{ color: entry.color }}>{entry.icon}</span>
          <span className="min-w-0">
            <span className="block text-[11px] font-medium">{entry.label}</span>
            <span className="block text-[10px] text-[var(--ecp-text-dim)]">{entry.hint}</span>
          </span>
        </div>
      ))}
      <p className="pt-1 text-[10px] text-[var(--ecp-text-dim)]">
        Drag a node onto the canvas, then connect handles to build the pipeline.
      </p>
    </div>
  );
}

export function NodeInspector({
  node,
  onRename,
  onDelete,
}: {
  node: Node;
  onRename: (label: string) => void;
  onDelete: () => void;
}) {
  const data = node.data as ConsoleNodeData;
  return (
    <div className="space-y-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-2.5">
      <div className="flex items-center justify-between">
        <Pill tone="info">{node.type}</Pill>
        <button
          type="button"
          onClick={onDelete}
          className="text-[11px] text-[var(--ecp-text-dim)] transition-colors hover:text-[var(--ecp-danger)]"
        >
          remove
        </button>
      </div>
      <Field label="Node label">
        <input
          value={data.label}
          onChange={(event) => onRename(event.target.value)}
          className={inputClass()}
        />
      </Field>
    </div>
  );
}

export function BlueprintConfigPanel({
  form,
  models,
  counts,
  onChange,
}: {
  form: BlueprintForm;
  models: string[];
  counts: { tools: number; knowledge: number; nodes: number };
  onChange: (next: BlueprintForm) => void;
}) {
  return (
    <div className="space-y-3 border-t border-[var(--ecp-border)] pt-3">
      <Field label="Blueprint name">
        <input
          value={form.name}
          onChange={(event) => onChange({ ...form, name: event.target.value })}
          className={inputClass()}
        />
      </Field>
      <Field label="Model">
        <input
          value={form.model}
          onChange={(event) => onChange({ ...form, model: event.target.value })}
          list="builder-models"
          placeholder="provider model id"
          className={inputClass()}
        />
        <datalist id="builder-models">
          {models.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>
      </Field>
      <Field label="System prompt">
        <textarea
          value={form.prompt}
          onChange={(event) => onChange({ ...form, prompt: event.target.value })}
          rows={3}
          className={inputClass()}
        />
      </Field>
      <div className="grid grid-cols-2 gap-3">
        <Field label="Temperature">
          <input
            type="number"
            step="0.05"
            min="0"
            max="2"
            value={form.temperature}
            onChange={(event) =>
              onChange({ ...form, temperature: Number(event.target.value) })
            }
            className={inputClass()}
          />
        </Field>
        <Field label="Max tokens">
          <input
            type="number"
            step="64"
            value={form.maxTokens}
            onChange={(event) =>
              onChange({ ...form, maxTokens: Number(event.target.value) })
            }
            className={inputClass()}
          />
        </Field>
      </div>
      <div className="flex flex-wrap gap-1.5">
        <Pill tone="info">{counts.tools} tools</Pill>
        <Pill tone="info">{counts.knowledge} knowledge</Pill>
        <Pill tone="neutral">{counts.nodes} nodes</Pill>
      </div>
    </div>
  );
}

export function blueprintSelectClass() {
  return selectClass();
}