"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export function WorkspaceSearch() {
  const [query, setQuery] = useState("");

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--color-text-secondary)]" />
      <Input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="pl-9 h-8 w-64 text-xs"
      />
      {query && (
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setQuery("")}
          className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6"
        >
          ×
        </Button>
      )}
    </div>
  );
}
