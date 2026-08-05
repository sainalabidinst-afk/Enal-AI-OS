"use client";

import { type ReactNode, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Bell, CheckCheck, X } from "lucide-react";

interface Notification {
  id: string;
  title: string;
  message: string;
  timestamp?: string;
  read?: boolean;
}

interface NotificationCenterProps {
  title?: string;
  notifications?: Notification[];
  onMarkRead?: (id: string) => void;
  onClearAll?: () => void;
  className?: string;
}

export function NotificationCenter({
  title = "Notifications",
  notifications = [],
  onMarkRead,
  onClearAll,
  className,
}: NotificationCenterProps) {
  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <Bell className="h-4 w-4" />
                <CardTitle>{title}</CardTitle>
                {unreadCount > 0 && (
                  <span className="text-xs bg-[var(--color-accent)] text-white px-2 py-0.5 rounded-full">
                    {unreadCount}
                  </span>
                )}
              </div>
              <CardDescription>Recent notifications and alerts</CardDescription>
            </div>
            {notifications.length > 0 && (
              <Button variant="ghost" size="sm" onClick={onClearAll}>
                Clear all
              </Button>
            )}
          </div>
        </CardHeader>
        <div className="divide-y divide-[var(--color-border)]">
          {notifications.length === 0 && (
            <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">No notifications</div>
          )}
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`px-4 py-3 ${notification.read ? "opacity-60" : "bg-[var(--color-bg-tertiary)]"}`}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className="text-sm font-medium text-[var(--color-text-primary)]">{notification.title}</p>
                  <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">{notification.message}</p>
                  {notification.timestamp && (
                    <p className="text-xs text-[var(--color-text-secondary)] mt-1">{notification.timestamp}</p>
                  )}
                </div>
                {!notification.read && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 shrink-0"
                    onClick={() => onMarkRead?.(notification.id)}
                  >
                    <CheckCheck className="h-3.5 w-3.5" />
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
