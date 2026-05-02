# -*- coding: utf-8 -*-
"""Conditional threshold values for microclimate monitoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RangeThreshold:
    """Recommended range for a measured parameter."""

    min_value: Optional[float]
    max_value: Optional[float]
    unit: str
    title: str


THRESHOLDS = {
    "temperature_c": RangeThreshold(20.0, 24.0, "°C", "Температура"),
    "humidity_percent": RangeThreshold(30.0, 60.0, "%", "Влажность"),
    "light_lux": RangeThreshold(200.0, 500.0, "лк", "Освещённость"),
    "air_quality": RangeThreshold(0.0, 0.6, "усл.", "Качество воздуха"),
    "pressure_hpa": RangeThreshold(None, None, "гПа", "Давление"),
    "noise_level": RangeThreshold(0.0, 60.0, "усл.", "Уровень шума"),
}


def check_value(key: str, value: float) -> str:
    """Returns status marker for a value: ok, low, high or unknown."""

    threshold = THRESHOLDS.get(key)
    if threshold is None:
        return "unknown"

    if threshold.min_value is not None and value < threshold.min_value:
        return "low"

    if threshold.max_value is not None and value > threshold.max_value:
        return "high"

    return "ok"


def get_recommendation(key: str, status: str) -> str | None:
    """Returns a human-readable recommendation for a threshold violation."""

    if status == "ok":
        return None

    recommendations = {
        ("temperature_c", "high"): "🥵 Температура высокая — рекомендуется проветривание или снижение нагрева.",
        ("temperature_c", "low"): "🥶 Температура низкая — проверьте отопление и закрытие окон.",
        ("humidity_percent", "low"): "💧 Влажность низкая — воздух пересушен, рекомендуется увлажнение.",
        ("humidity_percent", "high"): "💧 Влажность высокая — рекомендуется проветривание.",
        ("light_lux", "low"): "💡 Недостаточная освещённость — включите освещение или проверьте лампы.",
        ("light_lux", "high"): "💡 Освещённость выше ориентира — возможен избыток света или засветка датчика.",
        ("air_quality", "high"): "🌫 Плохое качество воздуха — необходимо проветривание.",
        ("noise_level", "high"): "🔊 Повышенный уровень шума — рекомендуется снизить акустическую нагрузку.",
    }

    return recommendations.get((key, status))
