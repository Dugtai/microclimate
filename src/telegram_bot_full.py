# -*- coding: utf-8 -*-
"""Extended Telegram bot for the microclimate monitoring stand."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from microclimate_core import MicroclimateReader, format_full_status, format_single


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not set. Create .env from .env.example.", file=sys.stderr)
    sys.exit(1)

READER = MicroclimateReader()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📊 Микроклимат кабинета\n\n"
        "Команды:\n"
        "/status — все параметры\n"
        "/temperature — температура\n"
        "/humidity — влажность\n"
        "/light — освещённость\n"
        "/air — качество воздуха\n"
        "/pressure — давление\n"
        "/noise — уровень шума\n"
        "/help — справка"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = READER.read_all()
    await update.message.reply_text(format_full_status(data))


async def temperature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "temperature_c"))


async def humidity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "humidity_percent"))


async def light(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "light_lux"))


async def air(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "air_quality"))


async def pressure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "pressure_hpa"))


async def noise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_single(READER.read_all(), "noise_level"))


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("temperature", temperature))
    app.add_handler(CommandHandler("humidity", humidity))
    app.add_handler(CommandHandler("light", light))
    app.add_handler(CommandHandler("air", air))
    app.add_handler(CommandHandler("pressure", pressure))
    app.add_handler(CommandHandler("noise", noise))

    print("Extended Telegram bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
