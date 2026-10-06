'use client';

import { PackList } from '@/components/capability-packs/pack-list';
import { PackDetailPanel } from '@/components/capability-packs/pack-detail-panel';
import { DependencyGraphViewer } from '@/components/capability-packs/dependency-graph-viewer';
import { useState } from 'react';

export default function CapabilityPacksPage() {
  const [selectedPackId, setSelectedPackId] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Capability Packs</h2>
        <p className="text-sm text-text-secondary">Registered packs and capability registry.</p>
      </div>

      <PackList onSelect={setSelectedPackId} />

      {selectedPackId && (
        <section className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Capability Detail</h3>
          <PackDetailPanel packId={selectedPackId} />
        </section>
      )}

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Dependency Graph</h3>
        <DependencyGraphViewer />
      </section>
    </div>
  );
}
