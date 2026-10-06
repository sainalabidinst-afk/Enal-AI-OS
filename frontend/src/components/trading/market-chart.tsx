'use client';

import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { MetricsCard } from '@/components/shared/metrics-card';

interface MarketChartProps {
  symbol?: string;
  data?: { confidence?: number; timeframes?: string[]; regimes?: Record<string, { regime?: string; confidence?: number }> };
}

export function MarketChart({ symbol = 'BTCUSDT', data }: MarketChartProps) {
  const chartData = useMemo(() => {
    if (!data?.timeframes) return [];
    const confidence = data.confidence ?? 0;
    return data.timeframes.map((tf, idx) => ({
      timeframe: tf,
      confidence: confidence * (0.8 + idx * 0.05),
    }));
  }, [data]);

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-3">
        <MetricsCard title="Symbol" value={symbol} />
        <MetricsCard title="Confidence" value={data?.confidence !== undefined ? `${Math.round((data.confidence as number) * 100)}%` : '-'} />
        <MetricsCard title="Regime" value={data?.regimes ? Object.values(data.regimes)[0]?.regime ?? '-' : '-'} />
      </div>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorConfidence" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="timeframe" stroke="var(--color-text-muted)" fontSize={12} />
            <YAxis stroke="var(--color-text-muted)" fontSize={12} domain={[0, 1]} />
            <Tooltip
              contentStyle={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)' }}
              labelStyle={{ color: 'var(--color-text-primary)' }}
            />
            <Area type="monotone" dataKey="confidence" stroke="var(--color-primary)" fillOpacity={1} fill="url(#colorConfidence)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
