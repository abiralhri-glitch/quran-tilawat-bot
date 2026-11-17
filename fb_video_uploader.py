"""
Facebook Video Uploader for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
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
    print(f"[UPLOADER] Uploading {os.path.basename(video_path)} to Facebook Page ID: {FB_PAGE_ID}...")
    
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
        
        # টাইমলাইন ফিড (Posts / All tab) এ দৃশ্যমান করতে ফিড পোস্ট যুক্ত করা
        if "id" in resp:
            video_id = resp["id"]
            try:
                feed_url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/feed"
                feed_data = {
                    "message": caption,
                    "link": f"https://www.facebook.com/reel/{video_id}/",
                    "access_token": FB_PAGE_ACCESS_TOKEN
                }
                rf = requests.post(feed_url, data=feed_data, timeout=60)
                print(f"[UPLOADER] Timeline Feed Story Created: {rf.json()}")
            except Exception as fe:
                print(f"[UPLOADER] Feed story creation notice: {fe}")
                
        return resp
