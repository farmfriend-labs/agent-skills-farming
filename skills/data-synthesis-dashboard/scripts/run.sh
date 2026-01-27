#!/bin/bash
# run.sh - Start data synthesis dashboard

set -e

# Load environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ -f "$PROJECT_ROOT/.env" ]]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

DASHBOARD_PORT="${DASHBOARD_PORT:-5000}"

echo "Starting Data Synthesis Dashboard on port $DASHBOARD_PORT..."
python3 "$SCRIPT_DIR/dashboard.py" --port "$DASHBOARD_PORT"
