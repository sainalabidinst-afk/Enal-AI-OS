'use client';

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Clock, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';

const DelayNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div
      className={`rounded-md border-2 bg-white px-4 py-3 shadow-sm ${
        selected ? 'border-gray-500' : 'border-gray-200'
      }`}
    >
      <Handle type="target" position={Position.Top} className="h-2 w-2" />
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-gray-600" />
          <span className="text-sm font-semibold text-gray-800">
            {data.label as string || 'Delay'}
          </span>
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
          <Settings className="h-3 w-3" />
        </Button>
      </div>
      <div className="mt-2 text-xs text-gray-500">
        {(data.delay as string) || '0s'}
      </div>
      <Handle type="source" position={Position.Bottom} className="h-2 w-2" />
    </div>
  );
};

export default DelayNode;
