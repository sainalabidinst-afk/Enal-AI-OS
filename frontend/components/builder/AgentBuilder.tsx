'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import BuilderCanvas from '@/components/builder/BuilderCanvas';
import AgentConfigPanel from '@/components/builder/AgentConfigPanel';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Play, MessageSquare, ArrowLeft } from 'lucide-react';
import { Node, Edge } from 'reactflow';

interface AgentFormData {
  name: string;
  description: string;
  model: string;
  tools: string[];
  knowledgeBaseIds: string[];
  prompt: string;
  temperature: number;
  maxTokens: number;
}

const defaultAgent: AgentFormData = {
  name: '',
  description: '',
  model: 'gpt-4o',
  tools: [],
  knowledgeBaseIds: [],
  prompt: '',
  temperature: 0.7,
  maxTokens: 1024,
};

const availableTools = [
  { id: 'web_search', name: 'Web Search' },
  { id: 'file_read', name: 'File Read' },
  { id: 'file_write', name: 'File Write' },
  { id: 'email_send', name: 'Email Send' },
  { id: 'calendar', name: 'Calendar' },
  { id: 'database_query', name: 'Database Query' },
];

const availableKnowledgeBases = [
  { id: 'kb_docs', name: 'Documents' },
  { id: 'kb_policies', name: 'Policies' },
  { id: 'kb_products', name: 'Products' },
  { id: 'kb_faq', name: 'FAQ' },
];

const AgentBuilder: React.FC = () => {
  const router = useRouter();
  const [agent, setAgent] = useState<AgentFormData>(defaultAgent);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [isRunning, setIsRunning] = useState(false);

  const handleSave = useCallback(async () => {
    setIsSaving(true);
    try {
      const payload = {
        ...agent,
        nodes,
        edges,
      };
      const response = await fetch('/api/v1/blueprints/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error('Failed to save agent');
      }
      const result = await response.json();
      alert(`Agent saved: ${result.id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to save agent');
    } finally {
      setIsSaving(false);
    }
  }, [agent, nodes, edges]);

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    try {
      const response = await fetch('/api/v1/blueprints/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...agent, nodes, edges }),
      });
      if (!response.ok) {
        throw new Error('Failed to run agent');
      }
      const result = await response.json();
      alert(`Agent executed: ${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      console.error(error);
      alert('Failed to run agent');
    } finally {
      setIsRunning(false);
    }
  }, [agent, nodes, edges]);

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50">
      <header className="flex items-center justify-between border-b bg-white px-4 py-2">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => router.back()}>
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Button>
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-blue-600" />
            <h1 className="text-lg font-semibold text-gray-800">Agent Builder</h1>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleSave}
            disabled={isSaving}
          >
            <span className="mr-1 h-4 w-4">💾</span>
            {isSaving ? 'Saving...' : 'Save'}
          </Button>
          <Button size="sm" onClick={handleRun} disabled={isRunning}>
            <Play className="mr-1 h-4 w-4" />
            {isRunning ? 'Running...' : 'Run'}
          </Button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1">
          <BuilderCanvas
            initialNodes={nodes}
            initialEdges={edges}
            onNodesChange={setNodes}
            onEdgesChange={setEdges}
          />
        </div>
        <AgentConfigPanel
          agent={agent}
          onChange={setAgent}
          onSave={handleSave}
          onRun={handleRun}
          availableTools={availableTools}
          availableKnowledgeBases={availableKnowledgeBases}
        />
      </div>
    </div>
  );
};

export default AgentBuilder;
