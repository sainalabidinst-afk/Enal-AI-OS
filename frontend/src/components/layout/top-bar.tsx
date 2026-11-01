'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useUIStore } from '@/stores/ui-store';
import { useNotificationStore } from '@/stores/notification-store';
import { Bell, Menu, Search, X } from 'lucide-react';

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
  '/digital-twin': 'Digital Twin',
  '/search': 'Search',
};

export function TopBar() {
  const router = useRouter();
  const pathname = usePathname();
  const mobileNavOpen = useUIStore((state) => state.mobileNavOpen);
  const toggleMobileNav = useUIStore((state) => state.toggleMobileNav);
  const unreadCount = useNotificationStore((state) => state.unreadCount);

  const title = titleMap[pathname] || 'Enal Cognitive Platform';

  useEffect(() => {
    const handleShortcut = (event: KeyboardEvent) => {
      const target = event.target;
      const isEditing =
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        target instanceof HTMLSelectElement ||
        (target instanceof HTMLElement && target.isContentEditable);

      if (event.key === '/' && !isEditing) {
        event.preventDefault();
        router.push('/search');
      }
    };

    window.addEventListener('keydown', handleShortcut);
    return () => window.removeEventListener('keydown', handleShortcut);
  }, [router]);

  return (
    <header className="app-topbar flex h-16 items-center justify-between border-b border-border px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={toggleMobileNav}
          className="icon-button rounded-md p-2 md:hidden"
          aria-label={mobileNavOpen ? 'Close navigation' : 'Open navigation'}
          aria-expanded={mobileNavOpen}
          aria-controls="mobile-navigation"
        >
          {mobileNavOpen ? <X size={18} /> : <Menu size={18} />}
        </button>
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-text-muted">
            Enal Cognitive Platform
          </p>
          <h1 className="text-base font-semibold tracking-tight">{title}</h1>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => router.push('/search')}
          className="topbar-search flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-xs text-text-secondary"
          aria-label="Open search"
        >
          <Search size={14} />
          <span className="hidden sm:inline">Search workspace</span>
          <kbd className="hidden sm:inline rounded border border-border-light px-1.5 py-0.5 text-[10px] text-text-muted">
            /
          </kbd>
        </button>
        <button
          onClick={() => router.push('/observability#alerts')}
          className="icon-button relative rounded-lg p-2"
          aria-label={unreadCount ? `Open alerts, ${unreadCount} unread` : 'Open alerts'}
        >
          <Bell size={18} />
          {unreadCount > 0 && (
            <span
              className="absolute right-1 top-1 h-2 w-2 rounded-full bg-danger"
              aria-hidden="true"
            />
          )}
        </button>
      </div>
    </header>
  );
}
