'use client';

import { useState } from 'react';
import { ConfirmationDialog } from '@/components/shared/confirmation-dialog';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';

interface AuditDetailModalProps {
  auditId: string | null;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AuditDetailModal({ auditId, isOpen, onOpenChange }: AuditDetailModalProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['audit', 'trail', auditId],
    queryFn: () => apiClient.get(`/api/v1/governance/audit`),
    enabled: !!auditId && isOpen,
  });

  const entry = data?.entries?.find((e: { id: string }) => e.id === auditId);

  return (
    <ConfirmationDialog
      isOpen={isOpen}
      title="Audit Detail"
      description={
        isLoading ? (
          <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />
        ) : (
          <JsonViewer data={entry} />
        )
      }
      confirmLabel="Close"
      onConfirm={() => onOpenChange(false)}
      onCancel={() => onOpenChange(false)}
      variant="default"
    />
  );
}
