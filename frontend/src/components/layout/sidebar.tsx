'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { cn } from '@/lib/cn';
import { useUIStore } from '@/stores/ui-store';
import { useAuthStore } from '@/stores/auth-store';
import { SearchBar } from '@/components/layout/search-bar';
import {
  Activity,
  BarChart3,
  Bell,
  Brain,
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  FileText,
  Hammer,
  LayoutDashboard,
  LogOut,
  Mic,
  Moon,
  Package,
  Search,
  Settings,
  Store,
  Sun,
  TrendingUp,
  X,
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
  { href: '/digital-twin', label: 'Digital Twin', icon: Brain },
];

interface SidebarProps {
  mobile?: boolean;
  onClose?: () => void;
}

export function Sidebar({ mobile = false, onClose }: SidebarProps) {
  const router = useRouter();
  const pathname = usePathname();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);
  const theme = useUIStore((state) => state.theme);
  const setTheme = useUIStore((state) => state.setTheme);
  const { user, logout } = useAuthStore();
  const collapsed = mobile ? false : sidebarCollapsed;

  const handleLogout = () => {
    logout();
    router.push('/login');
    onClose?.();
  };

  return (
    <aside
      className={cn(
        'app-sidebar flex h-full flex-col border-r border-border transition-all duration-200',
        collapsed ? 'w-[4.5rem]' : 'w-64',
        mobile && 'w-full'
      )}
    >
      <div className="flex items-center justify-between border-b border-border px-4 py-3">
        {!collapsed && (
          <div className="flex items-center gap-3">
            <span className="brand-mark" aria-hidden="true">
              E
            </span>
            <div>
              <span className="block text-sm font-semibold tracking-wide">Enal AI OS</span>
              <span className="block text-[10px] uppercase tracking-[0.18em] text-text-muted">
                Cognitive platform
              </span>
            </div>
          </div>
        )}
        <button
          onClick={mobile ? onClose : toggleSidebar}
          className="icon-button rounded-md p-2"
          aria-label={mobile ? 'Close navigation' : 'Toggle sidebar'}
        >
          {mobile ? (
            <X size={18} />
          ) : collapsed ? (
            <ChevronRight size={18} />
          ) : (
            <ChevronLeft size={18} />
          )}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4" aria-label="Primary navigation">
        <SearchBar />
        {!collapsed && (
          <p className="px-3 pb-2 pt-4 text-[10px] font-semibold uppercase tracking-[0.2em] text-text-muted">
            Workspace
          </p>
        )}
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  onClick={onClose}
                  aria-label={item.label}
                  title={collapsed ? item.label : undefined}
                  aria-current={isActive ? 'page' : undefined}
                  className={cn(
                    'sidebar-link flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors',
                    collapsed && 'justify-center px-0',
                    isActive
                      ? 'sidebar-link-active text-primary'
                      : 'text-text-secondary hover:bg-surface-hover hover:text-text-primary'
                  )}
                >
                  <Icon size={18} />
                  {!collapsed && <span>{item.label}</span>}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-border px-2 py-3">
        <div className={cn('flex items-center gap-3 px-3 py-2', collapsed && 'justify-center px-0')}>
          <div className="user-avatar flex h-9 w-9 items-center justify-center rounded-full text-xs font-semibold">
            {user?.username?.charAt(0).toUpperCase() ?? 'U'}
          </div>
          {!collapsed && (
            <div className="flex-1">
              <p className="text-sm font-medium">{user?.username ?? 'Guest'}</p>
              <p className="text-xs text-text-muted">
                {user?.roles?.join(', ') || 'Workspace member'}
              </p>
            </div>
          )}
        </div>
        <div className={cn('mt-2 flex items-center gap-2 px-3', collapsed && 'flex-col px-0')}>
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="sidebar-action flex flex-1 items-center gap-2 rounded-md px-2 py-2 text-xs text-text-secondary"
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
            aria-pressed={theme === 'light'}
            title={collapsed ? `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme` : undefined}
          >
            {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
            {!collapsed && <span>Theme</span>}
          </button>
          <button
            onClick={() => {
              router.push('/observability#alerts');
              onClose?.();
            }}
            className="sidebar-action flex flex-1 items-center gap-2 rounded-md px-2 py-2 text-xs text-text-secondary"
            aria-label="Open alerts"
            title={collapsed ? 'Open alerts' : undefined}
          >
            <Bell size={14} />
            {!collapsed && <span>Alerts</span>}
          </button>
          <button
            onClick={handleLogout}
            className="sidebar-action flex items-center gap-2 rounded-md px-2 py-2 text-xs text-danger"
            aria-label="Log out"
            title={collapsed ? 'Log out' : undefined}
          >
            <LogOut size={14} />
            {!collapsed && <span>Logout</span>}
          </button>
        </div>
      </div>
    </aside>
  );
}
