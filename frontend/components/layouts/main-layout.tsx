"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useSettingsStore } from "@/store/settings-store";

export function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const theme = useSettingsStore((s) => s.theme);

  const nav = [
    { href: "/", label: "Chat" },
    { href: "/workspace", label: "Workspace" },
    { href: "/executions", label: "Executions" },
    { href: "/artifacts", label: "Artifacts" },
    { href: "/metrics", label: "Metrics" },
    { href: "/capabilities", label: "Capabilities" },
    { href: "/settings", label: "Settings" },
  ];

  return (
    <div className="flex h-screen">
      <aside className="hidden md:flex w-64 flex-col border-r border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
        <div className="p-4">
          <h1 className="text-lg font-bold">Enal AI OS</h1>
          <p className="text-xs text-[var(--color-text-secondary)]">AI Execution Platform</p>
        </div>
        <nav className="flex-1 px-2 space-y-1">
          {nav.map((item) => {
            const active = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block rounded-lg px-3 py-2 text-sm ${
                  active ? "bg-[var(--color-accent)] text-white" : "text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-3 md:hidden">
          <h1 className="text-sm font-semibold">Enal AI OS</h1>
          <select
            value={theme}
            onChange={(e) => useSettingsStore.getState().setTheme(e.target.value as "light" | "dark" | "system")}
            className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-2 py-1 text-xs"
          >
            <option value="system">System</option>
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </header>
        <main className="flex-1 overflow-y-auto bg-[var(--color-bg-primary)]">{children}</main>
      </div>
    </div>
  );
}
