#!/usr/bin/env bash
# build.sh

echo "=== Building AI Resume Analyzer ==="

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Collect static files
python manage.py collectstatic --noinput --clear

echo "=== Build completed successfully ==="