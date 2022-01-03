#!/bin/sh

# Database
dbm="/app/database/migration"
[ -d "$dbm" ] || flask db init --directory $dbm
flask db migrate --directory $dbm
flask db upgrade --directory $dbm

# Assets
flask assets build

# Static ressources
mkdir -p ./static/img
cp -Rv ./app/custom/img ./static

exec gunicorn --bind 0.0.0.0:8000 --workers 2 'app:create_app()' "$@"
