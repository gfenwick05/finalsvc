#!/usr/bin/env bash
set -euo pipefail
IMAGE=booksvc:latest

echo "Building Docker image..."
docker build -t $IMAGE .

echo "Starting container (listening on host:5000)..."
docker run --rm -p 5000:5000 $IMAGE
