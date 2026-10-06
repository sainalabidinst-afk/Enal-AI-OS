'use client';

import { StatusBadge } from '@/components/shared/status-badge';

const strategies = [
  { name: 'RSI', status: 'active' as const },
  { name: 'EMA Cross', status: 'active' as const },
  { name: 'MACD', status: 'paused' as const },
];

export function StrategyPanel() {
  return (
    <div className="space-y-3">
      {strategies.map((strategy) => (
        <div key={strategy.name} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <span className="text-sm">{strategy.name}</span>
          <StatusBadge status={strategy.status === 'active' ? 'success' : 'warning'} label={strategy.status === 'active' ? 'Active' : 'Paused'} />
        </div>
      ))}
    </div>
  );
}
