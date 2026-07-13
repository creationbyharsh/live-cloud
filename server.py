from flask import Flask, request, render_template
import os, subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

process = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "NO FILE", 400

    f = request.files["file"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], "video.mp4")
    f.save(path)
    return "UPLOADED"

@app.route("/start")
def start():
    global process
    key = request.args.get("key")
    video = os.path.join(app.config["UPLOAD_FOLDER"], "video.mp4")
    cmd = f"ffmpeg -re -stream_loop -1 -i {video} -c:v copy -c:a aac -f flv rtmp://a.rtmp.youtube.com/live2/{key}"
    os.system(cmd + " || " + cmd)
    return "LIVE STARTED"

@app.route("/stop")
def stop():
    global process
    if process:
        process.kill()
        process = None
    return "STOPPED"

app.run(host="0.0.0.0", port=10000)
