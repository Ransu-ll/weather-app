#!/bin/bash
set -e
echo "BeforeInstall: stopping any running service..."
systemctl stop weatherapp || true
mkdir -p /srv/weatherapp
find /srv/weatherapp -mindepth 1 -delete

