#!/bin/sh

set -e

while ! pg_isready -h postgres -p 5432 > /dev/null 2> /dev/null; do
    echo "Waiting for postgres..."
    sleep 3
done
echo "PostgreSQL started"

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata default_user

python manage.py loadusers

exec "$@"
