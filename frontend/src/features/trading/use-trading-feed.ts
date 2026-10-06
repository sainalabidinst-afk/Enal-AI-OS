'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { startLiveFeed, stopLiveFeed } from '@/services/trading';
import { useTradingStore } from '@/features/trading/trading-store';

export function useTradingFeed(symbol: string, timeframes?: string[]) {
  const queryClient = useQueryClient();
  const setFeedStatus = useTradingStore((state) => state.setFeedStatus);

  const startMutation = useMutation({
    mutationFn: () => startLiveFeed(symbol, timeframes),
    onSuccess: () => {
      setFeedStatus('running');
      queryClient.invalidateQueries({ queryKey: ['trading'] });
    },
    onError: () => setFeedStatus('error'),
  });

  const stopMutation = useMutation({
    mutationFn: stopLiveFeed,
    onSuccess: () => {
      setFeedStatus('stopped');
      queryClient.invalidateQueries({ queryKey: ['trading'] });
    },
  });

  return {
    start: startMutation.mutate,
    stop: stopMutation.mutate,
    isRunning: useTradingStore((state) => state.feedStatus) === 'running',
  };
}
