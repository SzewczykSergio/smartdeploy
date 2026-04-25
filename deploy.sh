#!/bin/bash

set -e

echo "Starting deployment..."

cd /app_host/app || { echo "Failed to enter directory"; exit 1; }

echo "Pulling latest code..."
git config --global --add safe.directory /app_host/app
git pull || { echo "Git pull failed"; exit 1; }

echo "Building Docker image..."
docker build -t smartdeploy:latest . || { echo "Docker build failed"; exit 1; }

echo "Stopping old container..."
docker stop smartdeploy-app-new || echo "No container to stop"

echo "Removing old container..."
docker rm smartdeploy-app-new || echo "No container to remove"

echo "Starting new container..."
docker run -d \
  -p 8000:8000 \
  --name smartdeploy-app-new \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /home/devops/smartdeploy:/app_host \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  smartdeploy:latest || { echo "Failed to start container"; exit 1; }

echo "Deployment finished successfully!"