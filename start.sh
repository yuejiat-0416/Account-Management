#!/bin/bash

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start Django
python manage.py runserver 0.0.0.0:8000

