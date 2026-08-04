export interface CapabilityApp {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  route: string;
  domain: string;
  keywords: string[];
}

/**
 * Central registry of available capability "apps" shown in the App Launcher.
 * This is a pure data declaration — reusable by any Launcher / Marketplace UI.
 * Adding a new capability = adding a new entry here (no layout changes needed).
 */
export const CAPABILITY_APPS: CapabilityApp[] = [
  {
    id: "trading",
    name: "Trading Analyst",
    description: "Analyze market",
    icon: "📈",
    color: "#22c55e",
    route: "/apps/trading",
    domain: "trading",
    keywords: ["trading", "market", "stock", "analisis", "saham", "investasi"],
  },
  {
    id: "network",
    name: "Network Engineer",
    description: "Design & troubleshoot networks",
    icon: "🌐",
    color: "#3b82f6",
    route: "/apps/network",
    domain: "network",
    keywords: ["network", "jaringan", "router", "topology", "config"],
  },
  {
    id: "code",
    name: "Code Engineer",
    description: "Generate & review code",
    icon: "💻",
    color: "#8b5cf6",
    route: "/apps/code",
    domain: "code",
    keywords: ["code", "coding", "program", "source", "kode"],
  },
  {
    id: "security",
    name: "Security Engineer",
    description: "Audit & protect systems",
    icon: "🛡️",
    color: "#ef4444",
    route: "/apps/security",
    domain: "security",
    keywords: ["security", "keamanan", "vulnerability", "audit", "pentest"],
  },
  {
    id: "database",
    name: "Database Engineer",
    description: "Design & optimize databases",
    icon: "🗄️",
    color: "#f59e0b",
    route: "/apps/database",
    domain: "database",
    keywords: ["database", "sql", "schema", "query", "db"],
  },
  {
    id: "research",
    name: "Research Assistant",
    description: "Survey & synthesize research",
    icon: "📑",
    color: "#06b6d4",
    route: "/apps/research",
    domain: "research",
    keywords: ["research", "riset", "literature", "paper", "laporan"],
  },
  {
    id: "business",
    name: "Business Analyst",
    description: "Analyze business data",
    icon: "📊",
    color: "#10b981",
    route: "/apps/business",
    domain: "business",
    keywords: ["business", "bisnis", "analisis", "kpi", "data"],
  },
  {
    id: "devops",
    name: "DevOps Engineer",
    description: "Automate & deploy infrastructure",
    icon: "⚙️",
    color: "#6366f1",
    route: "/apps/devops",
    domain: "devops",
    keywords: ["devops", "ci", "cd", "deploy", "infrastructure", "kubernetes"],
  },
  {
    id: "architect",
    name: "System Architect",
    description: "Design system architecture",
    icon: "🏗️",
    color: "#a16207",
    route: "/apps/architect",
    domain: "architect",
    keywords: ["architect", "arsitektur", "system", "design", "modular"],
  },
  {
    id: "decision",
    name: "Decision Intelligence",
    description: "Support strategic decisions",
    icon: "🧠",
    color: "#ec4899",
    route: "/apps/decision",
    domain: "decision",
    keywords: ["decision", "keputusan", "intelligence", "strategi", "insight"],
  },
  {
    id: "self-development",
    name: "Self Development",
    description: "Improve your codebase",
    icon: "👤",
    color: "#14b8a6",
    route: "/apps/self-development",
    domain: "self-development",
    keywords: ["self", "development", "improve", "refactor", "improve"],
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
      ...app.keywords,
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(q);
  });
}
