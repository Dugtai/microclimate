#!/usr/bin/env bash
set -euo pipefail

# Template for Wi-Fi autoconnect priorities.
# Public version does not contain real SSID values.
# Run on the stand after replacing connection names.

SCHOOL_WIFI="${SCHOOL_WIFI:-school_wifi_connection_name}"
HOME_WIFI="${HOME_WIFI:-home_wifi_connection_name}"
HOTSPOT_WIFI="${HOTSPOT_WIFI:-microclimate_hotspot_connection_name}"

if ! command -v nmcli >/dev/null 2>&1; then
  echo "nmcli not found"
  exit 1
fi

echo "Available NetworkManager connections:"
nmcli connection show

echo

echo "Setting Wi-Fi priorities..."

# Higher value means higher priority.
nmcli connection modify "$SCHOOL_WIFI" connection.autoconnect yes connection.autoconnect-priority 100 || true
nmcli connection modify "$HOME_WIFI" connection.autoconnect yes connection.autoconnect-priority 50 || true

# Hotspot should not be automatically raised if known Wi-Fi networks are absent.
nmcli connection modify "$HOTSPOT_WIFI" connection.autoconnect no connection.autoconnect-priority -100 || true

echo "Done. Current priorities:"
nmcli -f NAME,AUTOCONNECT,AUTOCONNECT-PRIORITY connection show
