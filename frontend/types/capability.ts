export interface Capability {
  id: string;
  name: string;
  description?: string;
  domain: string;
  workers?: string[];
  subtasks?: Array<{
    id: string;
    name: string;
    description?: string;
  }>;
}

export interface CapabilitySummary {
  domains: string[];
  total: number;
  details?: Record<string, any>;
}

export interface CapabilityListResponse {
  capabilities: Capability[];
  domains: string[];
}
