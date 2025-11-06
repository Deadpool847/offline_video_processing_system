#!/bin/bash
# Run demo to test stylizers

set -e

echo "==========================================" 
echo "Running Demo..."
echo "=========================================="
echo ""

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd):$PYTHONPATH"

python3 scripts/demo.py

echo ""
echo "Demo complete! Check /app/outputs/demo/"