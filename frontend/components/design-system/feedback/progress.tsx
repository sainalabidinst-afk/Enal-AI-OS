import { cn } from "@/lib/utils";

interface ProgressProps {
  value?: number;
  max?: number;
  className?: string;
  variant?: "default" | "success" | "warning" | "danger";
}

export function Progress({ value = 0, max = 100, className, variant = "default" }: ProgressProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const variantClasses = {
    default: "bg-[var(--color-primary-500)]",
    success: "bg-[var(--color-success-500)]",
    warning: "bg-[var(--color-warning-500)]",
    danger: "bg-[var(--color-danger-500)]",
  };

  return (
    <div className={cn("h-2 w-full rounded-full bg-[var(--color-secondary-200)]", className)}>
      <div
        className={cn("h-full rounded-full transition-all", variantClasses[variant])}
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
}
