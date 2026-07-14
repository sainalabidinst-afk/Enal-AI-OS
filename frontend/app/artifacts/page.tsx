"use client";

import { useArtifactStore } from "@/store/artifact-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { ArtifactCard } from "@/components/artifact/artifact-card";

export default function ArtifactsPage() {
  const artifacts = useArtifactStore((s) => s.artifacts);
  const loadArtifacts = useArtifactStore((s) => s.loadArtifacts);
  const activeWorkspaceId = useWorkspaceStore((s) => s.activeWorkspaceId);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-xl font-bold">Artifacts</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {artifacts.map((artifact) => (
          <ArtifactCard key={artifact.id} artifact={artifact} />
        ))}
      </div>
    </div>
  );
}
