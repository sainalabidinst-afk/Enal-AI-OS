export interface Notification {
  id: string;
  recipient: string;
  message: string;
  channel: string;
  read: boolean;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface NotificationCreateRequest {
  recipient: string;
  message: string;
  channel?: string;
  metadata?: Record<string, any>;
}
