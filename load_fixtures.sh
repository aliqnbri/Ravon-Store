#!/bin/bash

# Set the apps for which to load fixtures
APPS="account product core customer payment order"


#Load fixtures for each app
for APP in $APPS; do
  python manage.py loaddata $APP/fixtures/$APP.json
  echo "Loaded fixtures for $app"
done