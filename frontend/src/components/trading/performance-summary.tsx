'use client';

import { MetricsCard } from '@/components/shared/metrics-card';

export function PerformanceSummary() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <MetricsCard title="Win Rate" value="64.2%" change="+3.1%" trend="up" />
      <MetricsCard title="Net Profit" value="+12.4%" change="+1.2%" trend="up" />
      <MetricsCard title="Max Drawdown" value="-4.8%" change="-0.6%" trend="up" />
    </div>
  );
}
