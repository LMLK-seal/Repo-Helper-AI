#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run the vector DB indexing script
python vector_db.py