# -*- coding: utf-8 -*-
"""
Module for reading microclimate sensor values.

This file contains a safe demonstration implementation. In the real stand,
this module can be adapted for the specific connected sensors and interface.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from random import uniform
from typing import Dict, Any


@dataclass
class SensorData:
    """Current microclimate sensor values."""

    temperature_c: float
    humidity_percent: float
    timestamp: str


class SensorReader:
    """Reads data from microclimate sensors.

    The current implementation returns demonstration values. Replace the body
    of read_all() with real sensor reading logic for production hardware.
    """

    def read_all(self) -> Dict[str, Any]:
        data = SensorData(
            temperature_c=round(uniform(21.0, 25.0), 1),
            humidity_percent=round(uniform(35.0, 55.0), 1),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return asdict(data)


def format_status(data: Dict[str, Any]) -> str:
    """Formats sensor values for bot messages."""

    temperature = data.get("temperature_c", "нет данных")
    humidity = data.get("humidity_percent", "нет данных")
    timestamp = data.get("timestamp", "нет данных")

    return (
        "Текущие параметры микроклимата:\n"
        f"🌡 Температура: {temperature} °C\n"
        f"💧 Влажность: {humidity} %\n"
        f"🕒 Время измерения: {timestamp}"
    )
