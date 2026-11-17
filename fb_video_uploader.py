"""
Facebook Reels & Video Uploader for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
Supports official Facebook Graph API Video Reels resumable protocol
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

    file_size = os.path.getsize(video_path)
    print(f"[UPLOADER] Uploading {os.path.basename(video_path)} as Facebook Reel ({file_size / (1024*1024):.2f} MB)...")

    # Phase 1: Initialize Reels Upload Session
    try:
        init_url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/video_reels"
        init_payload = {
            "upload_phase": "start",
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        r = requests.post(init_url, data=init_payload, timeout=30)
        data = r.json()

        if "video_id" in data and "upload_url" in data:
            video_id = data["video_id"]
            upload_url = data["upload_url"]
            print(f"[+] Initialized Reel upload session: Video ID {video_id}")

            # Phase 2: Upload Binary Video Data
            with open(video_path, "rb") as f:
                video_bytes = f.read()

            upload_headers = {
                "Authorization": f"OAuth {FB_PAGE_ACCESS_TOKEN}",
                "offset": "0",
                "file_size": str(file_size)
            }
            upload_resp = requests.post(upload_url, headers=upload_headers, data=video_bytes, timeout=180)
            print(f"[+] Reels binary upload status: {upload_resp.status_code}")

            # Phase 3: Finish and Publish as Reel
            finish_payload = {
                "upload_phase": "finish",
                "access_token": FB_PAGE_ACCESS_TOKEN,
                "video_id": video_id,
                "video_state": "PUBLISHED",
                "description": caption
            }
            finish_resp = requests.post(init_url, data=finish_payload, timeout=30)
            finish_data = finish_resp.json()
            print(f"[+] Reels finish result: {finish_data}")
            return {"id": video_id, "success": True, "reels_response": finish_data}
    except Exception as e:
        print(f"[UPLOADER] Reels API notice: {e}, falling back to standard...")

    # Standard fallback
    url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/videos"
    print(f"[UPLOADER] Posting to standard videos endpoint...")
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
        print(f"[UPLOADER] Facebook Standard Video Upload Response: {resp}")
        return resp
