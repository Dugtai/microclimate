#!/usr/bin/env bash
set -euo pipefail

# Connect to a known Wi-Fi network using NetworkManager.
# Usage:
#   sudo WIFI_SSID="network_name" WIFI_PASSWORD="network_password" ./wifi-connect.sh
# For an open network, leave WIFI_PASSWORD empty.

WIFI_SSID="${WIFI_SSID:-}"
WIFI_PASSWORD="${WIFI_PASSWORD:-}"
INTERFACE="${WIFI_INTERFACE:-wlan0}"

if [[ -z "$WIFI_SSID" ]]; then
  echo "WIFI_SSID is not set"
  exit 1
fi

if ! command -v nmcli >/dev/null 2>&1; then
  echo "nmcli not found. Install NetworkManager or adapt this script for wpa_supplicant."
  exit 1
fi

nmcli radio wifi on

if [[ -z "$WIFI_PASSWORD" ]]; then
  nmcli dev wifi connect "$WIFI_SSID" ifname "$INTERFACE"
else
  nmcli dev wifi connect "$WIFI_SSID" password "$WIFI_PASSWORD" ifname "$INTERFACE"
fi

echo "Wi-Fi connection command sent for SSID: $WIFI_SSID"
