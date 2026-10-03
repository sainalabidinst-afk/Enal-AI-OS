'use client';

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { GitBranch, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';

const ConditionalNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div
      className={`rounded-md border-2 bg-white px-4 py-3 shadow-sm ${
        selected ? 'border-orange-500' : 'border-orange-200'
      }`}
    >
      <Handle type="target" position={Position.Top} className="h-2 w-2" />
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <GitBranch className="h-4 w-4 text-orange-600" />
          <span className="text-sm font-semibold text-gray-800">
            {data.label as string || 'If / Else'}
          </span>
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
          <Settings className="h-3 w-3" />
        </Button>
      </div>
      <div className="mt-2 text-xs text-gray-500">
        {(data.condition as string) || 'condition'}
      </div>
      <Handle
        type="source"
        position={Position.Bottom}
        id="true"
        className="h-2 w-2"
        style={{ left: '30%' }}
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="false"
        className="h-2 w-2"
        style={{ left: '70%' }}
      />
    </div>
  );
};

export default ConditionalNode;
