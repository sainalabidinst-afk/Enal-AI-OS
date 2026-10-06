'use client';

import { cn } from '@/lib/cn';

type Status = 'success' | 'warning' | 'danger' | 'neutral' | 'info';

interface StatusBadgeProps {
  status: Status;
  label?: string;
  className?: string;
}

const statusStyles: Record<Status, string> = {
  success: 'border-success/40 bg-success/10 text-success',
  warning: 'border-warning/40 bg-warning/10 text-warning',
  danger: 'border-danger/40 bg-danger/10 text-danger',
  neutral: 'border-border bg-surface-tertiary text-text-secondary',
  info: 'border-primary/40 bg-primary/10 text-primary',
};

export function StatusBadge({ status, label, className }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium',
        statusStyles[status],
        className
      )}
    >
      <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-current" />
      {label ?? status}
    </span>
  );
}
