#!/bin/sh

# Database
dbm="/app/database/migration"
[ -d "$dbm" ] || flask db init --directory $dbm
flask db migrate --directory $dbm
flask db upgrade --directory $dbm

# Assets
flask assets build
cp -Rf /app/ressources/admin /app/static

exec gunicorn --bind 0.0.0.0:8000 --workers 3 'app:create_app()' "$@"
