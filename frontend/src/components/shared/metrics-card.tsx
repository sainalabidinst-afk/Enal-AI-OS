'use client';

import { cn } from '@/lib/cn';

interface MetricsCardProps {
  title: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
  className?: string;
}

export function MetricsCard({ title, value, change, trend = 'neutral', className }: MetricsCardProps) {
  const trendColor =
    trend === 'up'
      ? 'text-success'
      : trend === 'down'
        ? 'text-danger'
        : 'text-text-secondary';

  return (
    <div className={cn('rounded-lg border border-border bg-surface-secondary p-4', className)}>
      <p className="text-sm text-text-secondary">{title}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
      {change && <p className={cn('mt-1 text-xs', trendColor)}>{change}</p>}
    </div>
  );
}
