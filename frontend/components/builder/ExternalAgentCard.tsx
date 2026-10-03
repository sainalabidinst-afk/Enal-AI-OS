'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Server } from 'lucide-react';

interface ExternalAgentCardProps {
  agent: {
    id: string;
    name: string;
    endpoint: string;
    status: string;
    capabilities: string[];
  };
  onConnect?: () => void;
  onDisconnect?: () => void;
}

const ExternalAgentCard: React.FC<ExternalAgentCardProps> = ({
  agent,
  onConnect,
  onDisconnect,
}) => {
  const isConnected = agent.status === 'connected';

  return (
    <Card className="p-4">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100">
            <Server className="h-5 w-5 text-gray-600" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-900">{agent.name}</h3>
            <p className="text-xs text-gray-500">{agent.endpoint}</p>
          </div>
        </div>
        <Badge variant={isConnected ? 'default' : 'secondary'}>
          {agent.status}
        </Badge>
      </div>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {agent.capabilities.map((cap) => (
          <span
            key={cap}
            className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-600"
          >
            {cap}
          </span>
        ))}
      </div>

      <div className="mt-3 flex items-center gap-2">
        {isConnected ? (
          <Button variant="ghost" size="sm" onClick={onDisconnect}>
            Disconnect
          </Button>
        ) : (
          <Button variant="ghost" size="sm" onClick={onConnect}>
            Connect
          </Button>
        )}
        <Button variant="ghost" size="sm">
          <ExternalLink className="mr-1 h-4 w-4" />
          View
        </Button>
      </div>
    </Card>
  );
};

export default ExternalAgentCard;
