#!/bin/bash
set -euo pipefail

# Health check script for NIDS

echo "Checking backend health..."
curl -sSf http://localhost:8000/api/v1/system/health || { echo "Backend is down!"; exit 1; }

echo "Checking frontend health..."
curl -sSf http://localhost:3000/ > /dev/null || { echo "Frontend is down!"; exit 1; }

echo "All systems healthy!"
