import { create } from "zustand";
import type { Notification } from "@/types/notification";
import { getNotifications, markNotificationRead } from "@/services/notification";

interface NotificationState {
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;
  loadNotifications: (recipient: string, limit?: number) => Promise<void>;
  markAsRead: (recipient: string, notificationId: string) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useNotificationStore = create<NotificationState>()((set, get) => ({
  notifications: [],
  isLoading: false,
  error: null,

  loadNotifications: async (recipient: string, limit = 50) => {
    set({ isLoading: true, error: null });
    try {
      const data = await getNotifications(recipient, limit);
      set({ notifications: data.notifications || [], isLoading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load notifications", isLoading: false });
    }
  },

  markAsRead: async (recipient: string, notificationId: string) => {
    await markNotificationRead(recipient, notificationId);
    set((state) => ({
      notifications: state.notifications.map((n) => (n.id === notificationId ? { ...n, read: true } : n)),
    }));
  },

  setError: (error: string | null) => set({ error }),
}));
