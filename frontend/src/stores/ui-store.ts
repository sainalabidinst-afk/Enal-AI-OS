'use client';

import { create } from 'zustand';

type Theme = 'dark' | 'light';

interface UIState {
  sidebarCollapsed: boolean;
  theme: Theme;
  activeModule: string;
  isOnline: boolean;
  toggleSidebar: () => void;
  setTheme: (theme: Theme) => void;
  setActiveModule: (module: string) => void;
  setIsOnline: (online: boolean) => void;
  hydrate: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarCollapsed: false,
  theme: 'dark',
  activeModule: 'dashboard',
  isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,

  toggleSidebar: () =>
    set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

  setTheme: (theme) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    }
    set({ theme });
  },

  setActiveModule: (activeModule) => set({ activeModule }),

  setIsOnline: (isOnline) => set({ isOnline }),

  hydrate: () => {
    if (typeof window === 'undefined') return;
    const theme = (localStorage.getItem('theme') as Theme) || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    set({ theme });
  },
}));
