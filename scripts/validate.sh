#!/bin/bash
set -e
echo "Validating deployment..."
curl -sf http://localhost/health || exit 1
echo "Validation passed!"
