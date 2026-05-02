# -*- coding: utf-8 -*-
"""Console monitor for local stand debugging and demonstration."""

from __future__ import annotations

import os
import time

from microclimate_core import MicroclimateReader, format_full_status


INTERVAL_SECONDS = int(os.getenv("MONITOR_INTERVAL_SECONDS", "5"))


def clear_screen() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def main() -> None:
    reader = MicroclimateReader()

    while True:
        clear_screen()
        data = reader.read_all()
        print(format_full_status(data))
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
