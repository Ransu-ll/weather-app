#!/usr/bin/env bash
set -e

echo "---- [AfterInstall] Installing Python and deps ----"

PY=python3.9  # keep in sync with your pipeline/runtime

# Install Python if needed
if ! command -v $PY >/dev/null 2>&1; then
  if command -v dnf >/dev/null 2>&1; then
    dnf install -y python3.9 python3.9-devel
  elif command -v yum >/dev/null 2>&1; then
    yum install -y python39 python39-devel
  elif command -v apt-get >/dev/null 2>&1; then
    apt-get update && apt-get install -y python3.9 python3.9-venv python3.9-dev
  fi
fi

# Create venv + install deps
$PY -m venv /srv/weatherapp/venv
source /srv/weatherapp/venv/bin/activate
pip install --upgrade pip
pip install -r /srv/weatherapp/webapp/requirements.txt

# Systemd service (Waitress runs wsgi_dev.py)
echo "---- [AfterInstall] Writing systemd unit ----"
cat >/etc/systemd/system/weatherapp.service <<'EOF'
[Unit]
Description=Waitress WeatherApp (Flask)
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/srv/weatherapp
Environment="PATH=/srv/weatherapp/venv/bin"
ExecStart=/srv/weatherapp/venv/bin/python /srv/weatherapp/wsgi_dev.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

# Ensure ownership so service user can read/write
chown -R ec2-user:ec2-user /srv/weatherapp
