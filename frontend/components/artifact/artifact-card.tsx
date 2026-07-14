"use client";

import type { Artifact } from "@/types/artifact";
import { useArtifactStore } from "@/store/artifact-store";
import { ArtifactViewer } from "@/components/artifact/artifact-viewer";

interface ArtifactCardProps {
  artifact: Artifact;
  onClick?: () => void;
  onRestored?: () => void;
}

export function ArtifactCard({ artifact, onClick, onRestored }: ArtifactCardProps) {
  const isActive = useArtifactStore((s) => s.activeArtifactId) === artifact.id;
  const selectArtifact = useArtifactStore((s) => s.selectArtifact);

  const handleClick = () => {
    selectArtifact(artifact.id);
    onClick?.();
  };

  return (
    <button
      onClick={handleClick}
      className={`w-full text-left rounded-lg border p-4 transition-colors ${
        isActive ? "border-[var(--color-accent)] bg-[var(--color-bg-secondary)]" : "border-[var(--color-border)] bg-[var(--color-bg-secondary)] hover:border-[var(--color-text-secondary)]"
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium">{artifact.name}</p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">{artifact.type}</p>
          {artifact.description && <p className="text-xs text-[var(--color-text-secondary)] mt-1 line-clamp-2">{artifact.description}</p>}
        </div>
        <span className="text-xs text-[var(--color-text-secondary)]">v{artifact.current_version}</span>
      </div>

      {isActive && (
        <div className="mt-4">
          <ArtifactViewer artifact={artifact} onClose={() => selectArtifact(null)} onRestored={onRestored} />
        </div>
      )}
    </button>
  );
}
