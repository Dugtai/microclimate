#!/usr/bin/env bash
set -euo pipefail

echo "=== Microclimate stand diagnostics ==="

echo
uname -a || true

echo
python3 --version || true

echo
ip address show || true

echo
echo "Network check:"
ping -c 2 8.8.8.8 || true

echo
echo "Project services:"
systemctl status microclimate-telegram-bot.service --no-pager || true
systemctl status microclimate-vk-bot.service --no-pager || true
systemctl status microclimate-telegram-bot-full.service --no-pager || true
systemctl status microclimate-vk-bot-full.service --no-pager || true
systemctl status microclimate-console-monitor.service --no-pager || true
systemctl status microclimate-data-logger.service --no-pager || true
systemctl status microclimate-alert-monitor.service --no-pager || true

echo
echo "Recent logs:"
journalctl -u microclimate-telegram-bot-full.service -n 30 --no-pager || true
journalctl -u microclimate-vk-bot-full.service -n 30 --no-pager || true

echo
echo "Diagnostics complete."
