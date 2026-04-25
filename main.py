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
        <title>SmartDeploy Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                margin: 0;
                display: flex;
                justify-content: center;
                padding: 30px;
            }}

            .wrapper {{
                width: 100%;
                max-width: 1000px;
            }}

            /* NAVBAR */
            .navbar {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
                font-size: 14px;
            }}

            .navbar a {{
                color: #94a3b8;
                text-decoration: none;
                margin-right: 15px;
                transition: 0.2s;
            }}

            .navbar a:hover {{
                color: white;
            }}

            h1 {{
                text-align: center;
            }}

            .status {{
                text-align: center;
                margin-bottom: 20px;
                color: #22c55e;
            }}

            .container {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }}

            .card {{
                background: #1e293b;
                padding: 20px;
                margin: 10px;
                width: 220px;
                border-radius: 10px;
                text-align: center;
            }}

            .value {{
                font-size: 26px;
                margin-top: 10px;
            }}

            .buttons {{
                margin-top: 20px;
                text-align: center;
            }}

            .button {{
                display: inline-block;
                margin: 10px;
                padding: 12px 20px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 6px;
            }}

            .button:hover {{
                background: #2563eb;
            }}

            .section {{
                margin-top: 40px;
                padding: 25px;
                background: #1e293b;
                border-radius: 12px;
                line-height: 1.6;
            }}

            h2, h3 {{
                margin-top: 10px;
            }}

            ul {{
                padding-left: 20px;
            }}
        </style>
    </head>

    <body>
    <div class="wrapper">

        <!-- NAVBAR -->
        <div class="navbar">
            <div>
                <a href="/">Home</a>
                <a href="/generator">Generator</a>
                <a href="/logs">Logs</a>
                <a href="/containers">Containers</a>
            </div>
        </div>

        <h1>SmartDeploy Dashboard</h1>
        <p style="text-align:center;">Host: {socket.gethostname()}</p>

        <div class="status">
            ● Live system metrics & container monitoring
        </div>

        <div class="container">
            <div class="card">
                <h3>CPU</h3>
                <div class="value" id="cpu">0%</div>
            </div>

            <div class="card">
                <h3>RAM</h3>
                <div class="value" id="ram">0%</div>
            </div>

            <div class="card">
                <h3>Disk</h3>
                <div class="value" id="disk">0%</div>
            </div>

            <div class="card">
                <h3>Containers</h3>
                <div class="value" id="containers">0</div>
            </div>
        </div>

        <div class="buttons">
            <a class="button" href="/generator">AI Generator</a>
            <a class="button" href="/containers">View Containers</a>
            <a class="button" href="/logs">View Logs</a>
        </div>

        <!-- IMPROVED SECTION -->
        <div class="section">

            <h2>SmartDeploy – DevOps Automation Demo</h2>

            <p>
                This project showcases a complete DevOps pipeline running on a VPS,
                demonstrating real-world deployment automation and infrastructure management.
            </p>

            <h3>Architecture</h3>
            <ul>
                <li><b>FastAPI</b> backend application</li>
                <li><b>Docker</b> containerized environment</li>
                <li><b>Jenkins</b> CI/CD pipeline triggered by GitHub</li>
                <li><b>Ansible</b> automated deployment</li>
                <li>Runs on a <b>Linux VPS</b></li>
            </ul>

            <h3>Deployment Flow</h3>
            <p>GitHub → Jenkins → Docker Build → Ansible → Live Container</p>

            <h3>Features</h3>
            <ul>
                <li>Real-time CPU, RAM, Disk monitoring</li>
                <li>Live container tracking</li>
                <li>Streaming logs</li>
                <li>AI-powered product description generator</li>
            </ul>

            <h3>What This Demonstrates</h3>
            <ul>
                <li>End-to-end CI/CD pipeline</li>
                <li>Infrastructure as Code (IaC)</li>
                <li>Container lifecycle management</li>
                <li>AI integration in DevOps workflow</li>
            </ul>

            <p style="margin-top:15px; color:#94a3b8;">
                SmartDeploy | DevOps Portfolio Project
            </p>

        </div>

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
                margin: 0;
                display: flex;
                justify-content: center;
                padding: 30px;
            }}

            .wrapper {{
                width: 100%;
                max-width: 900px;
            }}

            .navbar {{
                margin-bottom: 20px;
            }}

            .navbar a {{
                color: #94a3b8;
                text-decoration: none;
                margin-right: 15px;
            }}

            .navbar a:hover {{
                color: white;
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
                padding: 12px;
                border-bottom: 1px solid #334155;
            }}

            h2 {{
                margin-bottom: 15px;
            }}
        </style>
    </head>

    <body>
    <div class="wrapper">

        <div class="navbar">
            <a href="/">Home</a>
            <a href="/generator">Generator</a>
            <a href="/logs">Logs</a>
            <a href="/containers">Containers</a>
        </div>

        <h2>Containers</h2>

        <div class="box">
            <ul>
                {items}
            </ul>
        </div>

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
                margin: 0;
                display: flex;
                justify-content: center;
                padding: 30px;
            }

            .wrapper {
                width: 100%;
                max-width: 1000px;
            }

            .navbar {
                margin-bottom: 20px;
                font-family: Arial;
            }

            .navbar a {
                color: #94a3b8;
                text-decoration: none;
                margin-right: 15px;
            }

            .navbar a:hover {
                color: white;
            }

            .box {
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                height: 500px;
                overflow-y: scroll;
                white-space: pre-wrap;
            }

            h2 {
                margin-bottom: 15px;
                font-family: Arial;
            }
        </style>
    </head>

    <body>
    <div class="wrapper">

        <div class="navbar">
            <a href="/">Home</a>
            <a href="/generator">Generator</a>
            <a href="/logs">Logs</a>
            <a href="/containers">Containers</a>
        </div>

        <h2>Live Logs (real-time)</h2>

        <div id="logs" class="box"></div>

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

    </div>
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
                ["docker", "logs", "-f", "--tail", "50", "smartdeploy-app"],
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
                margin: 0;
            }

            .wrapper {
                width: 100%;
                max-width: 700px;
            }

            /* NAVBAR */
            .navbar {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
                font-size: 14px;
            }

            .navbar a {
                color: #94a3b8;
                text-decoration: none;
                margin-right: 15px;
                transition: 0.2s;
            }

            .navbar a:hover {
                color: white;
            }

            .container {
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
                color: #94a3b8;
            }

            #result {
                margin-top: 20px;
                background: #0f172a;
                padding: 15px;
                border-radius: 8px;
                white-space: pre-wrap;
                min-height: 80px;
            }

            .copy-btn {
                margin-top: 10px;
                background: #3b82f6;
            }

            .copy-btn:hover {
                background: #2563eb;
            }

            .back-btn {
                display: inline-block;
                margin-bottom: 10px;
                color: #94a3b8;
                text-decoration: none;
                font-size: 14px;
            }

            .back-btn:hover {
                color: white;
            }
        </style>
    </head>
    <body>

    <div class="wrapper">

        <!-- NAVBAR -->
        <div class="navbar">
            <div>
                <a href="/">Home</a>
                <a href="/generator">Generator</a>
                <a href="/logs">Logs</a>
                <a href="/containers">Containers</a>
            </div>
        </div>

        <div class="container">
            <a href="/" class="back-btn">← Back</a>

            <h1>AI Product Description Generator</h1>

            <input id="name" placeholder="Product name" />
            <textarea id="features" placeholder="Features (comma separated)"></textarea>

            <select id="tone">
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="funny">Funny</option>
            </select>

            <button onclick="generate()">Generate</button>

            <div id="loader">AI is generating your description...</div>

            <div id="result"></div>
            <button class="copy-btn" onclick="copyText()">Copy</button>
        </div>

    </div>

    <script>
    async function generate() {
        const name = document.getElementById("name").value;
        const features = document.getElementById("features").value;
        const tone = document.getElementById("tone").value;

        document.getElementById("loader").style.display = "block";
        document.getElementById("result").innerText = "";

        try {
            const res = await fetch("/api/generate-description", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, features, tone })
            });

            const data = await res.json();

            document.getElementById("result").innerText = data.description;
        } catch (err) {
            document.getElementById("result").innerText = "Error generating description.";
        }

        document.getElementById("loader").style.display = "none";
    }

    function copyText() {
        const text = document.getElementById("result").innerText;
        navigator.clipboard.writeText(text);

        const btn = document.querySelector(".copy-btn");
        btn.innerText = "Copied!";
        setTimeout(() => btn.innerText = "Copy", 1500);
    }
    </script>

    </body>
    </html>
    """