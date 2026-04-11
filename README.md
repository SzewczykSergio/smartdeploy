\#SmartDeploy



\##Overview

SmartDeploy is a DevOps project demonstrating how to deploy a containerized backend application on a secured VPS.



This project covers:

\- Linux server setup

\- SSH hardening

\- Docker containerization

\- Public deployment



\---



\##Tech Stack

\- Linux (Ubuntu VPS)

\- Docker

\- FastAPI (Python)

\- Git \& GitHub



\---



\##Infrastructure

\- SSH key-based authentication

\- Disabled password login

\- Disabled root login

\- Non-root user with sudo privileges



\---



\##Application

A simple FastAPI app with two endpoints:



\- `/` → returns message + hostname  

\- `/health` → health check endpoint  



\---



\##Live Demo

http://51.178.39.34:8000



\---



\##Run locally



```bash

docker build -t smartdeploy .

docker run -p 8000:8000 smartdeploy

