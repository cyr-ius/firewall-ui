#!/bin/sh

# Assets
flask --app ./src assets build

# Static ressources
mkdir -p ./static/img
cp -Rv ./src/ressources/admin ./static
cp -Rv ./src/ressources/img ./static
cp -Rv ./src/ressources/css/fonts ./static/css

exec gunicorn --bind 0.0.0.0:8000 --workers 3 'src:create_app()' "$@"
