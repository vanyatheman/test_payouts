#!/usr/bin/env bash

set -ex

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn payouts_project.wsgi:application --bind 0:8000 --reload
# python manage.py runserver 0:8000