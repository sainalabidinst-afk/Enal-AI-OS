"""
Additional Technical Indicators for Trading Analyst.

Provides:
- OBV (On-Balance Volume)
- Stochastic Oscillator
- Fibonacci Retracement
- ADX (Average Directional Index)
- Parabolic SAR
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def compute_obv(closes: list[float], volumes: list[float]) -> list[float]:
    """On-Balance Volume."""
    if len(closes) != len(volumes) or len(closes) < 2:
        return []
    obv = [volumes[0]]
    for i in range(1, len(closes)):
        if closes[i] > closes[i - 1]:
            obv.append(obv[-1] + volumes[i])
        elif closes[i] < closes[i - 1]:
            obv.append(obv[-1] - volumes[i])
        else:
            obv.append(obv[-1])
    return obv


def compute_stochastic(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    k_period: int = 14,
    d_period: int = 3,
) -> dict[str, list[float]]:
    """Stochastic Oscillator (%K and %D)."""
    if len(closes) < k_period:
        return {"k": [], "d": []}
    k_values: list[float] = []
    for i in range(k_period - 1, len(closes)):
        lowest_low = min(lows[i - k_period + 1 : i + 1])
        highest_high = max(highs[i - k_period + 1 : i + 1])
        if highest_high == lowest_low:
            k_values.append(50.0)
        else:
            k_values.append(100.0 * (closes[i] - lowest_low) / (highest_high - lowest_low))
    d_values = []
    for i in range(d_period - 1, len(k_values)):
        d_values.append(sum(k_values[i - d_period + 1 : i + 1]) / d_period)
    return {"k": k_values, "d": d_values}


def compute_fibonacci_retracement(high: float, low: float) -> dict[str, float]:
    """Calculate Fibonacci retracement levels."""
    if high <= low:
        return {}
    diff = high - low
    return {
        "0.0%": high,
        "23.6%": high - diff * 0.236,
        "38.2%": high - diff * 0.382,
        "50.0%": high - diff * 0.5,
        "61.8%": high - diff * 0.618,
        "100.0%": low,
    }


def compute_adx(
    highs: list[float], lows: list[float], closes: list[float], period: int = 14
) -> list[float]:
    """Average Directional Index."""
    if len(closes) < period + 1:
        return []
    tr_list = []
    for i in range(1, len(highs)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        tr_list.append(tr)
    plus_dm = []
    minus_dm = []
    for i in range(1, len(highs)):
        up = highs[i] - highs[i - 1]
        down = lows[i - 1] - lows[i]
        plus_dm.append(up if up > down and up > 0 else 0.0)
        minus_dm.append(down if down > up and down > 0 else 0.0)
    atr = [sum(tr_list[:period]) / period]
    plus_di = [sum(plus_dm[:period]) / period]
    minus_di = [sum(minus_dm[:period]) / period]
    for i in range(period, len(tr_list)):
        atr.append((atr[-1] * (period - 1) + tr_list[i]) / period)
        plus_di.append((plus_di[-1] * (period - 1) + plus_dm[i]) / period)
        minus_di.append((minus_di[-1] * (period - 1) + minus_dm[i]) / period)
    dx = []
    for i in range(len(plus_di)):
        denom = plus_di[i] + minus_di[i]
        if denom == 0:
            dx.append(0.0)
        else:
            dx.append(100.0 * abs(plus_di[i] - minus_di[i]) / denom)
    adx = [sum(dx[:period]) / period]
    for i in range(period, len(dx)):
        adx.append((adx[-1] * (period - 1) + dx[i]) / period)
    return adx


def compute_parabolic_sar(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    af_start: float = 0.02,
    af_max: float = 0.2,
) -> list[float]:
    """Parabolic SAR."""
    if len(closes) < 2:
        return []
    psar = [lows[0]]
    uptrend = closes[0] > closes[1] if len(closes) > 1 else True
    af = af_start
    ep = highs[0] if uptrend else lows[0]
    for i in range(1, len(closes)):
        prev_psar = psar[-1]
        if uptrend:
            psar.append(prev_psar + af * (ep - prev_psar))
            psar[-1] = min(psar[-1], lows[i - 1], lows[i - 2] if i >= 2 else lows[i - 1])
            if lows[i] < psar[-1]:
                uptrend = False
                psar[-1] = ep
                ep = lows[i]
                af = af_start
            else:
                if highs[i] > ep:
                    ep = highs[i]
                    af = min(af + af_start, af_max)
        else:
            psar.append(prev_psar - af * (prev_psar - ep))
            psar[-1] = max(psar[-1], highs[i - 1], highs[i - 2] if i >= 2 else highs[i - 1])
            if highs[i] > psar[-1]:
                uptrend = True
                psar[-1] = ep
                ep = highs[i]
                af = af_start
            else:
                if lows[i] < ep:
                    ep = lows[i]
                    af = min(af + af_start, af_max)
    return psar
