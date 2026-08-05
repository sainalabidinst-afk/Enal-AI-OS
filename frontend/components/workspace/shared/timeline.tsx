"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface TimelineEvent {
  id: string;
  title: string;
  description?: string;
  timestamp?: string;
  status?: "completed" | "running" | "failed" | "pending";
}

interface TimelineProps {
  title?: string;
  events?: TimelineEvent[];
  className?: string;
}

const STATUS_STYLES = {
  completed: "bg-green-400",
  running: "bg-blue-400",
  failed: "bg-[var(--color-danger)]",
  pending: "bg-[var(--color-text-secondary)]",
};

export function Timeline({ title = "Timeline", events = [], className }: TimelineProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>Activity and event timeline</CardDescription>
        </CardHeader>
        <div className="p-4 space-y-4">
          {events.length === 0 && (
            <span className="text-xs text-[var(--color-text-secondary)]">No events yet.</span>
          )}
          {events.map((event, i) => (
            <div key={event.id} className="flex gap-3">
              <div className="flex flex-col items-center">
                <div className={`w-2 h-2 rounded-full ${STATUS_STYLES[event.status || "pending"]}`} />
                {i < events.length - 1 && <div className="w-px h-full bg-[var(--color-border)] mt-1" />}
              </div>
              <div className="flex-1 pb-4">
                <p className="text-sm font-medium text-[var(--color-text-primary)]">{event.title}</p>
                {event.description && (
                  <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">{event.description}</p>
                )}
                {event.timestamp && (
                  <p className="text-xs text-[var(--color-text-secondary)] mt-1">{event.timestamp}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
