#!bin/ash

echo "Apply database migrations"
python manage.py migrate

exec "$@"