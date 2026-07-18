export interface Capability {
  id: string;
  name: string;
  description?: string;
  domain: string;
  workers?: string[];
  skills?: string[];
  tags?: string[];
  dependencies?: string[];
  complexity?: string;
  related_capabilities?: string[];
  subtask_templates?: Array<{
    id: string;
    name: string;
    description?: string;
    required_skills?: string[];
    produces_artifact?: boolean;
    estimated_duration_minutes?: number;
    priority?: string;
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
