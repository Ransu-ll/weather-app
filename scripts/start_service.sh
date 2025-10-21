#!/bin/bash
set -e
echo "Starting weatherapp service..."
cat >/etc/systemd/system/weatherapp.service <<EOF
[Unit]
Description=Weather Flask App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/srv/weatherapp/webapp
ExecStart=/usr/local/bin/waitress-serve --host=0.0.0.0 --port=8000 wsgi_dev:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable weatherapp
systemctl restart weatherapp
sleep 2
systemctl status weatherapp --no-pager
