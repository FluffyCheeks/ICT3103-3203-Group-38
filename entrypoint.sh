#!/bin/sh

#python manage.py migrate --no-input
python manage.py collectstatic --no-input

#gunicorn pastelLuna.wsgi:application --bind 0.0.0.0:8000

python manage.py test --verbosity 2
python manage.py runserver 0.0.0.0:8000
