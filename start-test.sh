#!/usr/bin/env bash
#
# Boot a local ECOFLOW by SA Systems instance (Odoo + Postgres) via Docker.
#
# Open in your browser when ready:
#     http://localhost:8070
#
# Default login (set on first run):
#     Email:    admin
#     Password: admin
#
# Override the Odoo series:  ODOO_TAG=19 ./start-test.sh up   (supported: 18, 19)
#
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker Desktop first: https://docs.docker.com/get-docker/"
  exit 1
fi

COMPOSE="docker compose"
if ! docker compose version >/dev/null 2>&1; then
  COMPOSE="docker-compose"
fi

TAG="${ODOO_TAG:-18}"
DB="${DB:-ecoflow}"
MODULES="ecoflow"

export ODOO_TAG="$TAG"

case "${1:-up}" in
  init)
    echo "Creating DB '$DB' and installing ECOFLOW on Odoo $TAG..."
    $COMPOSE run --rm odoo odoo --config=/etc/odoo/odoo.conf \
      -d "$DB" -i "$MODULES" --stop-after-init
    echo "Initialized. Now run: ./start-test.sh up"
    ;;
  up)
    echo "Starting ECOFLOW (Odoo $TAG) + Postgres..."
    $COMPOSE up -d
    echo
    echo "Open: http://localhost:8070    Login: admin / admin"
    echo "Tail logs with: ./start-test.sh logs"
    ;;
  logs)
    $COMPOSE logs -f odoo
    ;;
  stop)
    $COMPOSE stop
    ;;
  restart)
    $COMPOSE restart odoo
    ;;
  update)
    $COMPOSE run --rm odoo odoo --config=/etc/odoo/odoo.conf \
      -d "$DB" -u "$MODULES" --stop-after-init
    $COMPOSE restart odoo
    ;;
  reset)
    echo "WARNING: this deletes the database and uploaded files."
    read -r -p "Continue? (y/N) " ans
    [[ "$ans" == "y" || "$ans" == "Y" ]] || exit 0
    $COMPOSE down -v
    ;;
  *)
    echo "Usage: ODOO_TAG=18 $0 {init|up|logs|stop|restart|update|reset}"
    exit 1
    ;;
esac
