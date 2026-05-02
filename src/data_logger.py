# -*- coding: utf-8 -*-
"""CSV logger for microclimate measurements."""

from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Any, Dict

from microclimate_core import MicroclimateReader, analyze


DEFAULT_LOG_PATH = Path(os.getenv("MICROCLIMATE_CSV_LOG", "data/microclimate.csv"))
INTERVAL_SECONDS = int(os.getenv("LOGGER_INTERVAL_SECONDS", "10"))

FIELDNAMES = [
    "timestamp",
    "temperature_c",
    "humidity_percent",
    "light_lux",
    "air_quality",
    "pressure_hpa",
    "noise_level",
    "temperature_status",
    "humidity_status",
    "light_status",
    "air_status",
    "noise_status",
]

STATUS_FIELD_MAP = {
    "temperature_c": "temperature_status",
    "humidity_percent": "humidity_status",
    "light_lux": "light_status",
    "air_quality": "air_status",
    "noise_level": "noise_status",
}


def ensure_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def build_row(data: Dict[str, Any]) -> Dict[str, Any]:
    row = {key: data.get(key, "") for key in FIELDNAMES}
    statuses = analyze(data)

    for data_key, status_key in STATUS_FIELD_MAP.items():
        row[status_key] = statuses.get(data_key, "unknown")

    return row


def append_row(path: Path, row: Dict[str, Any]) -> None:
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(row)


def main() -> None:
    reader = MicroclimateReader()
    ensure_csv(DEFAULT_LOG_PATH)
    print(f"Logging microclimate data to {DEFAULT_LOG_PATH}")

    while True:
        data = reader.read_all()
        row = build_row(data)
        append_row(DEFAULT_LOG_PATH, row)
        print(row)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
