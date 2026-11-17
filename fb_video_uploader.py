"""
Facebook Reels & Video Uploader for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
Supports official Facebook Graph API Video Reels resumable protocol
"""

import os
import requests
from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, FB_GRAPH_URL

# Fresh verified Page Access Token for কুরআনের তিলাওয়াত (Page ID: 1430288070174104)
FRESH_QURAN_TOKEN = "EAAe1H3izQCYBTHEsjdMjMFYCAPKGkCfZCD1ZBt0T5QYGslyoq9NhlkE2k4yCPGslDd5wKnJsnTaNp9BTz2l3HdsEZBrsiZC7SZBWQBjPylgJmGfup6X48kIXzQoMx0itoObz7T3S6cETbj5gbPyIAxSquGr8VXAgrhgrKZAsZC5YpQ5ddQODAoeL1NjAobyN41JclnguLkGtndhZCidlDrlPtkkV84CKUQIMDh2Rq1PlYbcZD"
EFFECTIVE_TOKEN = FRESH_QURAN_TOKEN or FB_PAGE_ACCESS_TOKEN
EFFECTIVE_PAGE_ID = FB_PAGE_ID or "1430288070174104"

def upload_quran_video_to_page(video_path: str, caption: str, title: str = "") -> dict:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not EFFECTIVE_TOKEN or not EFFECTIVE_PAGE_ID:
        print(f"[MOCK UPLOAD] Access token or Page ID not configured. Simulating video upload for {os.path.basename(video_path)}")
        return {"id": "mock_video_id_quran_123", "status": "simulated"}

    file_size = os.path.getsize(video_path)
    print(f"[UPLOADER] Uploading {os.path.basename(video_path)} as Facebook Reel ({file_size / (1024*1024):.2f} MB)...")

    # Phase 1: Initialize Reels Upload Session
    try:
        init_url = f"{FB_GRAPH_URL}/{EFFECTIVE_PAGE_ID}/video_reels"
        init_payload = {
            "upload_phase": "start",
            "access_token": EFFECTIVE_TOKEN
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
                "Authorization": f"OAuth {EFFECTIVE_TOKEN}",
                "offset": "0",
                "file_size": str(file_size)
            }
            upload_resp = requests.post(upload_url, headers=upload_headers, data=video_bytes, timeout=180)
            print(f"[+] Reels binary upload status: {upload_resp.status_code}")

            # Phase 3: Finish and Publish as Reel
            finish_payload = {
                "upload_phase": "finish",
                "access_token": EFFECTIVE_TOKEN,
                "video_id": video_id,
                "video_state": "PUBLISHED",
                "description": caption
            }
            finish_resp = requests.post(init_url, data=finish_payload, timeout=30)
            finish_data = finish_resp.json()
            print(f"[+] Reels finish result: {finish_data}")
            if finish_data.get("success") or "video_id" in finish_data:
                return {"id": video_id, "success": True, "reels_response": finish_data}
    except Exception as e:
        print(f"[UPLOADER] Reels API notice: {e}, falling back to standard...")

    # Standard fallback
    url = f"{FB_GRAPH_URL}/{EFFECTIVE_PAGE_ID}/videos"
    print(f"[UPLOADER] Posting to standard videos endpoint...")
    with open(video_path, "rb") as vf:
        files = {"source": vf}
        data = {
            "description": caption,
            "title": title or caption.split("\n")[0][:60],
            "published": True,
            "access_token": EFFECTIVE_TOKEN
        }
        r = requests.post(url, files=files, data=data, timeout=300)
        resp = r.json()
        print(f"[UPLOADER] Facebook Standard Video Upload Response: {resp}")
        return resp
