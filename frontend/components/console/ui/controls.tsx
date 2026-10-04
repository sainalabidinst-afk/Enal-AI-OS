"use client";

import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

export function Rating({
  value,
  compact = false,
}: {
  value: number;
  compact?: boolean;
}) {
  const clamped = Math.max(0, Math.min(5, value));
  return (
    <span className="inline-flex items-center gap-1">
      <span className="inline-flex">
        {Array.from({ length: 5 }).map((_, index) => {
          const filled = clamped - index >= 0.5;
          const half = clamped - index >= 0 && clamped - index < 0.5;
          return (
            <Star
              key={index}
              className={cn(
                "h-3 w-3",
                filled
                  ? "fill-[var(--ecp-alert)] text-[var(--ecp-alert)]"
                  : half
                    ? "fill-[var(--ecp-alert)]/50 text-[var(--ecp-alert)]"
                    : "text-[var(--ecp-text-dim)]"
              )}
            />
          );
        })}
      </span>
      {!compact && (
        <span className="text-[11px] text-[var(--ecp-text-muted)]">
          {clamped.toFixed(1)}
        </span>
      )}
    </span>
  );
}

export function Toggle({
  checked,
  onChange,
  label,
  description,
  disabled = false,
}: {
  checked: boolean;
  onChange: (next: boolean) => void;
  label: string;
  description?: string;
  disabled?: boolean;
}) {
  return (
    <label
      className={cn(
        "flex items-start gap-3 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface)] px-3 py-2.5",
        disabled && "opacity-50"
      )}
    >
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => onChange(!checked)}
        className={cn(
          "relative mt-0.5 h-5 w-9 shrink-0 rounded-full transition-colors",
          checked ? "bg-[var(--ecp-gov)]" : "bg-[var(--ecp-surface-3)]"
        )}
      >
        <span
          className={cn(
            "absolute top-0.5 h-4 w-4 rounded-full bg-white transition-transform",
            checked ? "left-[18px]" : "left-0.5"
          )}
        />
      </button>
      <span className="min-w-0">
        <span className="block text-xs font-medium">{label}</span>
        {description && (
          <span className="mt-0.5 block text-[11px] text-[var(--ecp-text-dim)]">
            {description}
          </span>
        )}
      </span>
    </label>
  );
}

export function Field({
  label,
  hint,
  children,
}: {
  label: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="block text-[11px] font-medium uppercase tracking-wide text-[var(--ecp-text-dim)]">
        {label}
      </span>
      {children}
      {hint && <span className="block text-[11px] text-[var(--ecp-text-dim)]">{hint}</span>}
    </label>
  );
}

export function inputClass() {
  return "w-full rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-3 py-2 text-xs text-[var(--ecp-text)] outline-none transition-colors focus:border-[var(--ecp-gov)]";
}

export function selectClass() {
  return `${inputClass()} appearance-none`;
}