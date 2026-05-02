# -*- coding: utf-8 -*-
"""VK bot for the school microclimate monitoring stand."""

from __future__ import annotations

import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from sensors_live import SensorReader, format_status


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

VK_TOKEN = os.getenv("VK_TOKEN")

if not VK_TOKEN:
    print("VK_TOKEN is not set. Create .env from .env.example.", file=sys.stderr)
    sys.exit(1)

SENSORS = SensorReader()


HELP_TEXT = (
    "Здравствуйте! Я бот стенда мониторинга микроклимата.\n\n"
    "Доступные команды:\n"
    "статус — получить текущие параметры микроклимата\n"
    "помощь — показать справку"
)


def send_message(vk, user_id: int, text: str) -> None:
    """Sends a VK message."""

    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 2**31 - 1),
    )


def handle_message(text: str) -> str:
    """Returns bot response for a user message."""

    normalized = text.strip().lower()

    if normalized in {"старт", "start", "помощь", "help"}:
        return HELP_TEXT

    if normalized in {"статус", "status", "показания", "датчики"}:
        data = SENSORS.read_all()
        return format_status(data)

    return "Команда не распознана. Напишите 'статус' или 'помощь'."


def main() -> None:
    """Starts the VK bot."""

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("VK bot started")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = handle_message(event.text)
            send_message(vk, event.user_id, response)


if __name__ == "__main__":
    main()
