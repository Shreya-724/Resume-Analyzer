#!/usr/bin/env bash
echo "=== Building AI Resume Analyzer ==="

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -c "import spacy; spacy.cli.download('en_core_web_sm')"

echo "=== Build completed successfully ==="