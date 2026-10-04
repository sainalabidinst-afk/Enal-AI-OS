"use client";

import { useCallback, useState } from "react";
import {
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  ReactFlow,
  ReactFlowProvider,
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  useReactFlow,
  type Connection,
  type Edge,
  type EdgeChange,
  type Node,
  type NodeChange,
  type NodeTypes,
} from "reactflow";
import "reactflow/dist/style.css";
import {
  AgentFlowNode,
  KnowledgeFlowNode,
  OutputFlowNode,
  ToolFlowNode,
  type ConsoleNodeData,
} from "./console-nodes";

const NODE_TYPES: NodeTypes = {
  agent: AgentFlowNode,
  tool: ToolFlowNode,
  knowledge: KnowledgeFlowNode,
  output: OutputFlowNode,
};

export type BuilderNodeKind = "agent" | "tool" | "knowledge" | "output";

export function toneFor(kind: string): ConsoleNodeData["tone"] {
  if (kind === "agent") return "sky";
  if (kind === "tool") return "gov";
  if (kind === "knowledge") return "blue";
  return "alert";
}

export function useBuilderGraph(initial?: { nodes: Node[]; edges: Edge[] }) {
  const [nodes, setNodes] = useState<Node[]>(initial?.nodes ?? []);
  const [edges, setEdges] = useState<Edge[]>(initial?.edges ?? []);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const { screenToFlowPosition } = useReactFlow();

  const onNodesChange = useCallback((changes: NodeChange[]) => {
    setNodes((current) => applyNodeChanges(changes, current));
  }, []);

  const onEdgesChange = useCallback((changes: EdgeChange[]) => {
    setEdges((current) => applyEdgeChanges(changes, current));
  }, []);

  const onConnect = useCallback((connection: Connection) => {
    setEdges((current) => addEdge({ ...connection, animated: true }, current));
  }, []);

  const addNode = useCallback(
    (kind: BuilderNodeKind, position: { x: number; y: number }, label?: string) => {
      const id = `${kind}-${Date.now().toString(36)}`;
      const node: Node = {
        id,
        type: kind as string,
        position,
        data: {
          label: label ?? `${kind} ${nodes.length + 1}`,
          tone: toneFor(kind as string),
        } as ConsoleNodeData,
      };
      setNodes((current) => [...current, node]);
      setSelectedId(id);
      return node;
    },
    [nodes.length]
  );

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const kind = event.dataTransfer.getData("application/ecp-node") as BuilderNodeKind;
      if (!kind || !NODE_TYPES[kind]) return;
      addNode(kind, screenToFlowPosition({ x: event.clientX, y: event.clientY }));
    },
    [addNode, screenToFlowPosition]
  );

  const renameNode = useCallback((id: string, label: string) => {
    setNodes((current) =>
      current.map((node) =>
        node.id === id ? { ...node, data: { ...node.data, label } } : node
      )
    );
  }, []);

  const removeNode = useCallback((id: string) => {
    setNodes((current) => current.filter((node) => node.id !== id));
    setEdges((current) => current.filter((edge) => edge.source !== id && edge.target !== id));
    setSelectedId(null);
  }, []);

  const load = useCallback((next: { nodes: Node[]; edges: Edge[] }) => {
    setNodes(next.nodes);
    setEdges(next.edges);
    setSelectedId(null);
  }, []);

  const reset = useCallback(() => {
    setNodes([]);
    setEdges([]);
    setSelectedId(null);
  }, []);

  const selected = nodes.find((node) => node.id === selectedId) ?? null;

  return {
    nodes,
    edges,
    selected,
    selectedId,
    setSelectedId,
    onNodesChange,
    onEdgesChange,
    onConnect,
    onDrop,
    addNode,
    renameNode,
    removeNode,
    load,
    reset,
  };
}

export function BuilderCanvasSurface({
  nodes,
  edges,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onDrop,
  onSelect,
  onClearSelection,
}: {
  nodes: Node[];
  edges: Edge[];
  onNodesChange: (changes: NodeChange[]) => void;
  onEdgesChange: (changes: EdgeChange[]) => void;
  onConnect: (connection: Connection) => void;
  onDrop: (event: React.DragEvent) => void;
  onSelect: (id: string) => void;
  onClearSelection: () => void;
}) {
  return (
    <div
      className="ecp-flow h-[560px]"
      onDrop={onDrop}
      onDragOver={(event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = "copy";
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={NODE_TYPES}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={(_, node) => onSelect(node.id)}
        onPaneClick={onClearSelection}
        fitView
        snapToGrid
        snapGrid={[16, 16]}
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Dots} gap={22} size={1} color="#223049" />
        <Controls />
        <MiniMap
          pannable
          zoomable
          style={{ background: "#0e1420", border: "1px solid #202b3d" }}
          nodeColor="#2dd4bf"
        />
      </ReactFlow>
    </div>
  );
}

export function BuilderProvider({ children }: { children: React.ReactNode }) {
  return <ReactFlowProvider>{children}</ReactFlowProvider>;
}