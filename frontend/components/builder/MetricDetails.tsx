'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricDetailsProps {
  metric: {
    name: string;
    value: number;
    average: number;
    min: number;
    max: number;
    trend: 'up' | 'down' | 'stable';
  };
}

const MetricDetails: React.FC<MetricDetailsProps> = ({ metric }) => {
  const trendIcon = {
    up: <TrendingUp className="h-4 w-4 text-green-600" />,
    down: <TrendingDown className="h-4 w-4 text-red-600" />,
    stable: <Minus className="h-4 w-4 text-gray-600" />,
  };

  return (
    <Card className="p-4">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-800">{metric.name}</span>
          <Badge variant="secondary">{metric.trend}</Badge>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-md border p-2">
            <div className="text-xs text-gray-500">Current</div>
            <div className="text-lg font-semibold text-gray-900">{metric.value.toFixed(2)}</div>
          </div>
          <div className="rounded-md border p-2">
            <div className="text-xs text-gray-500">Average</div>
            <div className="text-lg font-semibold text-gray-900">{metric.average.toFixed(2)}</div>
          </div>
          <div className="rounded-md border p-2">
            <div className="text-xs text-gray-500">Min</div>
            <div className="text-lg font-semibold text-gray-900">{metric.min.toFixed(2)}</div>
          </div>
          <div className="rounded-md border p-2">
            <div className="text-xs text-gray-500">Max</div>
            <div className="text-lg font-semibold text-gray-900">{metric.max.toFixed(2)}</div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-sm text-gray-600">
          {trendIcon[metric.trend]}
          <span>
            Trend: {metric.trend === 'up' ? 'Improving' : metric.trend === 'down' ? 'Declining' : 'Stable'}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default MetricDetails;
