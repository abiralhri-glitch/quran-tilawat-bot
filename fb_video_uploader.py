"""
Facebook Video Uploader for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
অফিসিয়াল ও ক্লিন মেটা ভিডিও পাবলিশার (কোনো ডুপ্লিকেট সেলফ-শেয়ার ছাড়া)
"""

import os
import requests
from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, FB_GRAPH_URL

def upload_quran_video_to_page(video_path: str, caption: str, title: str = "") -> dict:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID:
        print(f"[MOCK UPLOAD] Access token or Page ID not configured. Simulating video upload for {os.path.basename(video_path)}")
        return {"id": "mock_video_id_quran_123", "status": "simulated"}

    url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/videos"
    print(f"[UPLOADER] Uploading {os.path.basename(video_path)} cleanly to Facebook Page ID: {FB_PAGE_ID}...")
    
    with open(video_path, "rb") as vf:
        files = {"source": vf}
        data = {
            "description": caption,
            "title": title or caption.split("\n")[0][:60],
            "published": True,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        r = requests.post(url, files=files, data=data, timeout=300)
        resp = r.json()
        print(f"[UPLOADER] Facebook Video Upload Response: {resp}")
        return resp
