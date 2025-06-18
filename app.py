from flask import Flask, render_template, request, send_file
import io
from overlay import create_reel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        img_file = request.files["image"]
        prompt = request.form["prompt"]
        video_bytes = create_reel(img_file.read(), prompt)
        return send_file(io.BytesIO(video_bytes),
                         mimetype="video/mp4",
                         as_attachment=True,
                         download_name="reel.mp4")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
