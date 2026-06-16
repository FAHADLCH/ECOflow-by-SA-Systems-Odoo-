# -*- coding: utf-8 -*-
"""Core deterministic AI/analytics helpers for ECOFLOW.

Everything here is pure Python and explainable. No external services, no
network calls, no heavy ML dependencies — which keeps the module privacy-first
and Odoo-Online compatible. Models are intentionally simple and auditable:

* Holt-style linear trend + additive weekday seasonality for forecasting
* Robust z-score (median / MAD) for anomaly detection
* Exponential fill-level projection for predictive collection

These primitives are consumed by the forecast, bin-prediction and insight
models.
"""
import math
import statistics
from datetime import date, timedelta


def _safe_mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def moving_average(series, window=3):
    """Simple trailing moving average. Returns list aligned to ``series``."""
    out = []
    for i in range(len(series)):
        chunk = series[max(0, i - window + 1): i + 1]
        out.append(_safe_mean(chunk))
    return out


def linear_trend(series):
    """Ordinary least squares slope/intercept over an evenly spaced series.

    Returns ``(slope, intercept)`` where x = 0..n-1. Falls back to a flat line
    when there is insufficient variance.
    """
    n = len(series)
    if n < 2:
        return 0.0, (series[0] if series else 0.0)
    xs = list(range(n))
    mx = _safe_mean(xs)
    my = _safe_mean(series)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return 0.0, my
    slope = sum((xs[i] - mx) * (series[i] - my) for i in range(n)) / denom
    intercept = my - slope * mx
    return slope, intercept


def weekday_seasonality(pairs):
    """Average deviation from the mean per ISO weekday (0=Mon..6=Sun).

    ``pairs`` is an iterable of ``(date, value)``. Returns a dict weekday->delta.
    """
    pairs = list(pairs)
    if not pairs:
        return {}
    base = _safe_mean(v for _, v in pairs)
    buckets = {}
    for d, v in pairs:
        buckets.setdefault(d.weekday(), []).append(v - base)
    return {wd: _safe_mean(vs) for wd, vs in buckets.items()}


def forecast_series(pairs, horizon=7, window=4):
    """Forecast ``horizon`` future daily values from historical ``(date, value)``.

    Combines a smoothed linear trend with weekday seasonality. Returns a list of
    dicts: ``{date, value, lower, upper}`` (95%-ish band from residual spread).
    """
    pairs = sorted(pairs, key=lambda p: p[0])
    if not pairs:
        today = date.today()
        return [
            {"date": today + timedelta(days=i + 1), "value": 0.0,
             "lower": 0.0, "upper": 0.0}
            for i in range(horizon)
        ]

    values = [v for _, v in pairs]
    smoothed = moving_average(values, window=window)
    slope, intercept = linear_trend(smoothed)
    season = weekday_seasonality(pairs)

    # residuals of the in-sample fit, for the uncertainty band
    fitted = [intercept + slope * i for i in range(len(values))]
    residuals = [values[i] - fitted[i] for i in range(len(values))]
    spread = statistics.pstdev(residuals) if len(residuals) > 1 else 0.0

    last_date = pairs[-1][0]
    n = len(values)
    out = []
    for h in range(1, horizon + 1):
        d = last_date + timedelta(days=h)
        trend = intercept + slope * (n - 1 + h)
        seasonal = season.get(d.weekday(), 0.0)
        point = max(trend + seasonal, 0.0)
        out.append({
            "date": d,
            "value": round(point, 2),
            "lower": round(max(point - 1.96 * spread, 0.0), 2),
            "upper": round(point + 1.96 * spread, 2),
        })
    return out


def robust_zscores(values):
    """Return robust z-scores using median and MAD (outlier-resistant)."""
    values = list(values)
    if len(values) < 3:
        return [0.0] * len(values)
    med = statistics.median(values)
    deviations = [abs(v - med) for v in values]
    mad = statistics.median(deviations) or 1e-9
    # 1.4826 scales MAD to be consistent with the std-dev of a normal dist
    return [(v - med) / (1.4826 * mad) for v in values]


def project_fill_level(current_pct, daily_gain_pct, days):
    """Project a bin's fill percentage ``days`` ahead given a daily gain."""
    return min(current_pct + daily_gain_pct * days, 130.0)


def days_until_full(current_pct, daily_gain_pct, threshold=90.0):
    """Estimate whole days until a bin crosses ``threshold`` fill percentage."""
    if daily_gain_pct <= 0:
        return 999
    if current_pct >= threshold:
        return 0
    return int(math.ceil((threshold - current_pct) / daily_gain_pct))


def trend_label(slope):
    """Human label for a slope value."""
    if slope > 0.5:
        return "rising"
    if slope < -0.5:
        return "falling"
    return "stable"
