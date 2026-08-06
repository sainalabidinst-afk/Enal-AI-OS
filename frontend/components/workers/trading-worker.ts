import type { Candle } from "../apps/trading/chart-engine/models/chart-models";

interface WorkerRequest {
  id: string;
  type: "indicator" | "analysis" | "signal";
  payload: unknown;
}

interface IndicatorRequest {
  type: "indicator";
  indicator: "sma" | "ema" | "rsi" | "macd" | "atr" | "bollinger";
  candles: Candle[];
  params?: Record<string, unknown>;
}

interface AnalysisRequest {
  type: "analysis";
  candles: Candle[];
  analysisType: "market-structure" | "signal" | "risk";
}

self.onmessage = (e: MessageEvent<WorkerRequest>) => {
  const { id, type, payload } = e.data;

  try {
    let result: unknown;

    if (type === "indicator") {
      result = calculateIndicator(payload as IndicatorRequest);
    } else if (type === "analysis") {
      result = runAnalysis(payload as AnalysisRequest);
    } else {
      throw new Error(`Unknown worker type: ${type}`);
    }

    self.postMessage({ id, result, error: null });
  } catch (error) {
    self.postMessage({
      id,
      result: null,
      error: error instanceof Error ? error.message : "Unknown error",
    });
  }
};

function calculateIndicator(request: IndicatorRequest): unknown {
  const { indicator, candles, params } = request;

  if (!candles || candles.length === 0) {
    return { values: [] };
  }

  switch (indicator) {
    case "sma": {
      const period = (params?.period as number) || 20;
      return calculateSMA(candles, period);
    }
    case "ema": {
      const period = (params?.period as number) || 20;
      return calculateEMA(candles, period);
    }
    case "rsi": {
      const period = (params?.period as number) || 14;
      return calculateRSI(candles, period);
    }
    default:
      return { values: [] };
  }
}

function calculateSMA(candles: Candle[], period: number): { values: number[] } {
  const values: number[] = [];

  for (let i = 0; i < candles.length; i++) {
    if (i < period - 1) {
      values.push(NaN);
      continue;
    }

    let sum = 0;
    for (let j = i - period + 1; j <= i; j++) {
      sum += candles[j].close;
    }
    values.push(sum / period);
  }

  return { values };
}

function calculateEMA(candles: Candle[], period: number): { values: number[] } {
  const values: number[] = [];
  const k = 2 / (period + 1);
  let ema = candles[0].close;

  for (let i = 0; i < candles.length; i++) {
    if (i === 0) {
      values.push(candles[i].close);
      continue;
    }

    const prevEma = values[i - 1];
    if (isNaN(prevEma)) {
      values.push(candles[i].close);
      continue;
    }

    ema = candles[i].close * k + prevEma * (1 - k);
    values.push(ema);
  }

  return { values };
}

function calculateRSI(candles: Candle[], period: number): { values: number[] } {
  const values: number[] = [];

  for (let i = 0; i < candles.length; i++) {
    if (i < period) {
      values.push(NaN);
      continue;
    }

    const slice = candles.slice(i - period, i + 1);
    let gains = 0;
    let losses = 0;

    for (let j = 1; j < slice.length; j++) {
      const change = slice[j].close - slice[j - 1].close;
      if (change > 0) gains += change;
      else losses += Math.abs(change);
    }

    const avgGain = gains / period;
    const avgLoss = losses / period;
    const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
    const rsi = 100 - 100 / (1 + rs);

    values.push(rsi);
  }

  return { values };
}

function runAnalysis(request: AnalysisRequest): unknown {
  const { candles, analysisType } = request;

  if (!candles || candles.length < 20) {
    return { error: "Insufficient data" };
  }

  switch (analysisType) {
    case "market-structure":
      return analyzeMarketStructure(candles);
    case "signal":
      return analyzeSignal(candles);
    default:
      return { error: "Unknown analysis type" };
  }
}

function analyzeMarketStructure(candles: Candle[]): unknown {
  const highs = candles.slice(-20).map((c) => c.high);
  const lows = candles.slice(-20).map((c) => c.low);

  let higherHighs = 0;
  let higherLows = 0;
  let lowerHighs = 0;
  let lowerLows = 0;

  for (let i = 1; i < highs.length; i++) {
    if (highs[i] > highs[i - 1]) higherHighs++;
    else lowerHighs++;
    if (lows[i] > lows[i - 1]) higherLows++;
    else lowerLows++;
  }

  let trend: "bullish" | "bearish" | "sideways" = "sideways";
  if (higherHighs > lowerHighs && higherLows > lowerLows) trend = "bullish";
  else if (lowerHighs > higherHighs && lowerLows > higherLows) trend = "bearish";

  return { trend, higherHighs, higherLows, lowerHighs, lowerLows };
}

function analyzeSignal(candles: Candle[]): unknown {
  const lastClose = candles[candles.length - 1].close;
  const sma20 = calculateSMA(candles, 20).values;
  const lastSma20 = sma20[sma20.length - 1];

  let signal: "buy" | "sell" | "wait" = "wait";
  if (lastClose > lastSma20 && !isNaN(lastSma20)) signal = "buy";
  else if (lastClose < lastSma20 && !isNaN(lastSma20)) signal = "sell";

  return { signal, confidence: 70 };
}
