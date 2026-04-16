# SmartDeploy

## Overview

SmartDeploy is a DevOps project demonstrating a complete CI/CD pipeline for deploying a containerized backend application on a VPS.

Live Demo: https://devops.szewczyk.cloud/

---

## Features

- Linux VPS setup and management
- Docker containerization
- CI/CD pipeline using Jenkins
- Automated deployment using Ansible
- Reverse proxy configuration with NGINX
- Real-time system monitoring dashboard (CPU, RAM, Disk, Containers)
- Public deployment with domain access

---

## Architecture

GitHub → Jenkins → Docker → Ansible → Running Container

- Jenkins builds Docker image on each commit
- Deployment is executed via Ansible playbook
- Ansible ensures container is always running (idempotent)
- Deployment runs inside ephemeral container (CI/CD pattern)

---

## Tech Stack

- Linux (Ubuntu VPS)
- Docker
- Jenkins (CI/CD)
- Ansible
- NGINX
- FastAPI (Python)
- JavaScript (live dashboard)

---

## Monitoring

The application includes a custom dashboard displaying:

- CPU usage
- RAM usage
- Disk usage
- Running containers

Data is updated in real-time via API.

---

## Key Concepts Used

- CI/CD pipeline automation
- Infrastructure as Code (Ansible)
- Idempotent deployments
- Container orchestration
- Reverse proxy configuration
- Debugging production issues (502 errors, container failures)

---

## Notes

Deployment is executed using an ephemeral container that installs Ansible at runtime.  
This approach keeps the CI/CD environment clean and reproducible.

---

## How to Run

```bash
docker build -t smartdeploy .
docker run -p 8000:8000 smartdeploy