export type CapabilityStatus = "Ready" | "Beta" | "Coming Soon" | "Installed";

export interface CapabilityApp {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  route: string;
  domain: string;
  category: string;
  status: CapabilityStatus;
  version: string;
  keywords: string[];
}

/**
 * Central registry of available capability "apps" shown in the App Launcher.
 * This is a pure data declaration — reusable by any Launcher / Marketplace UI.
 * Adding a new capability = adding a new entry here (no layout changes needed).
 *
 * `status` drives the badge shown on each card:
 *   - "Ready"       → fully usable
 *   - "Beta"        → available but experimental
 *   - "Coming Soon" → shown but not yet built
 *   - "Installed"   → already installed
 */
export const CAPABILITY_APPS: CapabilityApp[] = [
  {
    id: "trading",
    name: "Trading Analyst",
    description: "Analyze market data, trends, and indicators",
    icon: "📈",
    color: "#22c55e",
    route: "/apps/trading",
    domain: "trading",
    category: "Finance",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["trading", "market", "stock", "analisis", "saham", "investasi", "crypto", "analysis"],
  },
  {
    id: "network",
    name: "Network Engineer",
    description: "Design & troubleshoot networks",
    icon: "🌐",
    color: "#3b82f6",
    route: "/apps/network",
    domain: "network",
    category: "Infrastructure",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["network", "jaringan", "router", "topology", "config", "firewall", "switch"],
  },
  {
    id: "code",
    name: "Code Engineer",
    description: "Generate & review code",
    icon: "💻",
    color: "#8b5cf6",
    route: "/apps/code",
    domain: "code",
    category: "Development",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["code", "coding", "program", "source", "kode", "developer", "engineering"],
  },
  {
    id: "security",
    name: "Security Engineer",
    description: "Audit & protect systems",
    icon: "🛡️",
    color: "#ef4444",
    route: "/apps/security",
    domain: "security",
    category: "Infrastructure",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["security", "keamanan", "vulnerability", "audit", "pentest", "firewall"],
  },
  {
    id: "database",
    name: "Database Engineer",
    description: "Design & optimize databases",
    icon: "🗄️",
    color: "#f59e0b",
    route: "/apps/database",
    domain: "database",
    category: "Data",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["database", "sql", "schema", "query", "db", "storage"],
  },
  {
    id: "research",
    name: "Research Assistant",
    description: "Survey & synthesize research",
    icon: "📑",
    color: "#06b6d4",
    route: "/apps/research",
    domain: "research",
    category: "Knowledge",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["research", "riset", "literature", "paper", "laporan", "study"],
  },
  {
    id: "business",
    name: "Business Analyst",
    description: "Analyze business data",
    icon: "📊",
    color: "#10b981",
    route: "/apps/business",
    domain: "business",
    category: "Business",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["business", "bisnis", "analisis", "kpi", "revenue", "commerce"],
  },
  {
    id: "devops",
    name: "DevOps Engineer",
    description: "Automate & deploy infrastructure",
    icon: "⚙️",
    color: "#6366f1",
    route: "/apps/devops",
    domain: "devops",
    category: "Infrastructure",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["devops", "ci", "cd", "deploy", "infrastructure", "kubernetes", "automation"],
  },
  {
    id: "architect",
    name: "System Architect",
    description: "Design system architecture",
    icon: "🏗️",
    color: "#a16207",
    route: "/apps/architect",
    domain: "architect",
    category: "Development",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["architect", "arsitektur", "system", "design", "modular", "blueprint"],
  },
  {
    id: "decision",
    name: "Decision Intelligence",
    description: "Support strategic decisions",
    icon: "🧠",
    color: "#ec4899",
    route: "/apps/decision",
    domain: "decision",
    category: "Intelligence",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["decision", "keputusan", "intelligence", "strategi", "insight", "analytics"],
  },
  {
    id: "self-development",
    name: "Self Development",
    description: "Improve your codebase",
    icon: "👤",
    color: "#14b8a6",
    route: "/apps/self-development",
    domain: "self-development",
    category: "Development",
    status: "Coming Soon",
    version: "1.0.0",
    keywords: ["self", "development", "improve", "refactor", "improve", "codebase"],
  },
];

export function findCapabilityApp(id: string): CapabilityApp | undefined {
  return CAPABILITY_APPS.find((app) => app.id === id);
}

export function searchCapabilityApps(query: string): CapabilityApp[] {
  const q = query.trim().toLowerCase();
  if (!q) return CAPABILITY_APPS;
  return CAPABILITY_APPS.filter((app) => {
    const haystack = [
      app.name,
      app.description,
      app.domain,
      app.category,
      ...app.keywords,
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(q);
  });
}
