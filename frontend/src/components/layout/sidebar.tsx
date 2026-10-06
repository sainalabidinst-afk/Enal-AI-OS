'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/cn';
import { useUIStore } from '@/stores/ui-store';
import { useAuthStore } from '@/stores/auth-store';
import { SearchBar } from '@/components/layout/search-bar';
import {
  LayoutDashboard,
  TrendingUp,
  Package,
  Hammer,
  ClipboardList,
  BarChart3,
  Store,
  Mic,
  Settings,
  Activity,
  FileText,
  Search,
  Sun,
  Moon,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Bell,
} from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/trading', label: 'Trading Intelligence', icon: TrendingUp },
  { href: '/capability-packs', label: 'Capability Packs', icon: Package },
  { href: '/builder', label: 'Builder', icon: Hammer },
  { href: '/evaluation', label: 'Evaluation Console', icon: ClipboardList },
  { href: '/benchmark', label: 'Benchmark Dashboard', icon: BarChart3 },
  { href: '/marketplace', label: 'Marketplace', icon: Store },
  { href: '/voice', label: 'Voice Agent', icon: Mic },
  { href: '/settings', label: 'Settings', icon: Settings },
  { href: '/observability', label: 'Observability', icon: Activity },
  { href: '/governance', label: 'Governance Explorer', icon: FileText },
  { href: '/audit-trail', label: 'Audit Trail', icon: Search },
];

export function Sidebar() {
  const pathname = usePathname();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);
  const { user, logout } = useAuthStore();

  return (
    <aside
      className={cn(
        'flex h-full flex-col border-r border-border bg-surface-secondary transition-all duration-200',
        sidebarCollapsed ? 'w-16' : 'w-64'
      )}
    >
      <div className="flex items-center justify-between border-b border-border px-4 py-3">
        {!sidebarCollapsed && (
          <span className="text-sm font-semibold tracking-wide">Enal Cognitive Platform</span>
        )}
        <button
          onClick={toggleSidebar}
          className="rounded-md p-1.5 hover:bg-surface-hover"
          aria-label="Toggle sidebar"
        >
          {sidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto px-2 py-3">
        <SearchBar />
        <ul className="mt-2 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    'flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
                    isActive
                      ? 'bg-primary/10 text-primary'
                      : 'text-text-secondary hover:bg-surface-hover hover:text-text-primary'
                  )}
                >
                  <Icon size={18} />
                  {!sidebarCollapsed && <span>{item.label}</span>}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-border px-2 py-3">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-xs font-semibold">
            {user?.username?.charAt(0).toUpperCase() ?? 'U'}
          </div>
          {!sidebarCollapsed && (
            <div className="flex-1">
              <p className="text-sm font-medium">{user?.username ?? 'Guest'}</p>
              <p className="text-xs text-text-muted">{user?.roles?.join(', ') ?? ''}</p>
            </div>
          )}
        </div>
        <div className="mt-2 flex items-center gap-2 px-3">
          <button className="flex flex-1 items-center gap-2 rounded-md px-2 py-1.5 text-xs text-text-secondary hover:bg-surface-hover hover:text-text-primary">
            <Sun size={14} />
            {!sidebarCollapsed && <span>Theme</span>}
          </button>
          <button className="flex flex-1 items-center gap-2 rounded-md px-2 py-1.5 text-xs text-text-secondary hover:bg-surface-hover hover:text-text-primary">
            <Bell size={14} />
            {!sidebarCollapsed && <span>Alerts</span>}
          </button>
          <button
            onClick={logout}
            className="flex items-center gap-2 rounded-md px-2 py-1.5 text-xs text-danger hover:bg-surface-hover"
          >
            <LogOut size={14} />
            {!sidebarCollapsed && <span>Logout</span>}
          </button>
        </div>
      </div>
    </aside>
  );
}
