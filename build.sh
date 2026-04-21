#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/uploads
mkdir -p instance

# Run database migrations (if any)
# python migrate.py

echo "Build completed successfully!"