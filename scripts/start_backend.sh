#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo ./scripts/start_backend.sh" >&2
  exit 1
fi

if ! docker inspect pi-verify-db --format '{{.State.Running}}' 2>/dev/null | grep -qx true; then
  echo "Database container pi-verify-db is not running. Start it first." >&2
  exit 1
fi

if curl --fail --silent http://127.0.0.1:8000/api/health >/dev/null; then
  echo "Backend is already responding on port 8000; no new process started."
  exit 0
fi

if ss -ltn '( sport = :8000 )' | grep -q 'LISTEN'; then
  echo "Port 8000 is occupied, but the backend health check failed." >&2
  exit 1
fi

systemctl start paperignition-backend.service
for attempt in {1..20}; do
  if curl --fail --silent http://127.0.0.1:8000/api/health >/dev/null; then
    echo "Backend ready: http://127.0.0.1:8000/api/health"
    exit 0
  fi
  sleep 1
done
echo "Backend service started, but its health check failed." >&2
exit 1
