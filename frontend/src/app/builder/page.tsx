'use client';

import { PackForm } from '@/components/builder/pack-form';
import { CapabilityEditor } from '@/components/builder/capability-editor';
import { PolicyEditor } from '@/components/builder/policy-editor';
import { BlueprintImportExport } from '@/components/builder/blueprint-import-export';

export default function BuilderPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Builder</h2>
        <p className="text-sm text-text-secondary">Create and register new capability packs.</p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <PackForm />
        <div className="space-y-4">
          <CapabilityEditor />
          <PolicyEditor />
        </div>
      </div>

      <BlueprintImportExport />
    </div>
  );
}
