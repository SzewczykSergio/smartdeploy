from fastapi import FastAPI
import psutil
import subprocess
import socket

app = FastAPI()

def get_docker_containers():
    try:
        result = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"])
        return result.decode().splitlines()
    except:
        return []

@app.get("/")
def dashboard():
    return {
        "message": "DevOps Dashboard",
        "hostname": socket.gethostname()
    }

@app.get("/system")
def system_info():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

@app.get("/containers")
def containers():
    return {
        "running_containers": get_docker_containers()
    }

@app.get("/logs")
def logs():
    try:
        result = subprocess.check_output(["docker", "logs", "smartdeploy-app", "--tail", "20"])
        return {"logs": result.decode()}
    except:
        return {"error": "Could not fetch logs"}

@app.get("/deploy")
def deploy():
    try:
        subprocess.Popen(["bash", "deploy.sh"])
        return {"status": "Deployment started"}
    except:
        return {"error": "Deployment failed"}