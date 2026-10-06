'use client';

import { Sidebar } from '@/components/layout/sidebar';
import { TopBar } from '@/components/layout/top-bar';
import { MobileNav } from '@/components/layout/mobile-nav';
import { usePathname } from 'next/navigation';
import { useUIStore } from '@/stores/ui-store';

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);

  if (pathname === '/login') {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen w-full overflow-hidden bg-surface-primary text-text-primary">
      <div className="hidden md:flex">
        <Sidebar />
      </div>
      <div className="flex flex-1 flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
      <MobileNav />
    </div>
  );
}
