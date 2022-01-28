#!/bin/bash
python manage.py migrate
nohup python manage.py register_event_listeners &
gunicorn Foobar_django_auth.wsgi:application --bind 0.0.0.0:8000 --log-level info --timeout 180 --workers 3
