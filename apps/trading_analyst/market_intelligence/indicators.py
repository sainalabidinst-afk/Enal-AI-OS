"""
Technical Indicators
====================

Pure functions for computing technical indicators from OHLCV data.
No state, no side effects. Input → Output.
"""

import statistics
import math
from typing import Any


def compute_ema(prices: list[float], period: int) -> list[float]:
    """Exponential Moving Average."""
    if len(prices) < period:
        return []
    multiplier = 2 / (period + 1)
    ema = [sum(prices[:period]) / period]
    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema


def compute_sma(prices: list[float], period: int) -> list[float]:
    """Simple Moving Average."""
    if len(prices) < period:
        return []
    return [sum(prices[i - period:i]) / period for i in range(period, len(prices) + 1)]


def compute_rsi(prices: list[float], period: int = 14) -> list[float]:
    """Relative Strength Index."""
    if len(prices) < period + 1:
        return []
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsi = []
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100 - (100 / (1 + rs)))
    return rsi


def compute_macd(prices: list[float]) -> dict[str, list[float]]:
    """MACD (12, 26, 9)."""
    ema12 = compute_ema(prices, 12)
    ema26 = compute_ema(prices, 26)
    if not ema12 or not ema26:
        return {"macd": [], "signal": [], "histogram": []}
    min_len = min(len(ema12), len(ema26))
    macd_line = [ema12[i] - ema26[i] for i in range(min_len)]
    signal = compute_ema(macd_line, 9) if len(macd_line) >= 9 else []
    histogram = []
    for i in range(len(signal)):
        histogram.append(macd_line[i + len(macd_line) - len(signal)] - signal[i])
    return {"macd": macd_line, "signal": signal, "histogram": histogram}


def compute_bollinger_bands(prices: list[float], period: int = 20, std_dev: float = 2.0) -> dict[str, list[float]]:
    """Bollinger Bands."""
    if len(prices) < period:
        return {"upper": [], "middle": [], "lower": []}
    middle = compute_sma(prices, period)
    upper, lower = [], []
    for i in range(len(prices) - period):
        window = prices[i:i + period]
        std = statistics.stdev(window)
        upper.append(middle[i] + std_dev * std)
        lower.append(middle[i] - std_dev * std)
    return {"upper": upper, "middle": middle, "lower": lower}


def compute_atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> list[float]:
    """Average True Range."""
    if len(highs) < 2:
        return []
    tr = []
    for i in range(1, len(highs)):
        tr.append(max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        ))
    if len(tr) < period:
        return []
    atr = [sum(tr[:period]) / period]
    for val in tr[period:]:
        atr.append((atr[-1] * (period - 1) + val) / period)
    return atr


def compute_linear_regression(prices: list[float]) -> tuple[float, float]:
    """
    Simple linear regression.

    Returns:
        (slope, intercept)
    """
    n = len(prices)
    if n < 2:
        return 0.0, 0.0
    x = list(range(n))
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(prices)
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, prices))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    slope = numerator / denominator if denominator != 0 else 0.0
    intercept = y_mean - slope * x_mean
    return slope, intercept


def detect_swing_points(highs: list[float], lows: list[float], window: int = 5) -> dict[str, list[int]]:
    """Detect swing highs and lows. Returns dict with 'highs' and 'lows' as list of indices."""
    swing_highs, swing_lows = [], []
    for i in range(window, len(highs) - window):
        if all(highs[i] > highs[j] for j in range(i - window, i)) and \
           all(highs[i] > highs[j] for j in range(i + 1, i + window + 1)):
            swing_highs.append(i)
        if all(lows[i] < lows[j] for j in range(i - window, i)) and \
           all(lows[i] < lows[j] for j in range(i + 1, i + window + 1)):
            swing_lows.append(i)
    return {"highs": swing_highs, "lows": swing_lows}


def compute_volume_stats(volumes: list[float]) -> dict[str, float]:
    """Compute volume statistics (total, average, recent average)."""
    if not volumes:
        return {"total": 0.0, "average": 0.0, "recent_avg": 0.0}
    total = sum(volumes)
    avg = total / len(volumes)
    recent = sum(volumes[-10:]) / min(10, len(volumes))
    return {"total": total, "average": avg, "recent_avg": recent}


def compute_volume_trend(volumes: list[float], short_period: int = 5, long_period: int = 20) -> str:
    """Compare short-term vs long-term volume average. Returns 'increasing', 'decreasing', or 'stable'."""
    if len(volumes) < min(short_period, long_period):
        return "stable"
    short_avg = sum(volumes[-short_period:]) / min(short_period, len(volumes))
    long_avg = sum(volumes[-long_period:]) / min(long_period, len(volumes))
    if long_avg == 0:
        return "stable"
    ratio = short_avg / long_avg
    if ratio > 1.5:
        return "increasing"
    elif ratio < 0.5:
        return "decreasing"
    return "stable"


def all_indicators(closes: list[float], highs: list[float], lows: list[float],
                   volumes: list[float]) -> dict[str, Any]:
    """Compute all indicators and return as a flat dict."""
    result: dict[str, Any] = {}

    # RSI
    rsi = compute_rsi(closes)
    result["rsi"] = rsi[-1] if rsi else 50.0
    rsi_val = result["rsi"]
    if rsi_val > 70:
        result["rsi_trend"] = "overbought"
    elif rsi_val < 30:
        result["rsi_trend"] = "oversold"
    else:
        result["rsi_trend"] = "neutral"

    # MACD
    macd = compute_macd(closes)
    result["macd_line"] = macd["macd"][-1] if macd["macd"] else 0.0
    result["macd_signal"] = macd["signal"][-1] if macd["signal"] else 0.0
    result["macd_histogram"] = macd["histogram"][-1] if macd["histogram"] else 0.0
    macd_line = result["macd_line"]
    macd_signal = result["macd_signal"]
    if macd_line > macd_signal:
        result["macd_cross"] = "above"
    elif macd_line < macd_signal:
        result["macd_cross"] = "below"
    else:
        result["macd_cross"] = "neutral"
    result["macd_direction"] = "bullish" if result["macd_histogram"] > 0 else "bearish"

    # EMA (20, 50, 200)
    for period in [20, 50, 200]:
        vals = compute_ema(closes, period)
        result[f"ema_{period}"] = vals[-1] if vals else None

    # Bollinger Bands
    bb = compute_bollinger_bands(closes)
    result["bb_upper"] = bb["upper"][-1] if bb["upper"] else 0.0
    result["bb_middle"] = bb["middle"][-1] if bb["middle"] else 0.0
    result["bb_lower"] = bb["lower"][-1] if bb["lower"] else 0.0

    # ATR
    atr = compute_atr(highs, lows, closes)
    result["atr"] = atr[-1] if atr else 0.0

    # Volume
    vol_stats = compute_volume_stats(volumes)
    result["volume_total"] = vol_stats["total"]
    result["volume_avg"] = vol_stats["average"]
    result["volume_recent_avg"] = vol_stats["recent_avg"]
    result["volume_trend"] = compute_volume_trend(volumes)

    # Linear regression
    slope, intercept = compute_linear_regression(closes)
    result["regression_slope"] = slope
    result["regression_intercept"] = intercept

    # Swing points
    swings = detect_swing_points(highs, lows)
    result["swing_highs_count"] = len(swings["highs"])
    result["swing_lows_count"] = len(swings["lows"])

    return result
