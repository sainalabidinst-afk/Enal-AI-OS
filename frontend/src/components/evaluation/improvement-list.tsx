'use client';

const improvements = [
  'Reduce cold-start latency',
  'Improve parser coverage',
  'Add fallback provider',
];

export function ImprovementList() {
  return (
    <div className="mt-4 space-y-2">
      {improvements.map((item) => (
        <div key={item} className="rounded-md border border-border px-3 py-2 text-sm text-text-secondary">
          {item}
        </div>
      ))}
    </div>
  );
}
