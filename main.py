from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
import psutil
import subprocess
import socket
import time
import os
from fastapi import Request
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


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
            .section {{
                margin-top: 50px;
                padding: 25px;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
                text-align: left;
                background: #1e293b;
                border-radius: 10px;
            }}
            .section h3, .section h4 {{
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>VPS Dashboard</h1>
        <p>Host: {socket.gethostname()}</p>

        <p>
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
        <a class="button" href="/generator">AI Description Generator</a>

        <div class="section">
            <h3>• How It Works</h3>
            <p>
                This dashboard is part of a DevOps project demonstrating automated deployment
                and infrastructure management on a VPS.
            </p>

            <ul style="line-height: 1.8;">
                <li>Application built with FastAPI and containerized using Docker</li>
                <li>CI/CD pipeline implemented with Jenkins</li>
                <li>Automatic deployment handled by Ansible playbook</li>
                <li>Application runs inside Docker container on VPS</li>
                <li>System metrics (CPU, RAM, Disk) collected in real-time</li>
            </ul>

            <h4>• Deployment Flow</h4>
            <p>
                GitHub → Jenkins → Docker Build → Ansible → Running Container
            </p>

            <h4>• What You See</h4>
            <ul style="line-height: 1.8;">
                <li>Live CPU, RAM and Disk usage</li>
                <li>Number of running containers</li>
                <li>Quick access to logs and deployment actions</li>
            </ul>

            <p style="margin-top:20px; font-size:12px; color:#94a3b8;">
                Project: SmartDeploy | DevOps CI/CD demonstration
            </p>
        </div>

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


@app.get("/containers", response_class=HTMLResponse)
def containers():
    containers = ["smartdeploy-app", "jenkins"]

    items = "".join([f"<li>{c}</li>" for c in containers])

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
        <h2>Containers</h2>
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
    <head>
        <title>Live Logs</title>
        <style>
            body {
                background: #0f172a;
                color: white;
                font-family: monospace;
                padding: 20px;
            }
            .box {
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                height: 500px;
                overflow-y: scroll;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <h2>Live Logs (real-time)</h2>

        <div id="logs" class="box"></div>

        <br>
        <a href="/">← Back</a>

        <script>
            const logBox = document.getElementById("logs");

            const evtSource = new EventSource("/api/logs/stream");

            evtSource.onmessage = function(event) {
                if (event.data.includes("ERROR")) {
                    logBox.innerHTML += "<span style='color:red'>" + event.data + "</span><br>";
                } else if (event.data.includes("WARNING")) {
                    logBox.innerHTML += "<span style='color:orange'>" + event.data + "</span><br>";
                } else if (event.data.includes("INFO")) {
                    logBox.innerHTML += "<span style='color:lightgreen'>" + event.data + "</span><br>";
                } else {
                    logBox.innerHTML += event.data + "<br>";
                }

                logBox.scrollTop = logBox.scrollHeight;
            };

            evtSource.onerror = function() {
                logBox.innerHTML += "<span style='color:red'>[connection lost]</span><br>";
            };
        </script>
    </body>
    </html>
    """

from fastapi.responses import StreamingResponse
import subprocess

@app.get("/api/logs/stream")
def stream_logs():
    def generate():
        try:
            process = subprocess.Popen(
                ["docker", "logs", "-f", "--tail", "50", "smartdeploy-app-new"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in iter(process.stdout.readline, ""):
                if "GET /system" in line or "GET /api/containers" in line:
                    continue

                yield f"data: {line.strip()}\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
    
function connectLogs() {
    const evtSource = new EventSource("/api/logs/stream");

    evtSource.onmessage = function(event) {
        logBox.innerHTML += event.data + "<br>";
        logBox.scrollTop = logBox.scrollHeight;
    };

    evtSource.onerror = function() {
        logBox.innerHTML += "<span style='color:red'>[reconnecting...]</span><br>";
        evtSource.close();
        setTimeout(connectLogs, 2000);
    };
}

connectLogs();
    
@app.post("/api/generate-description")
async def generate_description(request: Request):
    data = await request.json()

    name = data.get("name")
    features = data.get("features")
    tone = data.get("tone", "professional")

    prompt = f"""
    Write a {tone} product description.

    Product: {name}
    Features: {features}

    Make it engaging and clear.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "description": response.choices[0].message.content
    }
    
from fastapi.responses import HTMLResponse

@app.get("/generator", response_class=HTMLResponse)
def generator_ui():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Product Generator</title>
            <style>
                body {
                    background: #0f172a;
                    font-family: Arial, sans-serif;
                    color: white;
                    display: flex;
                    justify-content: center;
                    padding: 40px;
                }

                .container {
                    width: 600px;
                    background: #1e293b;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.5);
                }

                h1 {
                    text-align: center;
                    margin-bottom: 20px;
                }

                input, textarea, select {
                    width: 100%;
                    padding: 12px;
                    margin-top: 12px;
                    border-radius: 8px;
                    border: none;
                    font-size: 14px;
                    box-sizing: border-box;
                }
                
                textarea {
                    resize: none;
                    height: 140px;
                }

                button {
                    width: 100%;
                    padding: 14px;
                    margin-top: 16px;
                    background: #22c55e;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background: #16a34a;
                }

                #loader {
                    display: none;
                    text-align: center;
                    margin-top: 15px;
                }

                #result {
                    margin-top: 20px;
                    background: #0f172a;
                    padding: 15px;
                    border-radius: 8px;
                    white-space: pre-wrap;
                }

                .copy-btn {
                    margin-top: 10px;
                    background: #3b82f6;
                }
            </style>
        </head>
        <body>

        <div class="container">
            <h1>AI Product Description Generator</h1>

            <input id="name" placeholder="Product name" />
            <textarea id="features" placeholder="Features (comma separated)"></textarea>

            <select id="tone">
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="funny">Funny</option>
            </select>

            <button onclick="generate()">Generate</button>

            <div id="loader">AI is thinking...</div>

            <div id="result"></div>
            <button class="copy-btn" onclick="copyText()">Copy</button>
        </div>

        <script>
        async function generate() {
            const name = document.getElementById("name").value;
            const features = document.getElementById("features").value;
            const tone = document.getElementById("tone").value;

            document.getElementById("loader").style.display = "block";
            document.getElementById("result").innerText = "";

            const res = await fetch("/api/generate-description", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, features, tone })
            });

            const data = await res.json();

            document.getElementById("loader").style.display = "none";
            document.getElementById("result").innerText = data.description;
        }

        function copyText() {
            const text = document.getElementById("result").innerText;
            navigator.clipboard.writeText(text);
        }
        </script>

        </body>
        </html>
        """