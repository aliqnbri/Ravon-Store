#!/bin/bash


# Set the project directory
PROJECT_DIR=$(dirname $(dirname $(dirname $0 | tr -d '\n')))

# Change to the project directory
cd "$PROJECT_DIR"


# Get a list of all apps in the project
APPS="account product core customer payment order"

# Create fixtures directory for each app and dump data to fixtures files
for APP in $APPS; do
  FIXTURES_DIR=$APP/fixtures
  mkdir -p "$FIXTURES_DIR"
  python manage.py dumpdata $APP --indent=2 --output="$FIXTURES_DIR/$APP.json"
  echo "Dumped data for $APP"
done
