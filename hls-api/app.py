from flask import Flask, jsonify, request
from flask_cors import CORS
import shutil

import os, subprocess
import threading

app = Flask(__name__)
CORS(app)

SHARED_FOLDER = "/shared"
OUTPUT_DIR = "/hls"

@app.route("/list_videos", methods=["GET"])
def list_videos():
    videos = [f for f in os.listdir(SHARED_FOLDER) if f.endswith((".mp4", ".mov"))]
    return jsonify({"videos": videos})

def run_ffmpeg(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

@app.route("/generate_hls", methods=["POST"])
def generate_hls():
    data = request.get_json()
    video_name = data.get("video_name", None)
    if not video_name:
        return jsonify({"error": "video_name is required"}), 400

    input_path = os.path.join(SHARED_FOLDER, video_name)
    output_path = os.path.join(OUTPUT_DIR, "output.m3u8")

    command = [
    "ffmpeg",  # The FFmpeg tool is used for multimedia processing.
    "-y",  # Overwrite existing output files without asking.
    "-i", input_path,  # Specifies the input video file.
    "-c:v", "copy",  # Copies the video codec (no re-encoding for speed).
    "-c:a", "copy",  # Copies the audio codec (no re-encoding for speed).
    "-f", "hls",  # Sets the output format as HLS (HTTP Live Streaming).
    "-hls_time", "4",  # Sets each HLS segment duration to 4 seconds.
    "-hls_playlist_type", "event",  # Keeps all segments in the playlist until encoding ends.
    "-hls_flags", "delete_segments+temp_file",  # Removes old segments and creates temporary files for atomic updates.
    "-hls_list_size", "3",  # Only keeps the last 3 segments in the playlist.
    output_path  # Specifies the output file for the HLS playlist.
]


    def wait_for_first_chunk():
        while True:
            files = os.listdir(OUTPUT_DIR)
            if any(f.endswith(".ts") for f in files):
                break


    def clear_output_dir():
        for f in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, f)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                
    clear_output_dir()
    process = threading.Thread(target=run_ffmpeg, args=(command,))
    process.start()

    wait_for_first_chunk()

    return jsonify({"message": "First chunk ready!", "playlist_url": f"{request.host_url}hls/output.m3u8"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



