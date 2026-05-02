# -*- coding: utf-8 -*-
"""LCD/display monitor placeholder for the microclimate stand.

The real stand may use an I2C LCD display. This public version keeps the logic
safe and portable: it prints rotating values to stdout. Hardware-specific LCD
code can be added in the render_to_lcd() function.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict

from microclimate_core import MicroclimateReader, format_single


INTERVAL_SECONDS = int(os.getenv("DISPLAY_INTERVAL_SECONDS", "3"))
DISPLAY_KEYS = [
    "temperature_c",
    "humidity_percent",
    "light_lux",
    "air_quality",
    "pressure_hpa",
    "noise_level",
]


def render_to_lcd(line1: str, line2: str = "") -> None:
    """Renders text to LCD.

    Replace this function with a real LCD driver call on the hardware stand.
    """

    print("=" * 32)
    print(line1[:32])
    if line2:
        print(line2[:32])


def main() -> None:
    reader = MicroclimateReader()

    while True:
        data: Dict[str, Any] = reader.read_all()
        for key in DISPLAY_KEYS:
            render_to_lcd("Микроклимат", format_single(data, key))
            time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
