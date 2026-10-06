'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { runBenchmark, getBenchmarkSuite, getBenchmarkHistory } from '@/services/benchmark';
import { useBenchmarkStore } from '@/features/benchmark/benchmark-store';

export function useBenchmark() {
  const queryClient = useQueryClient();
  const setResults = useBenchmarkStore((state) => state.setResults);
  const setHeuristicScores = useBenchmarkStore((state) => state.setHeuristicScores);

  const runMutation = useMutation({
    mutationFn: runBenchmark,
    onSuccess: (data) => {
      setResults(data);
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
