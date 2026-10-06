'use client';

import { useQuery } from '@tanstack/react-query';
import { getLiveRegime } from '@/services/trading';
import { useTradingStore } from '@/features/trading/trading-store';

export function useRegimeDetection(symbol: string) {
  const { data, isLoading } = useQuery({
    queryKey: ['trading', 'regime', symbol],
    queryFn: () => getLiveRegime(symbol),
  });

  const setRegime = useTradingStore((state) => state.setRegime);

  if (data?.data) {
    setRegime(data.data.regime);
  }

  return {
    regime: data?.data?.regime ?? null,
    confidence: data?.data?.confidence ?? null,
    isLoading,
  };
}
