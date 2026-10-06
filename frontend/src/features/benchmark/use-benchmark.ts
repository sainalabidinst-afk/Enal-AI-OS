'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { runBenchmark, getBenchmarkSuite, getBenchmarkHistory } from '@/services/benchmark';
import { useBenchmarkStore } from '@/features/benchmark/benchmark-store';
import type { BenchmarkResult } from '@/types/benchmark';

export function useBenchmark() {
  const queryClient = useQueryClient();
  const setResults = useBenchmarkStore((state) => state.setResults);
  const setHeuristicScores = useBenchmarkStore((state) => state.setHeuristicScores);

  const runMutation = useMutation({
    mutationFn: runBenchmark as () => Promise<{ results?: BenchmarkResult[] }>,
    onSuccess: (data) => {
      setResults(data.results ?? []);
      setHeuristicScores(data.results ?? []);
      queryClient.invalidateQueries({ queryKey: ['benchmark'] });
    },
  });

  const { data: history, isLoading } = useQuery({
    queryKey: ['benchmark', 'history'],
    queryFn: getBenchmarkHistory,
  });

  return {
    run: runMutation.mutate,
    isRunning: runMutation.isPending,
    history: history ?? [],
    isLoadingHistory: isLoading,
  };
}
