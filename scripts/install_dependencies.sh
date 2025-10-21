#!/bin/bash
set -e
echo "Installing dependencies..."
dnf -y install python3-pip
pip3 install --upgrade pip
pip3 install -r /srv/weatherapp/webapp/requirements.txt
