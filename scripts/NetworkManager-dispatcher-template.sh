#!/usr/bin/env bash
set -euo pipefail

# NetworkManager dispatcher template.
# Copy this file to a local dispatcher directory and adapt paths on the stand.
# This public template intentionally does not contain real SSID, tokens or host data.

INTERFACE="$1"
STATUS="$2"
PROJECT_DIR="/home/root/microclimate"
LOG_FILE="$PROJECT_DIR/logs/network-dispatcher.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date '+%Y-%m-%d %H:%M:%S') interface=$INTERFACE status=$STATUS" >> "$LOG_FILE"

case "$STATUS" in
  up|connectivity-change)
    echo "$(date '+%Y-%m-%d %H:%M:%S') network available, restart script can be called here" >> "$LOG_FILE"
    # Example for local stand:
    # /usr/bin/env bash "$PROJECT_DIR/scripts/restart-bots-on-network.sh" >> "$LOG_FILE" 2>&1
    ;;
  down)
    echo "$(date '+%Y-%m-%d %H:%M:%S') network down" >> "$LOG_FILE"
    ;;
esac
