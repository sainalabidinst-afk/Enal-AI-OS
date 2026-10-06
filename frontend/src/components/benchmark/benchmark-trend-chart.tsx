'use client';

import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function BenchmarkTrendChart() {
  const { data, isLoading } = useQuery({
    queryKey: ['benchmark', 'history'],
    queryFn: () => apiClient.get('/api/v1/benchmark/history'),
  });

  const chartData = useMemo(() => {
    if (!Array.isArray(data)) return [];
    return data.map((item: { id: string; avg_score?: number; created_at?: string }) => ({
      id: item.id,
      score: item.avg_score ?? 0,
      date: item.created_at ? new Date(item.created_at).toLocaleDateString() : 'Unknown',
    }));
  }, [data]);

  if (isLoading) return <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />;

  return (
    <div className="mt-4 h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="date" stroke="var(--color-text-muted)" fontSize={12} />
          <YAxis domain={[0, 1]} stroke="var(--color-text-muted)" fontSize={12} />
          <Tooltip
            contentStyle={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)' }}
            labelStyle={{ color: 'var(--color-text-primary)' }}
          />
          <Line type="monotone" dataKey="score" stroke="var(--color-primary)" strokeWidth={2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
