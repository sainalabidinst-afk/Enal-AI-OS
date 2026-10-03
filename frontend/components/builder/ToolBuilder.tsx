'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import BuilderCanvas from '@/components/builder/BuilderCanvas';
import StepConfigPanel from '@/components/builder/StepConfigPanel';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Play, Wrench, ArrowLeft } from 'lucide-react';
import { Node, Edge } from 'reactflow';

interface StepFormData {
  id?: string;
  type: string;
  label: string;
  config: Record<string, unknown>;
}

const defaultStep: StepFormData = {
  id: '',
  type: 'llm_call',
  label: '',
  config: {},
};

const stepTypes = [
  { value: 'llm_call', label: 'LLM Call' },
  { value: 'python_code', label: 'Python Code' },
  { value: 'api_call', label: 'API Call' },
  { value: 'kb_search', label: 'KB Search' },
  { value: 'web_scraper', label: 'Web Scraper' },
  { value: 'conditional', label: 'Conditional' },
  { value: 'delay', label: 'Delay' },
];

const ToolBuilder: React.FC = () => {
  const router = useRouter();
  const [tool, setTool] = useState({
    id: undefined as string | undefined,
    name: '',
    description: '',
  });
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedStep, setSelectedStep] = useState<StepFormData | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isRunning, setIsRunning] = useState(false);

  const handleSave = useCallback(async () => {
    setIsSaving(true);
    try {
      const payload = {
        ...tool,
        steps: nodes.map((node) => ({
          id: node.id,
          type: node.data?.type || 'llm_call',
          label: node.data?.label || node.id,
          config: node.data?.config || {},
        })),
        edges,
      };
      const response = await fetch('/api/v1/blueprints/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error('Failed to save tool');
      }
      const result = await response.json();
      alert(`Tool saved: ${result.id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to save tool');
    } finally {
      setIsSaving(false);
    }
  }, [tool, nodes, edges]);

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    try {
      const response = await fetch('/api/v1/blueprints/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...tool,
          steps: nodes.map((node) => ({
            id: node.id,
            type: node.data?.type || 'llm_call',
            label: node.data?.label || node.id,
            config: node.data?.config || {},
          })),
          edges,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to run tool');
      }
      const result = await response.json();
      alert(`Tool executed: ${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      console.error(error);
      alert('Failed to run tool');
    } finally {
      setIsRunning(false);
    }
  }, [tool, nodes, edges]);

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50">
      <header className="flex items-center justify-between border-b bg-white px-4 py-2">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => router.back()}>
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Button>
          <div className="flex items-center gap-2">
            <Wrench className="h-5 w-5 text-green-600" />
            <h1 className="text-lg font-semibold text-gray-800">Tool Builder</h1>
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
        <StepConfigPanel
          step={selectedStep}
          onChange={setSelectedStep}
          onSave={handleSave}
          onRun={handleRun}
          stepTypes={stepTypes}
        />
      </div>
    </div>
  );
};

export default ToolBuilder;
