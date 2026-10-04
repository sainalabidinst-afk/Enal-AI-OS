"use client";

import { Bot, CircleDot, Database, Wrench } from "lucide-react";
import { Handle, Position, type NodeProps } from "reactflow";
import { cn } from "@/lib/utils";

export interface ConsoleNodeData {
  label: string;
  caption?: string;
  tone?: "sky" | "gov" | "alert" | "blue" | "neutral";
  status?: string;
}

const TONES: Record<string, { border: string; text: string; bg: string }> = {
  sky: { border: "rgba(56,189,248,0.45)", text: "#38bdf8", bg: "rgba(56,189,248,0.10)" },
  gov: { border: "rgba(45,212,191,0.45)", text: "#2dd4bf", bg: "rgba(45,212,191,0.10)" },
  alert: { border: "rgba(245,158,11,0.45)", text: "#f59e0b", bg: "rgba(245,158,11,0.10)" },
  blue: { border: "rgba(59,130,246,0.45)", text: "#3b82f6", bg: "rgba(59,130,246,0.10)" },
  neutral: { border: "#2b3950", text: "#93a1b8", bg: "rgba(255,255,255,0.03)" },
};

function Frame({
  data,
  selected,
  icon,
}: {
  data: ConsoleNodeData;
  selected?: boolean;
  icon: React.ReactNode;
}) {
  const tone = TONES[data.tone ?? "neutral"];
  return (
    <div
      className={cn(
        "min-w-[160px] rounded-lg border px-3 py-2 shadow-lg backdrop-blur",
        selected && "ring-2 ring-[var(--ecp-gov)]"
      )}
      style={{ borderColor: tone.border, background: tone.bg }}
    >
      <Handle type="target" position={Position.Left} />
      <div className="flex items-center gap-2">
        <span style={{ color: tone.text }}>{icon}</span>
        <span className="truncate text-xs font-semibold text-[#e7ecf6]">{data.label}</span>
      </div>
      {data.caption && (
        <p className="mt-1 truncate text-[10px] text-[#93a1b8]">{data.caption}</p>
      )}
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

export function AgentFlowNode({ data, selected }: NodeProps) {
  const node = data as unknown as ConsoleNodeData;
  return <Frame data={node} selected={selected} icon={<Bot className="h-3.5 w-3.5" />} />;
}

export function ToolFlowNode({ data, selected }: NodeProps) {
  const node = data as unknown as ConsoleNodeData;
  return <Frame data={node} selected={selected} icon={<Wrench className="h-3.5 w-3.5" />} />;
}

export function KnowledgeFlowNode({ data, selected }: NodeProps) {
  const node = data as unknown as ConsoleNodeData;
  return <Frame data={node} selected={selected} icon={<Database className="h-3.5 w-3.5" />} />;
}

export function OutputFlowNode({ data, selected }: NodeProps) {
  const node = data as unknown as ConsoleNodeData;
  return <Frame data={node} selected={selected} icon={<CircleDot className="h-3.5 w-3.5" />} />;
}