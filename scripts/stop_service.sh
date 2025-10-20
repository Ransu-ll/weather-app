#!/usr/bin/env bash
set -e
echo "---- [ApplicationStop] Stopping service ----"

# Stop via systemd first
systemctl stop weatherapp 2>/dev/null || true

# Kill any remaining processes (updated path)
pkill -f "waitress-serve" 2>/dev/null || true
pkill -f "webapp/wsgi_dev.py" 2>/dev/null || true

echo "Services stopped"
