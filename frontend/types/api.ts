export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface CreateExecutionRequest {
  goal: string;
  capability_id?: string;
  workspace_id: string;
  conversation_id?: string;
  parameters?: Record<string, unknown>;
}

export interface ExecuteCapabilityRequest {
  capability_id: string;
  goal: string;
  workspace_id: string;
  parameters?: Record<string, unknown>;
}

