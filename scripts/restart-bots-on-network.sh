#!/usr/bin/env bash
set -euo pipefail

# Restarts bot services after the network becomes available.
# Intended for NetworkManager dispatcher or manual execution.

PING_HOST="${PING_HOST:-8.8.8.8}"
SERVICES=(
  "microclimate-telegram-bot.service"
  "microclimate-vk-bot.service"
)

for i in {1..30}; do
  if ping -c 1 -W 2 "$PING_HOST" >/dev/null 2>&1; then
    echo "Network is available"
    for service in "${SERVICES[@]}"; do
      if systemctl list-unit-files "$service" >/dev/null 2>&1; then
        echo "Restarting $service"
        systemctl restart "$service" || true
      fi
    done
    exit 0
  fi
  sleep 2
done

echo "Network is not available after timeout"
exit 1
