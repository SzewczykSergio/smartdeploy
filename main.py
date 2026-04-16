from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
def dashboard():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    containers = get_docker_containers()

    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="5">
        <title>DevOps Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                text-align: center;
            }}
            h1 {{
                margin-top: 30px;
            }}
            .container {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .card {{
                background: #1e293b;
                padding: 20px;
                margin: 15px;
                width: 250px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}
            .value {{
                font-size: 28px;
                margin-top: 10px;
            }}
            .button {{
                display: block;
                margin: 10px auto;
                padding: 10px;
                width: 200px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            .button:hover {{
                background: #2563eb;
            }}
        </style>
    </head>
    <body>
        <h1>🚀 DevOps Dashboard</h1>
        <p>Host: {socket.gethostname()}</p>
        <p>Refreshing in <span id="timer">5</span>s</p>

        <div class="container">
            <div class="card">
                <h3>CPU Usage</h3>
                <div class="value">{cpu}%</div>
            </div>

            <div class="card">
                <h3>RAM Usage</h3>
                <div class="value">{ram}%</div>
            </div>

            <div class="card">
                <h3>Disk Usage</h3>
                <div class="value">{disk}%</div>
            </div>

            <div class="card">
                <h3>Containers</h3>
                <div class="value">{len(containers)}</div>
            </div>
        </div>

        <a class="button" href="/containers">View Containers</a>
        <a class="button" href="/logs">View Logs</a>
        <a class="button" href="/deploy">Deploy App</a>

<script>
    let timeLeft = 5;
    const timer = document.getElementById("timer");

    setInterval(() => {
        timeLeft--;
        if (timeLeft <= 0) {
            timeLeft = 5;
        }
        timer.innerText = timeLeft;
    }, 1000);
</script>

    </body>
    </html>
    """


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
    return {
        "logs": "Run on server: docker logs smartdeploy-app"
    }


@app.get("/deploy")
def deploy():
    try:
        subprocess.Popen(["bash", "deploy.sh"])
        return {"status": "Deployment started"}
    except:
        return {"error": "Deployment failed"}