#!/bin/bash
set -e
echo "BeforeInstall: Stopping any running service..."
systemctl stop weatherapp || true
rm -rf /srv/weatherapp
mkdir -p /srv/weatherapp
