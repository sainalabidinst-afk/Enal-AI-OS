'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { BenchmarkRunner } from '@/components/evaluation/benchmark-runner';
import { HeuristicTable } from '@/components/evaluation/heuristic-table';
import { ImprovementList } from '@/components/evaluation/improvement-list';
import { BenchmarkHistory } from '@/components/evaluation/benchmark-history';

export default function EvaluationPage() {
  const { data: scores, isLoading: scoresLoading } = useQuery({
    queryKey: ['benchmark', 'scores'],
    queryFn: () => apiClient.get('/api/v1/benchmark/capability-scores'),
  });

  return (
    <div className="space-y-6">
      <BenchmarkRunner />

      <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricsCard title="Scalability" value={scoresLoading ? '-' : '0.82'} />
        <MetricsCard title="Cost" value={scoresLoading ? '-' : '0.70'} />
        <MetricsCard title="Compliance" value={scoresLoading ? '-' : '0.78'} />
        <MetricsCard title="Observability" value={scoresLoading ? '-' : '0.86'} />
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Heuristic Breakdown</h3>
          <HeuristicTable />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Improvements</h3>
          <ImprovementList />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Benchmark History</h3>
        <BenchmarkHistory />
      </section>
    </div>
  );
}
