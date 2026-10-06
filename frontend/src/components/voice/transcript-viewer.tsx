'use client';

const sampleTranscripts = [
  { role: 'user', text: 'What is the current market regime?' },
  { role: 'assistant', text: 'The current regime is bullish with 0.85 confidence.' },
  { role: 'user', text: 'Execute capability pack trading-analyzer.' },
  { role: 'assistant', text: 'Capability executed successfully.' },
];

export function TranscriptViewer() {
  return (
    <div className="mt-4 space-y-3">
      {sampleTranscripts.map((item, idx) => (
        <div key={idx} className="rounded-md border border-border bg-surface-primary p-3">
          <p className="text-xs font-medium text-text-muted">{item.role}</p>
          <p className="text-sm text-text-secondary">{item.text}</p>
        </div>
      ))}
    </div>
  );
}
