#!/bin/sh
set -eux

# Install curl
apk add --no-cache curl

# Wait for Keycloak to be live
KC_BASE_URL=${KC_BASE_URL:-http://keycloak:8080}
KC_HEALTHCHECK_PATH=${KC_HEALTHCHECK_PATH:-/health/ready}
KC_HEALTHCHECK_INTERVAL=${KC_HEALTHCHECK_INTERVAL:-5}

until curl --head -fsS "$KC_BASE_URL$KC_HEALTHCHECK_PATH" > /dev/null; do
  sleep "$KC_HEALTHCHECK_INTERVAL"
done

# Check if custom command is provided, otherwise run default action (create one realm and one client)
if [ -n "$(printf '%s\n' "$@")" ]; then
  exec /usr/local/bin/python /app/project/main.py "$@"
else
  exec /usr/local/bin/python /app/project/main.py --kc-server-url "$KC_BASE_URL" --no-verify run "$KEYCLOAK_ADMIN" "$KEYCLOAK_ADMIN_PASSWORD"
fi
