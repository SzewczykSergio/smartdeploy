# SmartDeploy

## Overview

SmartDeploy is a full-stack DevOps project demonstrating an end-to-end CI/CD pipeline with real-time monitoring and AI-powered features.

It showcases how to build, deploy, and manage a containerized application on a VPS using modern DevOps tools.

Live Demo: https://devops.szewczyk.cloud/

---

## Features

### DevOps & Infrastructure
- Linux VPS setup and management
- Docker containerization
- Jenkins CI/CD pipeline (auto-triggered by GitHub push)
- Automated deployment using Ansible
- NGINX reverse proxy with domain routing

### Monitoring Dashboard
- Real-time CPU, RAM, Disk usage
- Live container tracking
- Clean web UI with navigation
- Auto-refreshing system metrics

### Logs System
- Real-time log streaming (Server-Sent Events)
- Docker logs integration
- Log filtering (INFO / WARNING / ERROR)

### AI Integration
- AI-powered product description generator
- Multiple tones (professional, casual, funny)
- Clean interactive UI
- Copy-to-clipboard feature

---

## Architecture

GitHub → Jenkins → Docker Build → Ansible → Running Container

### Flow Explained
1. Code pushed to GitHub
2. Jenkins pipeline triggers automatically
3. Docker image is built and tagged
4. Ansible deploys updated container
5. Application runs on VPS

---

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: HTML + CSS + JavaScript
- CI/CD: Jenkins
- Configuration Management: Ansible
- Containerization: Docker
- Web Server: NGINX
- Infrastructure: Linux VPS

---

## Monitoring System

The dashboard provides:

- CPU usage
- RAM usage
- Disk usage
- Number of running containers

Data is fetched from:
- `/system` API (psutil)
- `/api/containers` endpoint

Updates every 2 seconds in real-time.

---

## Logs Streaming

- Uses Server-Sent Events (SSE)
- Streams live Docker logs from:
  docker logs -f smartdeploy-app
- Filters out noisy system requests
- Displays logs with color-coded levels

---

## AI Generator

The app includes an AI-powered feature that:

- Generates product descriptions
- Accepts:
  - Product name
  - Features (comma-separated)
  - Tone selection
- Uses OpenAI API under the hood

---

## Key DevOps Concepts

- CI/CD automation
- Infrastructure as Code (Ansible)
- Idempotent deployments
- Container lifecycle management
- Reverse proxy configuration
- Real-time monitoring
- Log streaming architecture

---

## Challenges Solved

- Fixing Docker port conflicts
- Handling container restarts
- Debugging broken pipelines
- Fixing SSE connection issues
- Secure handling of API keys (Jenkins credentials)

---

## How to Run (Local)

git clone https://github.com/SzewczykSergio/smartdeploy.git  
cd smartdeploy  
docker build -t smartdeploy .  
docker run -p 8000:8000 smartdeploy  

---

## Notes

- Deployment uses an ephemeral container to run Ansible
- CI/CD environment stays clean and reproducible
- Jenkins injects secrets securely via credentials

---

## Project Purpose

This project demonstrates real-world DevOps practices, combining:

- Automation
- Monitoring
- AI integration
- Production debugging

---

## Author

Sergiusz Szewczyk