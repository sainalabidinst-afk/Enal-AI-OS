"use client";

import { Bell, Settings, Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";

export function WorkspaceActions() {
  return (
    <div className="flex items-center gap-1">
      <Button variant="ghost" size="icon" className="h-8 w-8 relative" aria-label="Notifications">
        <Bell className="h-4 w-4" />
        <span className="absolute top-1 right-1 h-2 w-2 bg-[var(--color-accent)] rounded-full" />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8" aria-label="Theme">
        <Sun className="h-4 w-4 hidden dark:block" />
        <Moon className="h-4 w-4 block dark:hidden" />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8" aria-label="Settings">
        <Settings className="h-4 w-4" />
      </Button>
    </div>
  );
}
