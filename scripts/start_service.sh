#!/usr/bin/env bash
set -e

echo "---- [ApplicationStart] Starting service ----"

# Start weatherapp service
systemctl enable weatherapp
systemctl start weatherapp

# Wait and verify service
sleep 3

echo "Checking service status..."
if systemctl is-active --quiet weatherapp; then
    echo "✓ weatherapp service started successfully"
else
    echo "✗ weatherapp service failed to start"
    journalctl -u weatherapp --no-pager -n 20
    exit 1
fi

echo "Service started successfully"