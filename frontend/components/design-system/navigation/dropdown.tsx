"use client";

import { type ReactNode, useState } from "react";
import { cn } from "@/lib/utils";

interface DropdownProps {
  trigger: ReactNode;
  children: ReactNode;
  align?: "left" | "right";
}

export function Dropdown({ trigger, children, align = "right" }: DropdownProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <div onClick={() => setOpen(!open)}>{trigger}</div>
      {open && (
        <div
          className={cn(
            "absolute z-20 mt-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] shadow-lg overflow-hidden min-w-[180px]",
            align === "right" ? "right-0" : "left-0"
          )}
        >
          {children}
        </div>
      )}
    </div>
  );
}

interface DropdownItemProps {
  children: ReactNode;
  onClick?: () => void;
  danger?: boolean;
  disabled?: boolean;
  onClose?: () => void;
}

export function DropdownItem({ children, onClick, danger, disabled, onClose }: DropdownItemProps) {
  return (
    <button
      onClick={() => {
        onClick?.();
        onClose?.();
      }}
      disabled={disabled}
      className={cn(
        "w-full text-left px-3 py-2 text-sm transition-colors",
        danger
          ? "text-[var(--color-danger-500)] hover:bg-[var(--color-danger-50)]"
          : "text-[var(--color-foreground)] hover:bg-[var(--color-secondary-100)]",
        disabled && "opacity-50 pointer-events-none"
      )}
    >
      {children}
    </button>
  );
}
