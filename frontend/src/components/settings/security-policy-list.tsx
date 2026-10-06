'use client';

const policies = [
  { name: 'model:read', status: 'Granted' },
  { name: 'capabilities:execute', status: 'Granted' },
  { name: 'admin', status: 'Denied' },
];

export function SecurityPolicyList() {
  return (
    <div className="mt-4 space-y-2">
      {policies.map((item) => (
        <div key={item.name} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <span className="text-sm">{item.name}</span>
          <span className={`text-xs ${item.status === 'Granted' ? 'text-success' : 'text-danger'}`}>{item.status}</span>
        </div>
      ))}
    </div>
  );
}
