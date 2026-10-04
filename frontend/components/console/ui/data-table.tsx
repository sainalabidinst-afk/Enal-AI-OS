"use client";

import { useMemo, useState, type ReactNode } from "react";
import { ArrowDown, ArrowUp, Search } from "lucide-react";
import { cn } from "@/lib/utils";

export interface Column<T> {
  key: string;
  header: string;
  sortable?: boolean;
  align?: "left" | "right" | "center";
  width?: string;
  render: (row: T) => ReactNode;
  sortValue?: (row: T) => string | number;
}

export function DataTable<T>({
  rows,
  columns,
  rowKey,
  searchable = true,
  searchPlaceholder = "Filter rows…",
  emptyLabel = "No rows match the current filter",
  initialSort,
  dense = false,
}: {
  rows: T[];
  columns: Column<T>[];
  rowKey: (row: T) => string;
  searchable?: boolean;
  searchPlaceholder?: string;
  emptyLabel?: string;
  initialSort?: { key: string; direction: "asc" | "desc" };
  dense?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<{ key: string; direction: "asc" | "desc" } | null>(
    initialSort ?? null
  );

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const base = needle
      ? rows.filter((row) =>
          columns.some((column) =>
            String(column.sortValue ? column.sortValue(row) : column.render(row))
              .toLowerCase()
              .includes(needle)
          )
        )
      : rows;
    if (!sort) return base;
    const column = columns.find((item) => item.key === sort.key);
    if (!column?.sortValue) return base;
    const factor = sort.direction === "asc" ? 1 : -1;
    return [...base].sort((left, right) => {
      const a = column.sortValue!(left);
      const b = column.sortValue!(right);
      if (typeof a === "number" && typeof b === "number") return (a - b) * factor;
      return String(a).localeCompare(String(b)) * factor;
    });
  }, [rows, columns, query, sort]);

  function toggleSort(key: string) {
    setSort((current) =>
      current?.key === key
        ? { key, direction: current.direction === "asc" ? "desc" : "asc" }
        : { key, direction: "desc" }
    );
  }

  return (
    <div>
      {searchable && (
        <div className="flex items-center gap-2 border-b border-[var(--ecp-border)] px-4 py-2.5">
          <Search className="h-3.5 w-3.5 shrink-0 text-[var(--ecp-text-dim)]" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={searchPlaceholder}
            className="w-full bg-transparent text-xs text-[var(--ecp-text)] outline-none placeholder:text-[var(--ecp-text-dim)]"
          />
          {query && (
            <span className="shrink-0 text-[10px] text-[var(--ecp-text-dim)]">
              {filtered.length}/{rows.length}
            </span>
          )}
        </div>
      )}

      <div className="max-h-full overflow-auto">
        <table className="w-full border-collapse text-left">
          <thead className="sticky top-0 z-10 bg-[var(--ecp-surface-2)]">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  style={column.width ? { width: column.width } : undefined}
                  className={cn(
                    "whitespace-nowrap border-b border-[var(--ecp-border)] px-3 text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]",
                    dense ? "py-2" : "py-2.5",
                    column.align === "right" && "text-right",
                    column.align === "center" && "text-center"
                  )}
                >
                  {column.sortable ? (
                    <button
                      type="button"
                      onClick={() => toggleSort(column.key)}
                      className="inline-flex items-center gap-1 transition-colors hover:text-[var(--ecp-text)]"
                    >
                      {column.header}
                      {sort?.key === column.key &&
                        (sort.direction === "asc" ? (
                          <ArrowUp className="h-3 w-3" />
                        ) : (
                          <ArrowDown className="h-3 w-3" />
                        ))}
                    </button>
                  ) : (
                    column.header
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr
                key={rowKey(row)}
                className="border-b border-[var(--ecp-border)]/70 transition-colors last:border-0 hover:bg-[var(--ecp-surface-2)]"
              >
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={cn(
                      "px-3 align-middle text-xs text-[var(--ecp-text-muted)]",
                      dense ? "py-1.5" : "py-2.5",
                      column.align === "right" && "text-right",
                      column.align === "center" && "text-center"
                    )}
                  >
                    {column.render(row)}
                  </td>
                ))}
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-4 py-8 text-center text-xs text-[var(--ecp-text-dim)]"
                >
                  {emptyLabel}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}