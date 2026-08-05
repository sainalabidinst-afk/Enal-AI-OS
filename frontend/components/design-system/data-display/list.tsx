import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface ListProps {
  children: ReactNode;
  className?: string;
}

export function List({ children, className }: ListProps) {
  return <ul className={cn("space-y-2", className)}>{children}</ul>;
}

interface ListItemProps {
  children: ReactNode;
  className?: string;
}

export function ListItem({ children, className }: ListItemProps) {
  return (
    <li className={cn("flex items-start gap-2 text-sm text-[var(--color-foreground)]", className)}>
      {children}
    </li>
  );
}
