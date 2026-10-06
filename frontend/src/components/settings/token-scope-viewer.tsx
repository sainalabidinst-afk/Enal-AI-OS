'use client';

const scopes = [
  { scope: 'model:read', granted: true },
  { scope: 'capabilities:execute', granted: true },
  { scope: 'admin', granted: false },
];

export function TokenScopeViewer() {
  return (
    <div className="mt-4 space-y-2">
      {scopes.map((item) => (
        <div key={item.scope} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <span className="text-sm font-mono">{item.scope}</span>
          <span className={`text-xs ${item.granted ? 'text-success' : 'text-text-muted'}`}>{item.granted ? 'Granted' : 'Denied'}</span>
        </div>
      ))}
    </div>
  );
}
