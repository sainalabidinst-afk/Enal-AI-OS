'use client';

import { ProviderCardGrid } from '@/components/marketplace/provider-card-grid';
import { ProviderHealthMonitor } from '@/components/marketplace/provider-health-monitor';

export default function MarketplacePage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Marketplace</h2>
        <p className="text-sm text-text-secondary">Model providers and health status.</p>
      </div>

      <ProviderCardGrid />

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Provider Health Monitor</h3>
        <ProviderHealthMonitor />
      </section>
    </div>
  );
}
