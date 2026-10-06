'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAuditTrail } from '@/services/audit';
import { useNotificationStore } from '@/stores/notification-store';

export function useNotifications() {
  const setNotifications = useNotificationStore((state) => state.setNotifications);
  const markRead = useNotificationStore((state) => state.markRead);

  const { data, isLoading } = useQuery<{ entries?: Array<{ id: string; action: string; timestamp: string; user?: string }> }>({
    queryKey: ['notifications'],
    queryFn: () => getAuditTrail() as Promise<{ entries?: Array<{ id: string; action: string; timestamp: string; user?: string }> }>,
    onSuccess: (data: { entries?: Array<{ id: string; action: string; timestamp: string; user?: string }> }) => {
      const notifications = (data?.entries ?? []).map((entry: { id: string; action: string; timestamp: string; user?: string }) => ({
        id: entry.id,
        recipient: entry.user ?? 'system',
        message: entry.action,
        channel: 'audit',
        read: false,
        created_at: entry.timestamp,
      }));
      setNotifications(notifications);
    },
  } as any);

  const markReadMutation = useMutation<void, Error, string>({
    mutationFn: (id: string) => Promise.resolve(markRead(id)),
  });

  return {
    notifications: useNotificationStore((state) => state.notifications),
    unreadCount: useNotificationStore((state) => state.unreadCount),
    isLoading,
    markAsRead: markReadMutation.mutate,
  };
}
