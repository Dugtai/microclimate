# -*- coding: utf-8 -*-
"""Core logic for reading, checking and formatting microclimate values."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from random import uniform
from typing import Any, Dict, List

from thresholds import THRESHOLDS, check_value, get_recommendation


@dataclass
class MicroclimateData:
    """Single microclimate measurement snapshot."""

    temperature_c: float
    humidity_percent: float
    light_lux: int
    air_quality: float
    pressure_hpa: float
    noise_level: float
    timestamp: str


class MicroclimateReader:
    """Reads values from sensors.

    The public repository contains a demonstration reader. On the real stand,
    replace the demo values with BME280, BH1750, MQ-135, MAX4466 and ADS1115
    reads.
    """

    def read_all(self) -> Dict[str, Any]:
        data = MicroclimateData(
            temperature_c=round(uniform(21.0, 27.8), 2),
            humidity_percent=round(uniform(35.0, 55.0), 1),
            light_lux=int(uniform(80, 520)),
            air_quality=round(uniform(0.35, 0.95), 3),
            pressure_hpa=round(uniform(995.0, 1015.0), 2),
            noise_level=round(uniform(20.0, 70.0), 1),
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        )
        return asdict(data)


def analyze(data: Dict[str, Any]) -> Dict[str, str]:
    """Checks all known values against thresholds."""

    result: Dict[str, str] = {}
    for key in THRESHOLDS:
        value = data.get(key)
        if isinstance(value, (int, float)):
            result[key] = check_value(key, float(value))
    return result


def collect_recommendations(data: Dict[str, Any]) -> List[str]:
    """Builds recommendations list based on threshold checks."""

    statuses = analyze(data)
    recommendations: List[str] = []

    for key, status in statuses.items():
        recommendation = get_recommendation(key, status)
        if recommendation:
            recommendations.append(recommendation)

    return recommendations


def _marker(status: str) -> str:
    if status == "ok":
        return "✅"
    if status in {"low", "high"}:
        return "⚠️"
    return "◻️"


def format_full_status(data: Dict[str, Any]) -> str:
    """Formats the full status message for Telegram/VK."""

    statuses = analyze(data)
    recommendations = collect_recommendations(data)
    recommendations_text = "\n".join(recommendations) if recommendations else "✅ Параметры находятся в допустимых пределах."

    return (
        "📊 Микроклимат кабинета\n"
        f"🕘 {data.get('timestamp', 'нет данных')}\n\n"
        f"{_marker(statuses.get('temperature_c', 'unknown'))} Температура: {data.get('temperature_c', 'нет данных')} °C "
        "(ориентир 20.0–24.0 °C)\n"
        f"{_marker(statuses.get('humidity_percent', 'unknown'))} Влажность: {data.get('humidity_percent', 'нет данных')} % "
        "(ориентир 30.0–60.0 %)\n"
        f"{_marker(statuses.get('light_lux', 'unknown'))} Освещённость: {data.get('light_lux', 'нет данных')} лк "
        "(ориентир 200–500 лк)\n"
        f"{_marker(statuses.get('air_quality', 'unknown'))} Качество воздуха: {data.get('air_quality', 'нет данных')} усл. "
        "(ориентир 0.0–0.6)\n"
        f"📈 Давление: {data.get('pressure_hpa', 'нет данных')} гПа\n"
        f"{_marker(statuses.get('noise_level', 'unknown'))} Уровень шума: {data.get('noise_level', 'нет данных')} усл.\n\n"
        "Учебный проект. Данные в реальном времени.\n\n"
        f"📌 Рекомендации:\n{recommendations_text}"
    )


def format_single(data: Dict[str, Any], key: str) -> str:
    """Formats one parameter by key."""

    labels = {
        "temperature_c": ("🌡 Температура", "°C"),
        "humidity_percent": ("💧 Влажность", "%"),
        "light_lux": ("💡 Освещённость", "лк"),
        "air_quality": ("🌫 Качество воздуха", "усл."),
        "pressure_hpa": ("📈 Давление", "гПа"),
        "noise_level": ("🔊 Уровень шума", "усл."),
    }

    title, unit = labels.get(key, (key, ""))
    return f"{title}: {data.get(key, 'нет данных')} {unit}".strip()
