"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useSettingsStore } from "@/store/settings-store";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";
import { ToastContainer } from "@/components/ui/toast";

export function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const theme = useSettingsStore((s) => s.theme);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const initialize = useAuthStore((s) => s.initialize);
  const eulaAccepted = useEulaStore((s) => s.hasAccepted());
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Initialize auth on mount
  useEffect(() => {
    initialize();
  }, [initialize]);

  const isPublicRoute =
    pathname === "/login" || pathname === "/" || pathname === "/eula";

  // Redirect to login if not authenticated (except public routes)
  useEffect(() => {
    if (!isAuthenticated && !isPublicRoute && typeof window !== "undefined") {
      const token = localStorage.getItem("enal-auth-token");
      if (!token) {
        router.push("/login");
      }
    }
  }, [isAuthenticated, isPublicRoute, router, pathname]);

  // EULA guard: redirect to /eula if authenticated but EULA not accepted
  useEffect(() => {
    if (
      isAuthenticated &&
      !eulaAccepted &&
      !isPublicRoute &&
      typeof window !== "undefined"
    ) {
      router.push("/eula");
    }
  }, [isAuthenticated, eulaAccepted, isPublicRoute, router]);

  const nav = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/workspace", label: "Workspace" },
    { href: "/executions", label: "Executions" },
    { href: "/artifacts", label: "Artifacts" },
    { href: "/metrics", label: "Metrics" },
    { href: "/capabilities", label: "Capabilities" },
    { href: "/integration", label: "Integration" },
    { href: "/settings", label: "Settings" },
  ];

  const isAuthPage = pathname === "/login" || pathname === "/eula";
  const isWorkspaceRoute = pathname.startsWith("/workspace") && !isAuthPage;

  // Don't show sidebar on login/eula pages
  if (isAuthPage) {
    return (
      <>
        {children}
        <ToastContainer />
      </>
    );
  }

  // Workspace routes use their own desktop-style layout
  if (isWorkspaceRoute) {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="hidden md:flex w-64 flex-col border-r border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
        {/* Logo */}
        <Link href="/dashboard" className="p-4 hover:opacity-80 transition-opacity">
          <h1 className="text-lg font-bold text-[var(--color-text-primary)]">Enal AI OS</h1>
          <p className="text-xs text-[var(--color-text-secondary)]">AI Execution Platform</p>
        </Link>

        {/* Navigation */}
        <nav className="flex-1 px-2 space-y-1 overflow-y-auto">
          {nav.map((item) => {
            const active =
              pathname === item.href ||
              (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block rounded-lg px-3 py-2 text-sm transition-colors ${
                  active
                    ? "bg-[var(--color-accent)] text-white"
                    : "text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)]"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Theme selector (desktop) */}
        <div className="border-t border-[var(--color-border)] p-3">
          <label className="block text-[10px] uppercase tracking-wide text-[var(--color-text-secondary)] mb-1.5">
            Theme
          </label>
          <select
            value={theme}
            onChange={(e) =>
              useSettingsStore
                .getState()
                .setTheme(e.target.value as "light" | "dark" | "system")
            }
            className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-2 py-1.5 text-xs text-[var(--color-text-primary)] focus:border-[var(--color-accent)] focus:outline-none"
          >
            <option value="system">System</option>
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </div>

        {/* User section at bottom */}
        <div className="border-t border-[var(--color-border)] p-3">
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 w-full rounded-lg px-2 py-1.5 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
            >
              <div className="h-6 w-6 rounded-full bg-[var(--color-accent)] flex items-center justify-center text-xs text-white font-medium">
                {user?.username?.charAt(0).toUpperCase() || "U"}
              </div>
              <span className="flex-1 text-left truncate">{user?.username || "User"}</span>
              <span className="text-xs">▼</span>
            </button>

            {showUserMenu && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setShowUserMenu(false)}
                />
                <div className="absolute bottom-full left-0 right-0 mb-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] shadow-lg z-20 overflow-hidden">
                  <div className="px-3 py-2 border-b border-[var(--color-border)]">
                    <p className="text-sm text-[var(--color-text-primary)]">{user?.username}</p>
                    <p className="text-xs text-[var(--color-text-secondary)]">Signed in</p>
                  </div>
                  <button
                    onClick={() => {
                      logout();
                      setShowUserMenu(false);
                      router.push("/login");
                    }}
                    className="w-full text-left px-3 py-2 text-sm text-[var(--color-danger)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
                  >
                    Sign out
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Mobile header */}
        <header className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-3 md:hidden">
          <h1 className="text-sm font-semibold text-[var(--color-text-primary)]">Enal AI OS</h1>
          <div className="flex items-center gap-2">
            <select
              value={theme}
              onChange={(e) =>
                useSettingsStore
                  .getState()
                  .setTheme(e.target.value as "light" | "dark" | "system")
              }
              className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-2 py-1 text-xs"
            >
              <option value="system">System</option>
              <option value="dark">Dark</option>
              <option value="light">Light</option>
            </select>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-[var(--color-bg-primary)]">
          {children}
        </main>
      </div>

      {/* Toast notifications */}
      <ToastContainer />
    </div>
  );
}
