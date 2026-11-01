'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useUIStore } from '@/stores/ui-store';
import { Sidebar } from './sidebar';

export function MobileNav() {
  const pathname = usePathname();
  const isOpen = useUIStore((state) => state.mobileNavOpen);
  const closeMobileNav = useUIStore((state) => state.closeMobileNav);

  useEffect(() => {
    closeMobileNav();
  }, [pathname, closeMobileNav]);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closeMobileNav();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, closeMobileNav]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 md:hidden" id="mobile-navigation">
      <button
        className="mobile-nav-backdrop absolute inset-0"
        onClick={closeMobileNav}
        aria-label="Close navigation"
      />
      <div
        className="mobile-nav-panel relative h-full w-72 max-w-[85vw]"
        role="dialog"
        aria-modal="true"
        aria-label="Main navigation"
      >
        <Sidebar mobile onClose={closeMobileNav} />
      </div>
    </div>
  );
}
