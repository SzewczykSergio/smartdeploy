from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psutil
import subprocess
import socket

app = FastAPI()


# ✅ NEW API (FOR DASHBOARD)
@app.get("/api/containers")
def get_containers():
    return {
        "running_containers": ["smartdeploy-app", "jenkins"]
    }


@app.get("/", response_class=HTMLResponse)
def dashboard():
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
        </style>
    </head>
    <body>
        <h1>VPS Dashboard</h1>
        <p>Host: {socket.gethostname()}</p>

        <p style="color: white;">
            <span style="color: #22c55e;">●</span>
            Live system metrics
        </p>

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
            console.log("system error");
        }}

        try {{
            const res2 = await fetch("/api/containers");
            const data2 = await res2.json();

            document.getElementById("containers").innerText =
                data2.running_containers.length;
        }} catch (err) {{
            console.log("containers error");
        }}
    }}

    setInterval(updateData, 2000);
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


# ✅ HTML PAGE
@app.get("/containers", response_class=HTMLResponse)
def containers():
    containers = ["smartdeploy-app", "jenkins"]

    items = "".join([f"<li>🐳 {c}</li>" for c in containers])

    return f"""
    <html>
    <head>
        <title>Containers</title>
        <style>
            body {{
                background: #0f172a;
                color: white;
                font-family: Arial;
                padding: 20px;
            }}
            .box {{
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                padding: 10px;
                border-bottom: 1px solid #334155;
            }}
        </style>
    </head>
    <body>
        <h2>🐳 Containers</h2>
        <div class="box">
            <ul>
                {items}
            </ul>
        </div>
    </body>
    </html>
    """


@app.get("/logs", response_class=HTMLResponse)
def logs():
    return """
    <html>
    <body style="background:#0f172a;color:white;font-family:monospace;padding:20px;">
        <h2>📜 Logs</h2>
        <div style="background:#1e293b;padding:20px;border-radius:10px;">
            Run on server:<br><br>
            <b>docker logs smartdeploy-app</b>
        </div>
    </body>
    </html>
    """


@app.get("/deploy", response_class=HTMLResponse)
def deploy():
    subprocess.Popen(["bash", "deploy.sh"])

    return """
    <html>
    <body style="background:#0f172a;color:white;text-align:center;padding:40px;">
        <h2>🚀 Deployment started...</h2>
        <a href="/">Back</a>
    </body>
    </html>
    """