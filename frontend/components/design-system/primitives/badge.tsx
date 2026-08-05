import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface BadgeProps {
  children: ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "secondary";
  size?: "sm" | "md";
  className?: string;
}

const variantClasses = {
  default: "bg-[var(--color-primary-100)] text-[var(--color-primary-700)]",
  success: "bg-[var(--color-success-100)] text-[var(--color-success-600)]",
  warning: "bg-[var(--color-warning-100)] text-[var(--color-warning-600)]",
  danger: "bg-[var(--color-danger-100)] text-[var(--color-danger-600)]",
  secondary: "bg-[var(--color-secondary-100)] text-[var(--color-secondary-700)]",
};

const sizeClasses = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-3 py-1 text-sm",
};

export function Badge({ children, variant = "default", size = "md", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full font-medium",
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {children}
    </span>
  );
}
