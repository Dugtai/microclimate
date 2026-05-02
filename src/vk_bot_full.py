# -*- coding: utf-8 -*-
"""Extended VK bot for the microclimate monitoring stand."""

from __future__ import annotations

import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from microclimate_core import MicroclimateReader, format_full_status, format_single


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

VK_TOKEN = os.getenv("VK_TOKEN")
if not VK_TOKEN:
    print("VK_TOKEN is not set. Create .env from .env.example.", file=sys.stderr)
    sys.exit(1)

READER = MicroclimateReader()

HELP_TEXT = (
    "Команды VK-бота:\n"
    "/start — включить справку\n"
    "/status — все параметры\n"
    "/temperature — температура\n"
    "/humidity — влажность\n"
    "/light — освещённость\n"
    "/air — качество воздуха\n"
    "/pressure — давление\n"
    "/noise — уровень шума\n"
    "/id — показать peer_id\n"
    "/help — справка"
)


def send_message(vk, peer_id: int, text: str) -> None:
    vk.messages.send(
        peer_id=peer_id,
        message=text,
        random_id=random.randint(1, 2**31 - 1),
    )


def handle_message(text: str, peer_id: int) -> str:
    normalized = text.strip().lower()
    data = READER.read_all()

    if normalized in {"/start", "start", "старт", "/help", "help", "помощь"}:
        return HELP_TEXT
    if normalized in {"/status", "status", "статус", "показания", "датчики"}:
        return format_full_status(data)
    if normalized in {"/temperature", "temperature", "температура"}:
        return format_single(data, "temperature_c")
    if normalized in {"/humidity", "humidity", "влажность"}:
        return format_single(data, "humidity_percent")
    if normalized in {"/light", "light", "свет", "освещенность", "освещённость"}:
        return format_single(data, "light_lux")
    if normalized in {"/air", "air", "воздух"}:
        return format_single(data, "air_quality")
    if normalized in {"/pressure", "pressure", "давление"}:
        return format_single(data, "pressure_hpa")
    if normalized in {"/noise", "noise", "шум"}:
        return format_single(data, "noise_level")
    if normalized in {"/id", "id"}:
        return f"peer_id: {peer_id}"

    return "Команда не распознана. Напишите /help."


def main() -> None:
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("Extended VK bot started")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = handle_message(event.text, event.peer_id)
            send_message(vk, event.peer_id, response)


if __name__ == "__main__":
    main()
