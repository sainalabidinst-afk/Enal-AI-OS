'use client';

import React, { useCallback, useEffect } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  Connection,
  NodeTypes,
  BackgroundVariant,
} from 'reactflow';
import 'reactflow/dist/style.css';

import BuilderToolbar from './BuilderToolbar';
import AgentNode from './AgentNode';
import ToolNode from './ToolNode';
import KnowledgeBaseNode from './KnowledgeBaseNode';
import ConditionalNode from './ConditionalNode';
import DelayNode from './DelayNode';

const nodeTypes: NodeTypes = {
  agent: AgentNode,
  tool: ToolNode,
  knowledgeBase: KnowledgeBaseNode,
  conditional: ConditionalNode,
  delay: DelayNode,
};

export type BlueprintNodeData = Record<string, unknown>;

interface BuilderCanvasProps {
  initialNodes?: Node<BlueprintNodeData>[];
  initialEdges?: Edge[];
  onNodesChange?: (nodes: Node<BlueprintNodeData>[]) => void;
  onEdgesChange?: (edges: Edge[]) => void;
}

const BuilderCanvas: React.FC<BuilderCanvasProps> = ({
  initialNodes = [],
  initialEdges = [],
  onNodesChange,
  onEdgesChange,
}) => {
  const [nodes, setNodes, onNodesChangeInternal] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChangeInternal] = useEdgesState(initialEdges);

  useEffect(() => {
    onNodesChange?.(nodes);
  }, [nodes, onNodesChange]);

  useEffect(() => {
    onEdgesChange?.(edges);
  }, [edges, onEdgesChange]);

  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) => addEdge({ ...connection, animated: true }, eds));
    },
    [setEdges]
  );

  return (
    <div className="flex h-screen w-full flex-col">
      <BuilderToolbar />
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChangeInternal}
          onEdgesChange={onEdgesChangeInternal}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[16, 16]}
        >
          <Background variant={BackgroundVariant.Dots} gap={16} size={1} />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>
    </div>
  );
};

export default BuilderCanvas;
