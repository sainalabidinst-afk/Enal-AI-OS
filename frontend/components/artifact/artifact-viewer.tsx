"use client";

import type { Artifact, ArtifactVersion } from "@/types/artifact";
import { useState } from "react";
import { useArtifactStore } from "@/store/artifact-store";
import { ApprovalDialog } from "@/components/ui/approval-dialog";

interface ArtifactViewerProps {
  artifact: Artifact;
  onClose: () => void;
  onRestored?: () => void;
  onDeleted?: () => void;
}

export function ArtifactViewer({ artifact, onClose, onRestored, onDeleted }: ArtifactViewerProps) {
  const [selectedVersion, setSelectedVersion] = useState<number>(artifact.current_version);
  const [restoreOpen, setRestoreOpen] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const restoreVersion = useArtifactStore((s) => s.restoreVersion);
  const deleteArtifact = useArtifactStore((s) => s.deleteArtifact);

  const version = artifact.versions.find((v) => v.version === selectedVersion) ?? artifact.versions[artifact.versions.length - 1];
  const isActive = selectedVersion === artifact.current_version;

  const handleRestore = async () => {
    setRestoring(true);
    setError(null);
    try {
      await restoreVersion(artifact.id, selectedVersion);
      setRestoreOpen(false);
      onRestored?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to restore version");
    } finally {
      setRestoring(false);
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    setError(null);
    try {
      await deleteArtifact(artifact.id);
      onDeleted?.();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete artifact");
    } finally {
      setDeleting(false);
    }
  };

  const handleDownload = () => {
    if (!version?.content) return;
    const blob = new Blob([version.content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${artifact.name || "artifact"}-v${selectedVersion}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-3xl rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] shadow-lg">
        <div className="flex items-center justify-between border-b border-[var(--color-border)] px-6 py-4">
          <div>
            <h2 className="text-lg font-semibold">{artifact.name}</h2>
            <p className="text-xs text-[var(--color-text-secondary)]">
              {artifact.type} • Version {selectedVersion} of {artifact.current_version}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={handleDownload} className="text-xs rounded-lg border border-[var(--color-border)] px-3 py-1 hover:bg-[var(--color-bg-tertiary)]">
              Download
            </button>
            <button onClick={handleDelete} disabled={deleting} className="text-xs rounded-lg border border-[var(--color-danger)] px-3 py-1 text-[var(--color-danger)] hover:bg-[var(--color-danger)]/10 disabled:opacity-50">
              {deleting ? "Deleting..." : "Delete"}
            </button>
            <button onClick={onClose} className="text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]">
              ✕
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row">
          <div className="w-full lg:w-48 border-b lg:border-b-0 lg:border-r border-[var(--color-border)] p-4 space-y-2">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Versions</p>
            <div className="space-y-1">
              {artifact.versions.map((v) => (
                <button
                  key={v.version}
                  onClick={() => setSelectedVersion(v.version)}
                  className={`w-full rounded-md px-3 py-2 text-left text-sm ${
                    selectedVersion === v.version
                      ? "bg-[var(--color-accent)] text-white"
                      : "hover:bg-[var(--color-bg-tertiary)]"
                  }`}
                >
                  v{v.version}
                </button>
              ))}
            </div>
            {!isActive && (
              <button
                onClick={() => setRestoreOpen(true)}
                className="w-full rounded-lg border border-[var(--color-accent)] px-3 py-2 text-sm text-[var(--color-accent)] hover:bg-[var(--color-accent)]/10"
              >
                Restore this version
              </button>
            )}
          </div>

          <div className="flex-1 p-6">
            {version ? (
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Content</p>
                  <pre className="mt-2 rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4 text-sm whitespace-pre-wrap">
                    {version.content || "(no content)"}
                  </pre>
                </div>
                {version.path && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Path</p>
                    <p className="mt-1 text-sm">{version.path}</p>
                  </div>
                )}
                <p className="text-xs text-[var(--color-text-secondary)]">
                  Created: {new Date(version.created_at).toLocaleString()}
                </p>
              </div>
            ) : (
              <p className="text-sm text-[var(--color-text-secondary)]">No version selected.</p>
            )}
          </div>
        </div>

        {error && (
          <div className="mx-6 mb-4 rounded-md border border-[var(--color-danger)] bg-[var(--color-bg-primary)] px-4 py-3 text-sm text-[var(--color-danger)]">
            {error}
          </div>
        )}

        <ApprovalDialog
          open={restoreOpen}
          title="Restore artifact version"
          description={`This will restore artifact "${artifact.name}" to version ${selectedVersion}. This action cannot be undone.`}
          reason="User requested version restore"
          impact="Current version will be replaced. A new version will be created from the restored content."
          confirmLabel="Restore"
          onConfirm={handleRestore}
          onCancel={() => setRestoreOpen(false)}
        />

        <ApprovalDialog
          open={deleting}
          title="Delete artifact"
          description={`This will permanently delete artifact "${artifact.name}". This action cannot be undone.`}
          reason="User requested artifact deletion"
          impact="All versions will be removed."
          confirmLabel="Delete"
          danger
          onConfirm={handleDelete}
          onCancel={() => setDeleting(false)}
        />
      </div>
    </div>
  );
}
