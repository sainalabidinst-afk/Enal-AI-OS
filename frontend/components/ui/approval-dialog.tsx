"use client";

import { useState } from "react";

interface ApprovalDialogProps {
  open: boolean;
  title?: string;
  description?: string;
  reason?: string;
  impact?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  danger?: boolean;
  onConfirm: () => Promise<void> | void;
  onCancel: () => void;
}

export function ApprovalDialog({
  open,
  title = "Approval required",
  description = "This action requires your approval before continuing.",
  reason,
  impact,
  confirmLabel = "Approve",
  cancelLabel = "Cancel",
  danger = false,
  onConfirm,
  onCancel,
}: ApprovalDialogProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!open) return null;

  const handleConfirm = async () => {
    setLoading(true);
    setError(null);
    try {
      await onConfirm();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 shadow-lg">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">{description}</p>

        {reason && (
          <div className="mt-4 rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Reason</p>
            <p className="mt-1 text-sm">{reason}</p>
          </div>
        )}

        {impact && (
          <div className="mt-3 rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Impact</p>
            <p className="mt-1 text-sm">{impact}</p>
          </div>
        )}

        {error && (
          <div className="mt-4 rounded-md border border-[var(--color-danger)] bg-[var(--color-bg-primary)] px-4 py-3 text-sm text-[var(--color-danger)]">
            {error}
          </div>
        )}

        <div className="mt-6 flex justify-end gap-2">
          <button
            onClick={onCancel}
            disabled={loading}
            className="rounded-lg border border-[var(--color-border)] px-4 py-2 text-sm hover:bg-[var(--color-bg-tertiary)] disabled:opacity-50"
          >
            {cancelLabel}
          </button>
          <button
            onClick={handleConfirm}
            disabled={loading}
            className={`rounded-lg px-4 py-2 text-sm font-medium text-white disabled:opacity-50 ${
              danger ? "bg-[var(--color-danger)] hover:opacity-90" : "bg-[var(--color-accent)] hover:opacity-90"
            }`}
          >
            {loading ? "Processing..." : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
