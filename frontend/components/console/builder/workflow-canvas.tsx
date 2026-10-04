"use client";

import { useMemo } from "react";
import {
  Background,
  BackgroundVariant,
  Controls,
  ReactFlow,
  type NodeTypes,
} from "reactflow";
import "reactflow/dist/style.css";
import { AgentFlowNode, KnowledgeFlowNode, OutputFlowNode, ToolFlowNode } from "./console-nodes";
import { blueprintToGraph, emptyGraph } from "./blueprint-graph";
import type { BlueprintResponse } from "@/services/console/builder";

const NODE_TYPES: NodeTypes = {
  agent: AgentFlowNode,
  tool: ToolFlowNode,
  knowledge: KnowledgeFlowNode,
  output: OutputFlowNode,
};

export function WorkflowCanvas({
  blueprint,
  height = 300,
  emptyLabel = "Select a blueprint to render its pipeline",
}: {
  blueprint: BlueprintResponse | null;
  height?: number;
  emptyLabel?: string;
}) {
  const graph = useMemo(
    () => (blueprint ? blueprintToGraph(blueprint) : emptyGraph()),
    [blueprint]
  );

  if (!blueprint) {
    return (
      <div
        style={{ height }}
        className="ecp-flow grid place-items-center rounded-lg border border-dashed border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] text-xs text-[var(--ecp-text-dim)]"
      >
        {emptyLabel}
      </div>
    );
  }

  return (
    <div
      style={{ height }}
      className="ecp-flow overflow-hidden rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)]"
    >
      <ReactFlow
        nodes={graph.nodes}
        edges={graph.edges}
        nodeTypes={NODE_TYPES}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Dots} gap={22} size={1} color="#223049" />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}