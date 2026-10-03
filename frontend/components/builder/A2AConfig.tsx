'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Link2,
  Plus,
  Trash2,
  ExternalLink,
  Server,
} from 'lucide-react';

interface A2AConfigProps {
  agents: Array<{ id: string; name: string; endpoint: string }>;
  onChange: (agents: A2AConfigProps['agents']) => void;
}

const A2AConfig: React.FC<A2AConfigProps> = ({ agents, onChange }) => {
  const addAgent = () => {
    onChange([...agents, { id: '', name: '', endpoint: '' }]);
  };

  const updateAgent = (index: number, patch: Partial<A2AConfigProps['agents'][number]>) => {
    const updated = agents.map((agent, i) =>
      i === index ? { ...agent, ...patch } : agent
    );
    onChange(updated);
  };

  const removeAgent = (index: number) => {
    onChange(agents.filter((_, i) => i !== index));
  };

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="border-b px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Link2 className="h-5 w-5 text-indigo-600" />
            <span className="font-semibold text-gray-800">A2A Configuration</span>
          </div>
          <Button variant="ghost" size="sm" onClick={addAgent}>
            <Plus className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        {agents.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center text-sm text-gray-500">
            <Link2 className="mb-2 h-8 w-8 text-gray-300" />
            <p>No external agents configured.</p>
            <Button variant="secondary" size="sm" className="mt-3" onClick={addAgent}>
              <Plus className="mr-1 h-4 w-4" />
              Add Agent
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {agents.map((agent, index) => (
              <Card key={index} className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1 space-y-3">
                    <div className="space-y-1">
                      <Label htmlFor={`agent-name-${index}`}>Name</Label>
                      <Input
                        id={`agent-name-${index}`}
                        value={agent.name}
                        onChange={(e) => updateAgent(index, { name: e.target.value })}
                        placeholder="Agent name"
                      />
                    </div>
                    <div className="space-y-1">
                      <Label htmlFor={`agent-endpoint-${index}`}>Endpoint</Label>
                      <Input
                        id={`agent-endpoint-${index}`}
                        value={agent.endpoint}
                        onChange={(e) => updateAgent(index, { endpoint: e.target.value })}
                        placeholder="https://..."
                      />
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-2"
                    onClick={() => removeAgent(index)}
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default A2AConfig;
