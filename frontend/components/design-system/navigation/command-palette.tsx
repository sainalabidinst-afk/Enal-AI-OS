"use client";

import { type ReactNode, useState, useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: ReactNode;
}

export function CommandPalette({ open, onOpenChange, children }: CommandPaletteProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
    }
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => onOpenChange(false)} />
      <div className="relative z-10 w-full max-w-lg rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] shadow-2xl">
        {children}
      </div>
    </div>
  );
}

interface CommandInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function CommandInput({ value, onChange, placeholder }: CommandInputProps) {
  return (
    <input
      ref={useRef<HTMLInputElement>(null)}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full px-4 py-3 text-sm border-b border-[var(--color-border)] bg-transparent text-[var(--color-foreground)] placeholder:text-[var(--color-secondary-400)] focus:outline-none"
    />
  );
}

interface CommandListProps {
  children: ReactNode;
  className?: string;
}

export function CommandList({ children, className }: CommandListProps) {
  return <div className={cn("p-2 max-h-96 overflow-y-auto", className)}>{children}</div>;
}

interface CommandItemProps {
  children: ReactNode;
  onSelect?: () => void;
  className?: string;
}

export function CommandItem({ children, onSelect, className }: CommandItemProps) {
  return (
    <button
      onClick={onSelect}
      className={cn(
        "w-full text-left px-3 py-2 text-sm rounded-md transition-colors hover:bg-[var(--color-secondary-100)]",
        className
      )}
    >
      {children}
    </button>
  );
}
