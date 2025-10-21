#!/bin/bash
set -e
echo "Stopping weatherapp service..."
systemctl stop weatherapp 2>/dev/null || true
pkill -f "waitress-serve" 2>/dev/null || true
pkill -f "webapp/wsgi_dev.py" 2>/dev/null || true
echo "Service stopped"
