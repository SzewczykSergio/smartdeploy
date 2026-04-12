from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def home():
    return {
    "message": "Hello from your DevOps app v2",
    "hostname": socket.gethostname()
    }

@app.get("/health")
def health():
    return {"status": "ok"}

