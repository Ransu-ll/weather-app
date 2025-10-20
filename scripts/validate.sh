#!/usr/bin/env bash
set -e

echo "---- [ValidateService] Checking health ----"
curl -fsS http://localhost:8000/ >/dev/null
echo "Health check OK"
