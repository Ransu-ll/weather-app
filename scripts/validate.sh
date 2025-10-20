#!/usr/bin/env bash
set -e

echo "---- [ValidateService] Checking health ----"

# Wait for app to start
sleep 5

# Check if service is running
if ! systemctl is-active --quiet weatherapp; then
    echo "✗ weatherapp service is not running"
    exit 1
fi

# Try health endpoint
echo "Testing application endpoints..."
MAX_RETRIES=3
RETRY_COUNT=0

until [ $RETRY_COUNT -ge $MAX_RETRIES ]
do
    if curl -fsS http://localhost:5000/health >/dev/null 2>&1; then
        echo "✓ Health check passed on port 5000"
        break
    elif curl -fsS http://localhost:5000/ >/dev/null 2>&1; then
        echo "✓ Root endpoint responding on port 5000"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT+1))
        echo "Attempt $RETRY_COUNT failed, retrying in 3 seconds..."
        sleep 3
    fi
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "✗ Application not responding after $MAX_RETRIES attempts"
    
    # Debug information
    echo "Service status:"
    systemctl status weatherapp --no-pager
    
    echo "Recent logs:"
    journalctl -u weatherapp --no-pager -n 20
    
    exit 1
fi

echo "Health check OK"