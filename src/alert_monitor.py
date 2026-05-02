# -*- coding: utf-8 -*-
"""Microclimate deviation monitor.

The script confirms deviations several times in a row before printing an alert.
It can be used as a base for Telegram/VK notification delivery.
"""

from __future__ import annotations

import os
import time
from collections import defaultdict
from typing import DefaultDict

from microclimate_core import MicroclimateReader, analyze, collect_recommendations, format_full_status


INTERVAL_SECONDS = int(os.getenv("ALERT_INTERVAL_SECONDS", "10"))
CONFIRM_COUNT = int(os.getenv("ALERT_CONFIRM_COUNT", "2"))


def main() -> None:
    reader = MicroclimateReader()
    counters: DefaultDict[str, int] = defaultdict(int)

    print("Alert monitor started")

    while True:
        data = reader.read_all()
        statuses = analyze(data)

        has_confirmed_alert = False
        for key, status in statuses.items():
            if status in {"low", "high"}:
                counters[key] += 1
            else:
                counters[key] = 0

            if counters[key] >= CONFIRM_COUNT:
                has_confirmed_alert = True

        if has_confirmed_alert:
            recommendations = collect_recommendations(data)
            if recommendations:
                print("\n🚨 Обнаружено отклонение микроклимата")
                print(format_full_status(data))
                print("-" * 60)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
