"use client";

import { type ReactNode, useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface MenuProps {
  trigger: ReactNode;
  children: ReactNode;
  align?: "left" | "right";
}

export function Menu({ trigger, children, align = "right" }: MenuProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  return (
    <div className="relative" ref={ref}>
      <div onClick={() => setOpen(!open)}>{trigger}</div>
      {open && (
        <div
          className={cn(
            "absolute z-20 mt-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] shadow-lg overflow-hidden min-w-[180px]",
            align === "right" ? "right-0" : "left-0"
          )}
        >
          {children}
        </div>
      )}
    </div>
  );
}

interface MenuItemProps {
  children: ReactNode;
  onClick?: () => void;
  danger?: boolean;
  disabled?: boolean;
}

export function MenuItem({ children, onClick, danger, disabled }: MenuItemProps) {
  return (
    <button
      onClick={() => {
        onClick?.();
      }}
      disabled={disabled}
      className={cn(
        "w-full text-left px-3 py-2 text-sm transition-colors",
        danger
          ? "text-[var(--color-danger)] hover:bg-[var(--color-danger)]/10"
          : "text-[var(--color-text-primary)] hover:bg-[var(--color-bg-tertiary)]",
        disabled && "opacity-50 pointer-events-none"
      )}
    >
      {children}
    </button>
  );
}
