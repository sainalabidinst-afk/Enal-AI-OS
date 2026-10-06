'use client';

import { PerformanceSummary } from '@/components/trading/performance-summary';
import { MarketFeedWidget } from '@/components/dashboard/market-feed-widget';
import { StrategyPanel } from '@/components/trading/strategy-panel';
import { TradeHistoryTable } from '@/components/trading/trade-history-table';
import { RegimeBadge } from '@/components/trading/regime-badge';
import { BacktestingModule } from '@/components/trading/backtesting-module';

export default function TradingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Trading Intelligence</h2>
        <p className="text-sm text-text-secondary">Multi-timeframe market analysis and strategy performance.</p>
      </div>

      <PerformanceSummary />

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Market Chart</h3>
          <p className="text-xs text-text-secondary">Candlestick multi-timeframe: 15m, 1h, 4h, 1d</p>
          <MarketFeedWidget symbol="BTCUSDT" />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Strategy Panel</h3>
          <StrategyPanel />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Trade History</h3>
          <p className="text-xs text-text-secondary">Entry/exit log for recent trades.</p>
          <TradeHistoryTable />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Market Regime</h3>
          <RegimeBadge symbol="BTCUSDT" />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Backtesting</h3>
        <BacktestingModule symbol="BTCUSDT" />
      </section>
    </div>
  );
}
