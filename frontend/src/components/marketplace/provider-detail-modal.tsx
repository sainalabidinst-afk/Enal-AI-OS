'use client';

import { useState } from 'react';
import { ConfirmationDialog } from '@/components/shared/confirmation-dialog';

interface ProviderDetailModalProps {
  provider: string | null;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ProviderDetailModal({ provider, isOpen, onOpenChange }: ProviderDetailModalProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['providers', provider],
    queryFn: () => apiClient.get('/api/v1/models/providers'),
    enabled: !!provider && isOpen,
  });

  const providerData = provider ? data?.[provider] : null;

  return (
    <ConfirmationDialog
      isOpen={isOpen}
      title={provider ?? 'Provider Detail'}
      description={
        isLoading ? (
          <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />
        ) : (
          <JsonViewer data={providerData} />
        )
      }
      confirmLabel="Close"
      onConfirm={() => onOpenChange(false)}
      onCancel={() => onOpenChange(false)}
      variant="default"
    />
  );
}
