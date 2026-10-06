'use client';

import { useState } from 'react';
import { BenchmarkScoreGrid } from '@/components/benchmark/benchmark-score-grid';
import { BenchmarkTrendChart } from '@/components/benchmark/benchmark-trend-chart';
import { BenchmarkDetailModal } from '@/components/benchmark/benchmark-detail-modal';

export default function BenchmarkPage() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Benchmark Dashboard</h2>
        <p className="text-sm text-text-secondary">Capability pack scores and benchmark trends.</p>
      </div>

      <BenchmarkScoreGrid onSelect={setSelectedId} />

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Score Trend</h3>
        <BenchmarkTrendChart />
      </section>

      <BenchmarkDetailModal benchmarkId={selectedId} isOpen={!!selectedId} onOpenChange={(open) => !open && setSelectedId(null)} />
    </div>
  );
}
