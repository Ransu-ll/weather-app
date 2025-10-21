#!/bin/bash
set -e
echo "Validating deployment..."
curl -sf http://localhost:8000/health || exit 1
echo "Validation passed!"
