#!/bin/bash

# Apply database migrations
#echo "Apply database migrations"
#python manage.py makemigrations
#python manage.py migrate

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

export DJANGO_SETTINGS_MODULE=core.settings

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
