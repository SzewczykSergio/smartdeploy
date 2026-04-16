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

<div style="width: 300px; margin: 10px auto;">
    <div id="progress" style="
        height: 10px;
        width: 100%;
        background: #1e293b;
        border-radius: 5px;
        overflow: hidden;
    ">
        <div id="bar" style="
            height: 100%;
            width: 100%;
            background: #3b82f6;
            transition: width 1s linear;
        "></div>
    </div>
</div>

        <div class="container">
            <div class="card">
                <h3>CPU Usage</h3>
                <div class="value" id="cpu">0%</div>
            </div>

            <div class="card">
                <h3>RAM Usage</h3>
                <div class="value" id="ram">0%</div>
            </div>

            <div class="card">
                <h3>Disk Usage</h3>
                <div class="value" id="disk">0%</div>
            </div>

            <div class="card">
                <h3>Containers</h3>
                <div class="value" id="containers">0</div>
            </div>
        </div>

        <a class="button" href="/containers">View Containers</a>
        <a class="button" href="/logs">View Logs</a>
        <a class="button" href="/deploy">Deploy App</a>

<script>
    async function updateData() {{
        try {{
            const res = await fetch("/system");
            const data = await res.json();

            document.getElementById("cpu").innerText = data.cpu_percent + "%";
            document.getElementById("ram").innerText = data.ram_percent + "%";
            document.getElementById("disk").innerText = data.disk_percent + "%";
        }} catch (err) {{
            console.log("Error fetching system data");
        }}

        try {{
            const res2 = await fetch("/containers");
            const data2 = await res2.json();

            document.getElementById("containers").innerText = data2.running_containers.length;
        }} catch (err) {{
            console.log("Error fetching containers");
        }}
    }}

    setInterval(updateData, 2000);

    // run once on load
    updateData();
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