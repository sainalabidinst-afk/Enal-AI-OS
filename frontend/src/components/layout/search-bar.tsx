'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { useRouter } from 'next/navigation';
import { Search, X } from 'lucide-react';
import { useUIStore } from '@/stores/ui-store';

export function SearchBar() {
  const [query, setQuery] = useState('');
  const router = useRouter();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);

  const { data, isError } = useQuery({
    queryKey: ['search', query],
    queryFn: () => apiClient.get('/api/v1/search', { params: { q: query } }),
    enabled: query.length > 2,
  });

  const results = data ?? {};

  if (sidebarCollapsed) return null;

  return (
    <div className="px-2 py-2">
      <div className="relative">
        <Search size={14} className="absolute left-3 top-2.5 text-text-muted" />
        <input
          className="w-full rounded-md border border-border bg-surface-primary pl-8 pr-8 py-1.5 text-xs outline-none focus:border-primary"
          placeholder="Search packs, providers, logs..."
          aria-label="Search packs, providers, and logs"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && query.trim()) {
              router.push(`/search?q=${encodeURIComponent(query.trim())}`);
            }
          }}
        />
        {query && (
          <button
            onClick={() => setQuery('')}
            className="absolute right-2 top-2 text-text-muted hover:text-text-primary"
            aria-label="Clear search"
          >
            <X size={12} />
          </button>
        )}
      </div>
      {query.length > 2 && (
        <div className="mt-2 max-h-48 overflow-auto rounded-md border border-border bg-surface-primary">
          {isError ? (
            <p className="px-3 py-2 text-xs text-warning" role="status">
              Search is unavailable. Check the backend connection.
            </p>
          ) : Object.entries(results).map(([domain, items]: [string, unknown[]]) => (
            <div key={domain} className="px-3 py-2">
              <p className="text-xs font-medium text-text-muted">{domain}</p>
              <div className="mt-1 space-y-1">
                {(items as Array<{ id: string; name: string }>).map((item) => (
                  <button
                    key={item.id}
                    onClick={() => router.push(`/search?q=${encodeURIComponent(item.name)}`)}
                    className="block w-full text-left text-xs text-text-secondary hover:text-text-primary"
                  >
                    {item.name}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
