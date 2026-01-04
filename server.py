from flask import render_template
from flask import Flask, request
import os, subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

process = None

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, "video.mp4")
    f.save(path)
    return "UPLOADED"

@app.route("/start")
def start():
    global process
    key = request.args.get("key")
    video = os.path.join(UPLOAD_FOLDER, "video.mp4")
    cmd = [
        "ffmpeg","-re","-stream_loop","-1","-i",video,
        "-c:v","copy","-c:a","aac","-f","flv",
        f"rtmp://a.rtmp.youtube.com/live2/{key}"
    ]
    process = subprocess.Popen(cmd)
    return "LIVE STARTED"

@app.route("/stop")
def stop():
    global process
    if process:
        process.kill()
        process = None
    return "STOPPED"

app.run(host="0.0.0.0", port=10000)
