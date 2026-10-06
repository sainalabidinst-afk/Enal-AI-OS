'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAuditTrail } from '@/services/audit';
import { useNotificationStore } from '@/stores/notification-store';

export function useNotifications() {
  const setNotifications = useNotificationStore((state) => state.setNotifications);
  const markRead = useNotificationStore((state) => state.markRead);

  const { data, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => getAuditTrail(),
    onSuccess: (data) => {
      const notifications = (data?.entries ?? []).map((entry: { id: string; action: string; timestamp: string }) => ({
        id: entry.id,
        recipient: entry.user ?? 'system',
        message: entry.action,
        channel: 'audit',
        read: false,
        created_at: entry.timestamp,
      }));
      setNotifications(notifications);
    },
  });

  const markReadMutation = useMutation({
    mutationFn: (id: string) => markRead(id),
  });

  return {
    notifications: useNotificationStore((state) => state.notifications),
    unreadCount: useNotificationStore((state) => state.unreadCount),
    isLoading,
    markAsRead: markReadMutation.mutate,
  };
}
