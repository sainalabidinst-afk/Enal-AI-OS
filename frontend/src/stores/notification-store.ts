'use client';

import { create } from 'zustand';

export interface Notification {
  id: string;
  recipient: string;
  message: string;
  channel: string;
  metadata?: Record<string, unknown>;
  read: boolean;
  created_at: string;
}

interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  isLoading: boolean;
  setNotifications: (notifications: Notification[]) => void;
  appendNotifications: (items: Notification[]) => void;
  markRead: (id: string) => void;
  setUnreadCount: (count: number) => void;
  setLoading: (loading: boolean) => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  unreadCount: 0,
  isLoading: false,

  setNotifications: (notifications) =>
    set({
      notifications,
      unreadCount: notifications.filter((n) => !n.read).length,
    }),

  appendNotifications: (items) =>
    set((state) => ({
      notifications: [...items, ...state.notifications],
      unreadCount: state.unreadCount + items.filter((n) => !n.read).length,
    })),

  markRead: (id) =>
    set((state) => {
      const notifications = state.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      );
      return {
        notifications,
        unreadCount: notifications.filter((n) => !n.read).length,
      };
    }),

  setUnreadCount: (unreadCount) => set({ unreadCount }),
  setLoading: (isLoading) => set({ isLoading }),
}));
