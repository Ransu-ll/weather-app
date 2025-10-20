#!/usr/bin/env bash
set -e
if systemctl is-active --quiet weatherapp; then
  systemctl stop weatherapp
fi
