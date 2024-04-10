#!/bin/sh

echo "Apply database migrations"
python manage.py migrate

exec "$@"