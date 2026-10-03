'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Server,
  Plus,
  Trash2,
  Check,
  X,
} from 'lucide-react';

interface MCPConnectorProps {
  servers: Array<{ id: string; name: string; endpoint: string; status: string }>;
  onChange: (servers: MCPConnectorProps['servers']) => void;
}

const MCPConnector: React.FC<MCPConnectorProps> = ({ servers, onChange }) => {
  const addServer = () => {
    onChange([...servers, { id: '', name: '', endpoint: '', status: 'disconnected' }]);
  };

  const updateServer = (index: number, patch: Partial<MCPConnectorProps['servers'][number]>) => {
    const updated = servers.map((server, i) =>
      i === index ? { ...server, ...patch } : server
    );
    onChange(updated);
  };

  const removeServer = (index: number) => {
    onChange(servers.filter((_, i) => i !== index));
  };

  const connectServer = (index: number) => {
    updateServer(index, { status: 'connected' });
  };

  const disconnectServer = (index: number) => {
    updateServer(index, { status: 'disconnected' });
  };

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="border-b px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Server className="h-5 w-5 text-green-600" />
            <span className="font-semibold text-gray-800">MCP Servers</span>
          </div>
          <Button variant="ghost" size="sm" onClick={addServer}>
            <Plus className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        {servers.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center text-sm text-gray-500">
            <Server className="mb-2 h-8 w-8 text-gray-300" />
            <p>No MCP servers configured.</p>
            <Button variant="secondary" size="sm" className="mt-3" onClick={addServer}>
              <Plus className="mr-1 h-4 w-4" />
              Add Server
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {servers.map((server, index) => (
              <Card key={index} className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1 space-y-3">
                    <div className="space-y-1">
                      <Label htmlFor={`server-name-${index}`}>Name</Label>
                      <Input
                        id={`server-name-${index}`}
                        value={server.name}
                        onChange={(e) => updateServer(index, { name: e.target.value })}
                        placeholder="Server name"
                      />
                    </div>
                    <div className="space-y-1">
                      <Label htmlFor={`server-endpoint-${index}`}>Endpoint</Label>
                      <Input
                        id={`server-endpoint-${index}`}
                        value={server.endpoint}
                        onChange={(e) => updateServer(index, { endpoint: e.target.value })}
                        placeholder="https://..."
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Badge variant={server.status === 'connected' ? 'default' : 'secondary'}>
                        {server.status}
                      </Badge>
                      <div className="flex items-center gap-1">
                        {server.status === 'connected' ? (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => disconnectServer(index)}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        ) : (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => connectServer(index)}
                          >
                            <Check className="h-4 w-4" />
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeServer(index)}
                        >
                          <Trash2 className="h-4 w-4 text-red-500" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default MCPConnector;
