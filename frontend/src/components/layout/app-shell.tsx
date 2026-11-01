'use client';

import { Sidebar } from '@/components/layout/sidebar';
import { TopBar } from '@/components/layout/top-bar';
import { MobileNav } from '@/components/layout/mobile-nav';
import { usePathname } from 'next/navigation';

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  if (pathname === '/login') {
    return <>{children}</>;
  }

  return (
    <div className="app-shell flex h-screen w-full overflow-hidden text-text-primary">
      <div className="app-sidebar-shell hidden md:flex">
        <Sidebar />
      </div>
      <div className="flex flex-1 flex-col overflow-hidden">
        <TopBar />
        <main className="app-main flex-1 overflow-auto">
          <div className="app-content">{children}</div>
        </main>
      </div>
      <MobileNav />
    </div>
  );
}
