#!/bin/bash

set -e  # Stop execution if a command fails.

# Extract Python version from template.yaml
PYTHON_VERSION=$(grep "Runtime:" template.yaml | head -n 1 | awk '{print $2}')

# echo "📦 Installing dependencias of requirements.txt for $PYTHON_VERSION..."
# mkdir -p layers/libs-layer/python/lib/$PYTHON_VERSION/site-packages
# pip install -r layers/libs-layer/requirements.txt -t layers/libs-layer/python/lib/$PYTHON_VERSION/site-packages

echo "🔨 Construyendo AWS SAM..."
sam build
