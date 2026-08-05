"use client";

import { type ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

interface TimelineEvent {
  id: string;
  title: string;
  description?: string;
  timestamp?: string;
  status?: "completed" | "running" | "failed" | "pending";
}

interface TimelineProps {
  events?: TimelineEvent[];
  className?: string;
}

const STATUS_STYLES = {
  completed: "bg-[var(--color-success-500)]",
  running: "bg-[var(--color-primary-500)]",
  failed: "bg-[var(--color-danger-500)]",
  pending: "bg-[var(--color-secondary-400)]",
};

export function Timeline({ events = [], className }: TimelineProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Timeline</CardTitle>
        <CardDescription>Activity and event timeline</CardDescription>
      </CardHeader>
      <div className="p-4 space-y-4">
        {events.length === 0 && (
          <span className="text-xs text-[var(--color-secondary-500)]">No events yet.</span>
        )}
        {events.map((event, i) => (
          <div key={event.id} className="flex gap-3">
            <div className="flex flex-col items-center">
              <div className={`w-2 h-2 rounded-full ${STATUS_STYLES[event.status || "pending"]}`} />
              {i < events.length - 1 && <div className="w-px h-full bg-[var(--color-border)] mt-1" />}
            </div>
            <div className="flex-1 pb-4">
              <p className="text-sm font-medium text-[var(--color-foreground)]">{event.title}</p>
              {event.description && (
                <p className="text-xs text-[var(--color-secondary-500)] mt-0.5">{event.description}</p>
              )}
              {event.timestamp && (
                <p className="text-xs text-[var(--color-secondary-500)] mt-1">{event.timestamp}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
