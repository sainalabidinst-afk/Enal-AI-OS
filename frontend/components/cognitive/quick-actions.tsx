"use client";

import { useState, useCallback, useMemo } from "react";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CAPABILITY_APPS, type CapabilityApp } from "@/components/apps/capability-registry";
import { cn } from "@/lib/utils";

const CATEGORY_ICONS: Record<string, string> = {
  Finance: "📈",
  Infrastructure: "🌐",
  Development: "💻",
  Data: "🗄️",
  Knowledge: "📑",
  Business: "📊",
  Intelligence: "🧠",
};

export function QuickActions() {
  const setActiveCapability = useCognitiveStore((s) => s.setActiveCapability);
  const [activeCategory, setActiveCategory] = useState<string>("all");

  const categories = useMemo(() => {
    const cats = new Set(CAPABILITY_APPS.map((app) => app.category));
    return ["all", ...Array.from(cats)];
  }, []);

  const filtered =
    activeCategory === "all"
      ? CAPABILITY_APPS
      : CAPABILITY_APPS.filter((app) => app.category === activeCategory);

  const handleQuickAction = useCallback(
    (app: CapabilityApp) => {
      setActiveCapability(app.id);
    },
    [setActiveCapability]
  );

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-1.5">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={cn(
              "rounded-full px-3 py-1 text-[10px] font-medium transition-all",
              activeCategory === cat
                ? "bg-[var(--color-accent)] text-white shadow-md"
                : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)]"
            )}
          >
            {cat === "all" ? "All" : `${CATEGORY_ICONS[cat] ?? "📦"} ${cat}`}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {filtered.map((app) => (
          <QuickActionCard
            key={app.id}
            app={app}
            onClick={() => handleQuickAction(app)}
          />
        ))}
      </div>
    </div>
  );
}

interface QuickActionCardProps {
  app: CapabilityApp;
  onClick: () => void;
}

function QuickActionCard({ app, onClick }: QuickActionCardProps) {
  const [pressed, setPressed] = useState(false);

  const handleClick = () => {
    setPressed(true);
    setTimeout(() => setPressed(false), 300);
    onClick();
  };

  return (
    <button
      onClick={handleClick}
      className={cn(
        "flex items-center gap-3 rounded-lg border p-3 text-left transition-all duration-150",
        "border-[var(--color-border)] bg-[var(--color-bg-secondary)]",
        "hover:border-[var(--color-accent)] hover:shadow-md",
        pressed && "scale-95 opacity-75"
      )}
      style={{ color: app.color }}
    >
      <span className="text-lg shrink-0" style={{ color: app.color }}>
        {app.icon}
      </span>
      <div className="min-w-0 flex-1">
        <div className="text-xs font-semibold text-[var(--color-text-primary)]">
          {app.name}
        </div>
        <p className="text-[10px] text-[var(--color-text-secondary)] truncate">
          {app.description}
        </p>
        <div className="mt-1 flex flex-wrap gap-1">
          {app.keywords.slice(0, 2).map((kw) => (
            <span
              key={kw}
              className="rounded bg-[var(--color-bg-primary)] px-1.5 py-0.5 text-[9px] text-[var(--color-text-secondary)]"
            >
              {kw}
            </span>
          ))}
        </div>
      </div>
      <span
        className="text-[10px] uppercase font-medium"
        style={{ color: app.color, opacity: 0.8 }}
      >
        {app.version}
      </span>
    </button>
  );
}
