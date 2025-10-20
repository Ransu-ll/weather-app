#!/usr/bin/env bash
set -e

echo "---- [AfterInstall] Installing Python and deps ----"

PY=python3.9

# Amazon Linux 2023 uses dnf
if ! command -v $PY >/dev/null 2>&1; then
    echo "Installing Python 3.9..."
    dnf install -y python3.9 python3.9-pip
fi

# Create venv + install deps
echo "Setting up virtual environment..."
$PY -m venv /srv/weatherapp/venv
source /srv/weatherapp/venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip

# Install from webapp/requirements.txt
if [ -f "/srv/weatherapp/webapp/requirements.txt" ]; then
    echo "Installing from webapp/requirements.txt..."
    pip install -r /srv/weatherapp/webapp/requirements.txt
elif [ -f "/srv/weatherapp/requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    pip install -r /srv/weatherapp/requirements.txt
else
    echo "No requirements.txt found, installing default packages..."
    pip install flask waitress jinja2 requests
fi

# Systemd service - updated for webapp/ path
echo "---- [AfterInstall] Writing systemd unit ----"
cat >/etc/systemd/system/weatherapp.service <<'EOF'
[Unit]
Description=Waitress WeatherApp (Flask)
After=network.target

[Service]
Type=simple
User=ec2-user
Group=ec2-user
WorkingDirectory=/srv/weatherapp/webapp
Environment="PATH=/srv/weatherapp/venv/bin"
ExecStart=/srv/weatherapp/venv/bin/waitress-serve --host=0.0.0.0 --port=5000 wsgi_dev:app
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

# Ensure ownership
chown -R ec2-user:ec2-user /srv/weatherapp

echo "Dependencies installed successfully"