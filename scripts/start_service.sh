#!/usr/bin/env bash
set -e
cd /srv/weatherapp
source venv/bin/activate

# stop any existing process
pkill -f wsgi_dev.py || true

# start new process in background
nohup python webapp/wsgi_dev.py > /var/log/weatherapp.log 2>&1 &
