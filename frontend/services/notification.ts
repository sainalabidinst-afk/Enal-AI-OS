import { api } from "./api";
import type { Notification, NotificationCreateRequest } from "@/types/notification";

export async function sendNotification(
  request: NotificationCreateRequest
): Promise<Notification> {
  return api.post<Notification>("/api/v1/notifications", request);
}

export async function getNotifications(recipient: string, limit = 50): Promise<{ recipient: string; notifications: Notification[] }> {
  const qs = limit !== 50 ? `?limit=${limit}` : "";
  return api.get(`/api/v1/notifications/${encodeURIComponent(recipient)}${qs}`);
}

export async function markNotificationRead(
  recipient: string,
  notificationId: string
): Promise<{ read: boolean }> {
  return api.patch(`/api/v1/notifications/${encodeURIComponent(recipient)}/read/${notificationId}`);
}
