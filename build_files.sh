#!/bin/bash
echo "Creating virtual environment for build..."
python3 -m venv venv_build
source venv_build/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Running database migrations..."
python manage.py migrate --noinput
