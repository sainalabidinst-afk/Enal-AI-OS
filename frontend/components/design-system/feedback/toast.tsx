"use client";

import { type ReactNode, useState, useEffect } from "react";
import { cn } from "@/lib/utils";

interface ToastProps {
  message: string;
  variant?: "default" | "success" | "warning" | "danger";
  duration?: number;
  onClose?: () => void;
}

export function Toast({ message, variant = "default", duration = 3000, onClose }: ToastProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      onClose?.();
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const variantClasses = {
    default: "bg-[var(--color-surface)] text-[var(--color-foreground)]",
    success: "bg-[var(--color-success-100)] text-[var(--color-success-600)]",
    warning: "bg-[var(--color-warning-100)] text-[var(--color-warning-600)]",
    danger: "bg-[var(--color-danger-100)] text-[var(--color-danger-600)]",
  };

  if (!visible) return null;

  return (
    <div
      className={cn(
        "fixed bottom-4 right-4 z-50 rounded-lg border border-[var(--color-border)] px-4 py-3 shadow-lg",
        variantClasses[variant]
      )}
    >
      {message}
    </div>
  );
}
