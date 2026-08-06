"use client";

import { memo } from "react";
import { ErrorBoundary } from "../error-boundary/error-boundary";

interface TradingErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const TradingErrorBoundary = memo(function TradingErrorBoundary({
  children,
  fallback,
}: TradingErrorBoundaryProps) {
  return (
    <ErrorBoundary
      fallback={
        fallback || (
          <div className="flex h-full w-full items-center justify-center bg-[var(--color-bg-secondary)]">
            <div className="text-center space-y-2">
              <p className="text-4xl">⚠️</p>
              <p className="text-sm text-[var(--color-secondary-500)]">Trading workspace encountered an error.</p>
            </div>
          </div>
        )
      }
      onError={(error, errorInfo) => {
        console.error("Trading workspace error:", error, errorInfo);
      }}
    >
      {children}
    </ErrorBoundary>
  );
});
