#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo ./scripts/start_frontend.sh" >&2
  exit 1
fi

if ! command -v nginx >/dev/null; then
  echo "Host nginx is not installed. Install it with: sudo apt-get install nginx" >&2
  exit 1
fi

if [[ ! -f "$project_root/frontend/dist/index.html" ]]; then
  echo "Frontend build missing. Build frontend/dist first." >&2
  exit 1
fi

# The www-data worker cannot read files beneath /root.
install -d -m 755 /var/www/paperignition
cp -a "$project_root/frontend/dist/." /var/www/paperignition/
chmod -R a+rX /var/www/paperignition

config="$project_root/deploy/nginx.host.conf"
nginx -t -c "$config"

pid_file=/run/paperignition-nginx.pid
if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
  nginx -s reload -c "$config"
else
  nginx -c "$config"
fi

for attempt in {1..20}; do
  if curl --fail --silent http://127.0.0.1/ >/dev/null; then
    echo "Frontend ready: http://127.0.0.1/"
    exit 0
  fi
  sleep 1
done
echo "Frontend nginx started, but its health check failed." >&2
exit 1
