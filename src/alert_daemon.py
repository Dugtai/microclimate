# -*- coding: utf-8 -*-
"""Alert daemon for the microclimate monitoring stand.

The daemon periodically reads sensor values, compares them with thresholds and
prints alerts to stdout. In the real stand this script can be extended to send
messages to Telegram or VK after adding recipient IDs to the local .env file.
"""

from __future__ import annotations

import os
import time

from microclimate_core import MicroclimateReader, collect_recommendations, format_full_status


CHECK_INTERVAL_SECONDS = int(os.getenv("ALERT_CHECK_INTERVAL_SECONDS", "30"))
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))


def main() -> None:
    reader = MicroclimateReader()
    last_alert_time = 0.0

    print("Microclimate alert daemon started")

    while True:
        data = reader.read_all()
        recommendations = collect_recommendations(data)
        now = time.time()

        if recommendations and now - last_alert_time >= ALERT_COOLDOWN_SECONDS:
            print("ALERT:")
            print(format_full_status(data))
            last_alert_time = now

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
