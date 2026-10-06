'use client';

import { useRef } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { useToast } from '@/components/shared/toast';
import { Loader2, Upload, Download } from 'lucide-react';

export function BlueprintImportExport() {
  const fileRef = useRef<HTMLInputElement>(null);
  const addToast = useToast((state) => state.addToast);

  const importMutation = useMutation({
    mutationFn: (file: File) => {
      const reader = new FileReader();
      return new Promise<Record<string, unknown>>((resolve, reject) => {
        reader.onload = () => {
          try {
            const json = JSON.parse(reader.result as string);
            resolve(apiClient.post('/api/v1/blueprints/import', json));
          } catch {
            reject(new Error('Invalid JSON'));
          }
        };
        reader.onerror = () => reject(reader.error);
        reader.readAsText(file);
      });
    },
    onSuccess: () => addToast('success', 'Blueprint imported'),
    onError: () => addToast('error', 'Import failed'),
  });

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) importMutation.mutate(file);
  };

  const handleExport = () => {
    apiClient.get('/api/v1/blueprints/export').then((data) => {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'blueprint.json';
      a.click();
      URL.revokeObjectURL(url);
      addToast('success', 'Blueprint exported');
    }).catch(() => addToast('error', 'Export failed'));
  };

  return (
    <div className="flex items-center gap-3 rounded-lg border border-border bg-surface-secondary p-4">
      <div>
        <h3 className="text-sm font-semibold">Blueprint Import / Export</h3>
        <p className="text-xs text-text-secondary">Share blueprints between environments.</p>
      </div>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-xs hover:bg-surface-hover"
        >
          <Upload size={14} />
          Import
        </button>
        <input ref={fileRef} type="file" accept="application/json" className="hidden" onChange={handleImport} />
        <button
          type="button"
          onClick={handleExport}
          className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-xs hover:bg-surface-hover"
        >
          <Download size={14} />
          Export
        </button>
      </div>
    </div>
  );
}
