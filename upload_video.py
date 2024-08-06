import os
import logging
import random
from flask import Flask, jsonify
from instagrapi import Client
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get credentials from environment variables
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

if not username or not password:
    logger.error("Username or password not set in environment variables")
    exit(1)

# Initialize the Instagram Client
cl = Client()

used_videos = set()

def get_random_video_path(folder_path, used_videos):
    videos = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    available_videos = [video for video in videos if video not in used_videos]
    if not available_videos:
        logger.info("Resetting used videos list")
        used_videos.clear()
        available_videos = videos
    video = random.choice(available_videos)
    used_videos.add(video)
    return os.path.join(folder_path, video)

def login_and_upload():
    try:
        cl.login(username, password)
        logger.info(f"Login successful for {username}")
    except Exception as e:
        logger.error(f"Login failed for {username}: {e}")
        return
    
    video_path = get_random_video_path("assets", used_videos)
    if not video_path:
        return
    
    caption = "Mau Amal jariyah terus ngalir meskipun sudah meninggal? bisa Share video ini agar sodara muslim kita yang lain bisa mendapatkan ilmu berharga #dakwah #ustadzadihidayat #sholat"
    
    try:
        cl.video_upload(video_path, caption)
        logger.info(f"Video uploaded successfully for {username}")
    except Exception as e:
        logger.error(f"Video upload failed for {username}: {e}")

@app.route('/upload', methods=['POST'])
def upload():
    login_and_upload()
    return jsonify({"status": "Upload Triggered"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
