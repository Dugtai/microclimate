# -*- coding: utf-8 -*-
"""Telegram bot for the school microclimate monitoring stand."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from sensors_live import SensorReader, format_status


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN is not set. Create .env from .env.example.", file=sys.stderr)
    sys.exit(1)

SENSORS = SensorReader()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a short help message."""

    await update.message.reply_text(
        "Здравствуйте! Я бот стенда мониторинга микроклимата.\n\n"
        "Команды:\n"
        "/status — текущие показания\n"
        "/help — справка"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends command list."""

    await update.message.reply_text(
        "Доступные команды:\n"
        "/status — получить текущие параметры микроклимата\n"
        "/help — показать справку"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends current microclimate sensor values."""

    data = SENSORS.read_all()
    await update.message.reply_text(format_status(data))


def main() -> None:
    """Starts the Telegram bot."""

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))

    print("Telegram bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
