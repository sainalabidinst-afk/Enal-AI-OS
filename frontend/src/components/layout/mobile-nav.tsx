'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/cn';
import { useUIStore } from '@/stores/ui-store';
import { X } from 'lucide-react';
import { Sidebar } from './sidebar';

export function MobileNav() {
  const pathname = usePathname();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);

  if (sidebarCollapsed) return null;

  return (
    <div className="fixed inset-0 z-50 md:hidden">
      <div className="absolute inset-0 bg-black/50" />
      <div className="relative h-full w-64">
        <Sidebar />
      </div>
    </div>
  );
}
