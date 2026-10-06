'use client';

import { usePathname } from 'next/navigation';
import { cn } from '@/lib/cn';
import { useUIStore } from '@/stores/ui-store';
import { useNotificationStore } from '@/stores/notification-store';
import { Bell, Search } from 'lucide-react';

const titleMap: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/trading': 'Trading Intelligence',
  '/capability-packs': 'Capability Packs',
  '/builder': 'Builder',
  '/evaluation': 'Evaluation Console',
  '/benchmark': 'Benchmark Dashboard',
  '/marketplace': 'Marketplace',
  '/voice': 'Voice Agent',
  '/settings': 'Settings',
  '/observability': 'Observability',
  '/governance': 'Governance Explorer',
  '/audit-trail': 'Audit Trail',
};

export function TopBar() {
  const pathname = usePathname();
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);
  const unreadCount = useNotificationStore((state) => state.unreadCount);

  const title = titleMap[pathname] || 'Enal Cognitive Platform';

  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-surface-secondary px-4">
      <div className="flex items-center gap-3">
        <button
          onClick={toggleSidebar}
          className="rounded-md p-1.5 hover:bg-surface-hover md:hidden"
          aria-label="Toggle menu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        </button>
        <h1 className="text-base font-semibold">{title}</h1>
      </div>

      <div className="flex items-center gap-2">
        <button className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-xs text-text-secondary hover:bg-surface-hover">
          <Search size={14} />
          <span className="hidden sm:inline">Search</span>
          <kbd className="hidden sm:inline rounded border border-border-light px-1.5 py-0.5 text-[10px] text-text-muted">
            ⌘K
          </kbd>
        </button>
        <button className="relative rounded-md p-2 hover:bg-surface-hover">
          <Bell size={18} />
          {unreadCount > 0 && (
            <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-danger" />
          )}
        </button>
      </div>
    </header>
  );
}
