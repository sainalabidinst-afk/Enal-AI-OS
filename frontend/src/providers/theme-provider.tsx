'use client';

import { useEffect } from 'react';
import { useUIStore } from '@/stores/ui-store';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useUIStore((state) => state.theme);
  const hydrate = useUIStore((state) => state.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return <>{children}</>;
}
