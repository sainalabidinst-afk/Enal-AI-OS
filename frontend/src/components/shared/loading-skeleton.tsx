'use client';

import { cn } from '@/lib/cn';

interface SkeletonProps {
  className?: string;
}

export function LoadingSkeleton({ className }: SkeletonProps) {
  return (
    <div className={cn('animate-pulse rounded-md bg-surface-tertiary', className)} />
  );
}

export function CardSkeleton() {
  return (
    <div className="space-y-3 rounded-lg border border-border bg-surface-secondary p-4">
      <LoadingSkeleton className="h-4 w-1/2" />
      <LoadingSkeleton className="h-8 w-3/4" />
      <LoadingSkeleton className="h-4 w-full" />
    </div>
  );
}

export function TableRowSkeleton() {
  return (
    <div className="flex items-center gap-4 border-b border-border px-4 py-3">
      <LoadingSkeleton className="h-4 w-1/4" />
      <LoadingSkeleton className="h-4 w-1/4" />
      <LoadingSkeleton className="h-4 w-1/4" />
      <LoadingSkeleton className="h-4 w-1/4" />
    </div>
  );
}
