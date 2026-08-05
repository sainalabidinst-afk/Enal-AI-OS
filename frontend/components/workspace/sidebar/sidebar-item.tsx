"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface SidebarItemProps {
  icon?: ReactNode;
  label: string;
  active?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

export function SidebarItem({ icon, label, active, disabled, onClick, className }: SidebarItemProps) {
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={onClick}
      disabled={disabled}
      aria-current={active ? "page" : undefined}
      title={label}
      className={cn(
        "w-10 h-10 flex-col gap-1",
        active
          ? "bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent)] hover:text-white"
          : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]",
        className
      )}
    >
      {icon && <span className="h-4 w-4">{icon}</span>}
      <span className="text-[10px] leading-none">{label}</span>
    </Button>
  );
}
