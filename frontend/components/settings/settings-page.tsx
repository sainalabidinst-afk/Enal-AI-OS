"use client";

import { useSettingsStore } from "@/store/settings-store";

export function SettingsPage() {
  const theme = useSettingsStore((s) => s.theme);
  const setTheme = useSettingsStore((s) => s.setTheme);
  const recipient = useSettingsStore((s) => s.recipient);
  const setRecipient = useSettingsStore((s) => s.setRecipient);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-xl font-bold">Settings</h1>

      <section className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Appearance</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium">Theme</p>
            <p className="text-xs text-[var(--color-text-secondary)]">Choose light, dark, or system preference.</p>
          </div>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value as "light" | "dark" | "system")}
            className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-1 text-sm"
          >
            <option value="system">System</option>
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </div>
      </section>

      <section className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Notifications</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium">Notification recipient</p>
            <p className="text-xs text-[var(--color-text-secondary)]">Used to fetch notifications from the backend.</p>
          </div>
          <input
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-1 text-sm"
          />
        </div>
      </section>
    </div>
  );
}
