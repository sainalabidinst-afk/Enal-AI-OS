import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface KeyValueProps {
  label: string;
  value: ReactNode;
  className?: string;
}

export function KeyValue({ label, value, className }: KeyValueProps) {
  return (
    <div className={cn("flex items-center justify-between py-2", className)}>
      <span className="text-sm text-[var(--color-secondary-500)]">{label}</span>
      <span className="text-sm text-[var(--color-foreground)]">{value}</span>
    </div>
  );
}
