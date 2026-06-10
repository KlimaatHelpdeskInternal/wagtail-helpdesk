#!/usr/bin/env bash
# Exit on error
set -o errexit

python manage.py collectstatic --no-input --settings=settings.render-showcase
# Apply any outstanding database migrations
python manage.py makemigrations --settings=settings.render-showcase
python manage.py migrate --settings=settings.render-showcase