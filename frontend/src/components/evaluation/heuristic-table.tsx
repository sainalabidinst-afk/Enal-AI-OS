'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';

const heuristics = [
  { key: 'scalability', label: 'Scalability' },
  { key: 'cost', label: 'Cost' },
  { key: 'compliance', label: 'Compliance' },
  { key: 'observability', label: 'Observability' },
  { key: 'security', label: 'Security' },
  { key: 'accuracy', label: 'Accuracy' },
  { key: 'coherence', label: 'Coherence' },
  { key: 'completeness', label: 'Completeness' },
  { key: 'relevance', label: 'Relevance' },
];

export function HeuristicTable() {
  const { data } = useQuery({
    queryKey: ['benchmark', 'scores'],
    queryFn: () => apiClient.get('/api/v1/benchmark/capability-scores'),
  });

  return (
    <div className="mt-4 space-y-3">
      {heuristics.map((item) => (
        <div key={item.key} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <span className="text-sm">{item.label}</span>
          <StatusBadge status="success" label={typeof data?.[item.key] === 'number' ? `${Math.round(data[item.key] * 100)}%` : 'Pass'} />
        </div>
      ))}
    </div>
  );
}
