import type { Edge, Node } from "reactflow";
import type { BlueprintResponse } from "@/services/console/builder";

export interface BlueprintGraph {
  nodes: Node[];
  edges: Edge[];
}

const COLUMN = 260;
const ROW = 92;

/** Projects an agent blueprint onto a canvas graph. */
export function blueprintToGraph(blueprint: BlueprintResponse): BlueprintGraph {
  const stored = blueprint.metadata?.graph as
    | { nodes?: Node[]; edges?: Edge[] }
    | undefined;
  if (stored?.nodes?.length) {
    return { nodes: stored.nodes, edges: stored.edges ?? [] };
  }

  const nodes: Node[] = [
    {
      id: "input",
      type: "knowledge",
      position: { x: 0, y: ROW * 1.5 },
      data: { label: "User Input", caption: blueprint.model || "model unset", tone: "neutral" },
    },
    {
      id: "agent",
      type: "agent",
      position: { x: COLUMN, y: ROW * 1.5 },
      data: {
        label: blueprint.name || blueprint.id,
        caption: `${blueprint.model} · temp ${blueprint.temperature} · ${blueprint.max_tokens} tokens`,
        tone: "sky",
      },
    },
  ];

  const edges: Edge[] = [
    { id: "input-agent", source: "input", target: "agent", animated: true },
  ];

  const tools = blueprint.tools ?? [];
  tools.forEach((tool, index) => {
    const id = `tool-${index}`;
    nodes.push({
      id,
      type: "tool",
      position: { x: COLUMN * 2, y: index * ROW },
      data: { label: tool, tone: "gov" },
    });
    edges.push({ id: `agent-${id}`, source: "agent", target: id });
  });

  const knowledge = blueprint.knowledge_base_ids ?? [];
  knowledge.forEach((entry, index) => {
    const id = `kb-${index}`;
    nodes.push({
      id,
      type: "knowledge",
      position: { x: 0, y: ROW * 3 + index * ROW },
      data: { label: entry, tone: "blue" },
    });
    edges.push({ id: `${id}-agent`, source: id, target: "agent" });
  });

  nodes.push({
    id: "output",
    type: "output",
    position: { x: COLUMN * 3, y: Math.max(ROW * 1.5, (tools.length * ROW) / 2) },
    data: {
      label: "Response",
      caption: blueprint.description?.slice(0, 48) || "agent output",
      tone: "alert",
    },
  });

  const tail = tools.length ? `tool-${tools.length - 1}` : "agent";
  edges.push({ id: `${tail}-output`, source: tail, target: "output", animated: true });

  return { nodes, edges };
}

export function emptyGraph(): BlueprintGraph {
  return { nodes: [], edges: [] };
}