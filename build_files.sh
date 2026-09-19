#!/bin/bash
echo "Creating virtual environment for build..."
python3 -m venv venv_build
source venv_build/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
mkdir -p staticfiles
touch staticfiles/.gitkeep
echo "Running database migrations..."
python manage.py migrate --noinput
echo "Cleaning up build environment to reduce bundle size..."
deactivate || true
rm -rf venv_build
