#!/bin/bash

find . -type d -name "migrations" -not -path "./.venv/*" -exec rm -rf {} \;