'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ConfirmationDialog } from '@/components/shared/confirmation-dialog';
import { JsonViewer } from '@/components/shared/json-viewer';

interface BenchmarkDetailModalProps {
  benchmarkId: string | null;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export function BenchmarkDetailModal({ benchmarkId, isOpen, onOpenChange }: BenchmarkDetailModalProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['benchmark', 'history', benchmarkId],
    queryFn: () => apiClient.get(`/api/v1/benchmark/history/${benchmarkId}`),
    enabled: !!benchmarkId && isOpen,
  });

  return (
    <ConfirmationDialog
      isOpen={isOpen}
      title="Benchmark Detail"
      description={
        isLoading ? (
          <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />
        ) : (
          <JsonViewer data={data} />
        )
      }
      confirmLabel="Close"
      onConfirm={() => onOpenChange(false)}
      onCancel={() => onOpenChange(false)}
      variant="default"
    />
  );
}
