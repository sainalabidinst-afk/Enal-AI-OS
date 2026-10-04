import { api } from "@/services/api";
import type {
  CloneReceipt,
  ListingAnalytics,
  MarketplaceListing,
  MarketplaceTemplate,
} from "@/types/console";

export function listTemplates(params?: {
  category?: string;
  search?: string;
}) {
  const search = new URLSearchParams();
  if (params?.category) search.set("category", params.category);
  if (params?.search) search.set("search", params.search);
  const query = search.toString();
  return api.get<MarketplaceTemplate[]>(
    `/api/v1/marketplace/templates${query ? `?${query}` : ""}`
  );
}

export function getTemplate(templateId: string) {
  return api.get<MarketplaceTemplate>(
    `/api/v1/marketplace/templates/${encodeURIComponent(templateId)}`
  );
}

export function cloneTemplate(templateId: string, targetProject = "default") {
  return api.post<CloneReceipt>(
    `/api/v1/marketplace/clone/${encodeURIComponent(templateId)}?target_project=${encodeURIComponent(
      targetProject
    )}`
  );
}

export function listListings() {
  return api.get<MarketplaceListing[]>("/api/v1/marketplace");
}

export function shareAgent(payload: {
  agent_id: string;
  visibility?: string;
  allowed_roles?: string[];
  allow_clone?: boolean;
}) {
  return api.post<MarketplaceListing>("/api/v1/marketplace/share", payload);
}

export function unshareAgent(agentId: string) {
  return api.delete<{ message: string }>(
    `/api/v1/marketplace/share/${encodeURIComponent(agentId)}`
  );
}

export function getListingAnalytics(agentId: string) {
  return api.get<ListingAnalytics>(
    `/api/v1/marketplace/analytics/${encodeURIComponent(agentId)}`
  );
}