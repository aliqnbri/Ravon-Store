#!/bin/bash

# Run makemigrations and migrate commands
python manage.py makemigrations core
python manage.py makemigrations account
python manage.py makemigrations customer
python manage.py makemigrations product
python manage.py makemigrations order
python manage.py makemigrations payment
python manage.py migrate

