'use client';

import { StatusBadge } from '@/components/shared/status-badge';

const trades = [
  { id: 1, pair: 'BTCUSDT', side: 'Long', pnl: '+2.1%', time: '2026-10-06 14:30 UTC' },
  { id: 2, pair: 'ETHUSDT', side: 'Short', pnl: '+1.4%', time: '2026-10-06 13:15 UTC' },
  { id: 3, pair: 'BTCUSDT', side: 'Long', pnl: '-0.8%', time: '2026-10-06 12:00 UTC' },
];

export function TradeHistoryTable() {
  return (
    <div className="mt-4 space-y-2">
      {trades.map((trade) => (
        <div key={trade.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{trade.pair} {trade.side} #{trade.id}</p>
            <p className="text-xs text-text-muted">{trade.time}</p>
          </div>
          <StatusBadge status={trade.pnl.startsWith('+') ? 'success' : 'danger'} label={trade.pnl} />
        </div>
      ))}
    </div>
  );
}
