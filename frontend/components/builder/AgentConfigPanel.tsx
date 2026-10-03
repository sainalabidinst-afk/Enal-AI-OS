'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { Select } from '@/components/ui/select';
import {
  Bot,
  Save,
  Play,
  Trash2,
  Plus,
  BookOpen,
  Wrench,
} from 'lucide-react';

interface AgentConfigPanelProps {
  agent: {
    id?: string;
    name: string;
    description: string;
    model: string;
    tools: string[];
    knowledgeBaseIds: string[];
    prompt: string;
    temperature: number;
    maxTokens: number;
  };
  onChange: (agent: AgentConfigPanelProps['agent']) => void;
  onSave?: () => void;
  onRun?: () => void;
  onDelete?: () => void;
  availableTools: Array<{ id: string; name: string }>;
  availableKnowledgeBases: Array<{ id: string; name: string }>;
}

const modelOptions = [
  { value: 'gpt-4o', label: 'GPT-4o' },
  { value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
  { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
  { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet' },
  { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
];

const AgentConfigPanel: React.FC<AgentConfigPanelProps> = ({
  agent,
  onChange,
  onSave,
  onRun,
  onDelete,
  availableTools,
  availableKnowledgeBases,
}) => {
  const update = (patch: Partial<AgentConfigPanelProps['agent']>) => {
    onChange({ ...agent, ...patch });
  };

  const tabs = [
    { id: 'general', label: 'General' },
    { id: 'model', label: 'Model' },
    { id: 'tools', label: 'Tools' },
    { id: 'knowledge', label: 'KB' },
  ];

  const [activeTab, setActiveTab] = React.useState('general');

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="flex items-center justify-between border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-blue-600" />
          <span className="font-semibold text-gray-800">Agent Configuration</span>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="sm" onClick={onDelete}>
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={onSave}>
            <Save className="h-4 w-4" />
          </Button>
          <Button size="sm" onClick={onRun}>
            <Play className="mr-1 h-4 w-4" />
            Run
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

        {activeTab === 'general' && (
          <div className="mt-4 space-y-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <Input
                value={agent.name}
                onChange={(e) => update({ name: e.target.value })}
                placeholder="My Agent"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                value={agent.description}
                onChange={(e) => update({ description: e.target.value })}
                placeholder="What does this agent do?"
                rows={3}
                className="flex min-h-[60px] w-full rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">System Prompt</label>
              <textarea
                value={agent.prompt}
                onChange={(e) => update({ prompt: e.target.value })}
                placeholder="You are a helpful assistant..."
                rows={8}
                className="flex min-h-[60px] w-full rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2 font-mono"
              />
            </div>
          </div>
        )}

        {activeTab === 'model' && (
          <div className="mt-4 space-y-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Model</label>
              <Select
                id="model"
                label=""
                value={agent.model}
                onChange={(e) => update({ model: e.target.value })}
                options={modelOptions}
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Temperature: {agent.temperature.toFixed(1)}
              </label>
              <input
                type="range"
                min={0}
                max={2}
                step={0.1}
                value={agent.temperature}
                onChange={(e) => update({ temperature: parseFloat(e.target.value) })}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Max Tokens</label>
              <Input
                type="number"
                value={agent.maxTokens}
                onChange={(e) => update({ maxTokens: parseInt(e.target.value, 10) || 1024 })}
              />
            </div>
          </div>
        )}

        {activeTab === 'tools' && (
          <div className="mt-4 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Tools</label>
              <Button variant="ghost" size="sm">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-2">
              {availableTools.map((tool) => (
                <div key={tool.id} className="flex items-center gap-2">
                  <Checkbox
                    id={`tool-${tool.id}`}
                    label={tool.name}
                    checked={agent.tools.includes(tool.id)}
                    onChange={(e) => {
                      const tools = e.target.checked
                        ? [...agent.tools, tool.id]
                        : agent.tools.filter((id) => id !== tool.id);
                      update({ tools });
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'knowledge' && (
          <div className="mt-4 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Knowledge Bases</label>
              <Button variant="ghost" size="sm">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-2">
              {availableKnowledgeBases.map((kb) => (
                <div key={kb.id} className="flex items-center gap-2">
                  <Checkbox
                    id={`kb-${kb.id}`}
                    label={kb.name}
                    checked={agent.knowledgeBaseIds.includes(kb.id)}
                    onChange={(e) => {
                      const knowledgeBaseIds = e.target.checked
                        ? [...agent.knowledgeBaseIds, kb.id]
                        : agent.knowledgeBaseIds.filter((id) => id !== kb.id);
                      update({ knowledgeBaseIds });
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentConfigPanel;
