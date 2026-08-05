import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface CapabilityBannerProps {
  message: string;
  variant?: "info" | "success" | "warning" | "danger";
  action?: ReactNode;
  className?: string;
}

const variantClasses = {
  info: "bg-[var(--color-primary-50)] text-[var(--color-primary-700)] border-[var(--color-primary-200)]",
  success: "bg-[var(--color-success-50)] text-[var(--color-success-700)] border-[var(--color-success-200)]",
  warning: "bg-[var(--color-warning-50)] text-[var(--color-warning-700)] border-[var(--color-warning-200)]",
  danger: "bg-[var(--color-danger-50)] text-[var(--color-danger-700)] border-[var(--color-danger-200)]",
};

export function CapabilityBanner({ message, variant = "info", action, className }: CapabilityBannerProps) {
  return (
    <div
      className={cn(
        "flex items-center justify-between gap-4 rounded-lg border px-4 py-3",
        variantClasses[variant],
        className
      )}
    >
      <p className="text-sm font-medium">{message}</p>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
