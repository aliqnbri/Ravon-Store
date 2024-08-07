#!/bin/bash

# Set the project directory
PROJECT_DIR=$(dirname $(dirname $(readlink -f $0)))

# Change to the project directory
cd "$PROJECT_DIR"

# Get a list of all apps in the project
APPS=$(python manage.py showmigrations | awk '{print $1}' | grep -v '\<')

# Create fixtures directory for each app and dump data to fixtures files
for APP in $APPS; do
  FIXTURES_DIR=$APP/fixtures
  mkdir -p $FIXTURES_DIR
  echo "Dumping data for $APP to $FIXTURES_DIR..."
  python manage.py dumpdata $APP --indent=2 --output=$FIXTURES_DIR/$APP.json
done