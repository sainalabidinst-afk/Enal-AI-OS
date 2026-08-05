"use client";

import { type ReactNode, useEffect, useRef } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface DialogProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children?: ReactNode;
  footer?: ReactNode;
}

export function Dialog({ open, onClose, title, description, children, footer }: DialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div
        ref={dialogRef}
        className={cn(
          "relative z-10 w-full max-w-lg rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] shadow-2xl",
          "flex flex-col max-h-[85vh]"
        )}
      >
        {(title || description) && (
          <div className="border-b border-[var(--color-border)] px-6 py-4">
            {title && <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">{title}</h2>}
            {description && <p className="text-sm text-[var(--color-text-secondary)] mt-1">{description}</p>}
          </div>
        )}
        <div className="flex-1 overflow-y-auto px-6 py-4">{children}</div>
        {footer && <div className="border-t border-[var(--color-border)] px-6 py-4 flex justify-end gap-2">{footer}</div>}
      </div>
    </div>
  );
}
