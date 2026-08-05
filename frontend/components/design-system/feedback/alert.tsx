import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface AlertProps {
  children: ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
  title?: string;
  className?: string;
}

const variantClasses = {
  default: "bg-[var(--color-secondary-50)] text-[var(--color-foreground)]",
  success: "bg-[var(--color-success-50)] text-[var(--color-success-700)]",
  warning: "bg-[var(--color-warning-50)] text-[var(--color-warning-700)]",
  danger: "bg-[var(--color-danger-50)] text-[var(--color-danger-700)]",
};

export function Alert({ children, variant = "default", title, className }: AlertProps) {
  return (
    <div
      className={cn(
        "rounded-lg border border-[var(--color-border)] p-4",
        variantClasses[variant],
        className
      )}
    >
      {title && <h4 className="font-medium mb-1">{title}</h4>}
      {children}
    </div>
  );
}
