'use client';

import { UserProfile } from '@/components/settings/user-profile';
import { TokenScopeViewer } from '@/components/settings/token-scope-viewer';
import { SecurityPolicyList } from '@/components/settings/security-policy-list';
import { ApiKeyManager } from '@/components/settings/api-key-manager';

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Settings</h2>
        <p className="text-sm text-text-secondary">User profile, token scope, and security policies.</p>
      </div>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">User Profile</h3>
          <UserProfile />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Token Scope</h3>
          <TokenScopeViewer />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Security Policies</h3>
          <SecurityPolicyList />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">API Keys</h3>
          <ApiKeyManager />
        </div>
      </section>
    </div>
  );
}
