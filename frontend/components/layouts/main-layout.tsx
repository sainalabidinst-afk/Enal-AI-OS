"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";
import { ToastContainer } from "@/components/ui/toast";

export function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const initialize = useAuthStore((s) => s.initialize);
  const eulaAccepted = useEulaStore((s) => s.hasAccepted());

  // Initialize auth on mount
  useEffect(() => {
    initialize();
  }, [initialize]);

  const isPublicRoute =
    pathname === "/login" || pathname === "/" || pathname === "/eula";
  const isConsoleRoute = pathname.startsWith("/console");

  // Redirect to login if not authenticated (except public routes)
  useEffect(() => {
    if (
      !isAuthenticated &&
      !isPublicRoute &&
      !isConsoleRoute &&
      typeof window !== "undefined"
    ) {
      const token = localStorage.getItem("enal-auth-token");
      if (!token) {
        router.push("/login");
      }
    }
  }, [isAuthenticated, isPublicRoute, isConsoleRoute, router, pathname]);

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

  // Console routes ship their own observability-console shell
  if (isConsoleRoute) {
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
      {/* Main content */}
      <div className="flex flex-1 flex-col min-w-0">
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
