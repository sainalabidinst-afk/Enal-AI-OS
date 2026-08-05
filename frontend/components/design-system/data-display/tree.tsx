"use client";

import { type ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { ChevronRight, ChevronDown, Folder, File } from "lucide-react";

interface TreeNode {
  id: string;
  label: string;
  icon?: "folder" | "file";
  children?: TreeNode[];
}

interface TreeProps {
  nodes: TreeNode[];
  onSelect?: (node: TreeNode) => void;
  className?: string;
}

export function Tree({ nodes, onSelect, className }: TreeProps) {
  return (
    <div className={cn("space-y-1", className)}>
      {nodes.map((node) => (
        <TreeNode key={node.id} node={node} onSelect={onSelect} />
      ))}
    </div>
  );
}

export { TreeNode };

function TreeNode({ node, onSelect }: { node: TreeNode; onSelect?: (node: TreeNode) => void }) {
  const [open, setOpen] = useState(false);
  const Icon = node.icon === "folder" ? Folder : File;
  const hasChildren = node.children && node.children.length > 0;

  return (
    <div>
      <button
        onClick={() => {
          if (hasChildren) setOpen(!open);
          onSelect?.(node);
        }}
        className="flex items-center gap-1 w-full px-2 py-1 text-sm rounded hover:bg-[var(--color-secondary-100)] transition-colors"
      >
        {hasChildren && (
          <span className="w-4 h-4 flex items-center justify-center">
            {open ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          </span>
        )}
        {!hasChildren && <span className="w-4 h-4" />}
        <Icon className="h-4 w-4 text-[var(--color-secondary-500)]" />
        <span className="text-[var(--color-foreground)]">{node.label}</span>
      </button>
      {open && hasChildren && (
        <div className="ml-4 border-l border-[var(--color-border)] pl-2">
          {node.children!.map((child) => (
            <TreeNode key={child.id} node={child} onSelect={onSelect} />
          ))}
        </div>
      )}
    </div>
  );
}
