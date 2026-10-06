'use client';

import { create } from 'zustand';
import type { BenchmarkResult, BenchmarkSummary } from '@/types/benchmark';

interface BenchmarkState {
  results: BenchmarkResult[];
  summary: BenchmarkSummary | null;
  heuristicScores: BenchmarkResult[];
  setResults: (results: BenchmarkResult[]) => void;
  setHeuristicScores: (scores: BenchmarkResult[]) => void;
  reset: () => void;
}

export const useBenchmarkStore = create<BenchmarkState>((set) => ({
  results: [],
  summary: null,
  heuristicScores: [],
  setResults: (results) => set({ results }),
  setHeuristicScores: (heuristicScores) => set({ heuristicScores }),
  reset: () => set({ results: [], summary: null, heuristicScores: [] }),
}));
