"""
Facebook Reels & High-Quality Long Video Uploader for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
- supports official Facebook Graph API Video Reels resumable protocol
- supports official Facebook Graph API Resumable Chunked Upload for Full Long Videos
"""

import os
import requests
from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, FB_GRAPH_URL

def upload_quran_video_to_page(video_path: str, caption: str, title: str = "", is_reel: bool = True) -> dict:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    token = FB_PAGE_ACCESS_TOKEN
    page_id = FB_PAGE_ID or "1430288070174104"

    if not token:
        print(f"[MOCK UPLOAD] Access token not configured. Simulating video upload for {os.path.basename(video_path)}")
        return {"id": "mock_video_id_quran_123", "status": "simulated"}

    file_size = os.path.getsize(video_path)

    # =========================================================================
    # ১. যদি REEL হয়: Facebook Video Reels Resumable Upload (Short 9:16)
    # =========================================================================
    if is_reel:
        print(f"[REELS UPLOADER] Uploading {os.path.basename(video_path)} as Facebook Reel ({file_size / (1024*1024):.2f} MB)...")
        try:
            init_url = f"{FB_GRAPH_URL}/{page_id}/video_reels"
            init_payload = {
                "upload_phase": "start",
                "access_token": token
            }
            r = requests.post(init_url, data=init_payload, timeout=35)
            data = r.json()
            if "video_id" in data and "upload_url" in data:
                video_id = data["video_id"]
                upload_url = data["upload_url"]
                print(f"[+] Initialized Reel upload session: Video ID {video_id}")

                with open(video_path, "rb") as f:
                    video_bytes = f.read()

                upload_headers = {
                    "Authorization": f"OAuth {token}",
                    "offset": "0",
                    "file_size": str(file_size)
                }
                upload_resp = requests.post(upload_url, headers=upload_headers, data=video_bytes, timeout=180)
                print(f"[+] Reels binary upload status: {upload_resp.status_code}")

                finish_payload = {
                    "upload_phase": "finish",
                    "access_token": token,
                    "video_id": video_id,
                    "video_state": "PUBLISHED",
                    "description": caption
                }
                finish_resp = requests.post(init_url, data=finish_payload, timeout=35)
                finish_data = finish_resp.json()
                print(f"[+] Reels finish result: {finish_data}")
                if finish_data.get("success") or "video_id" in finish_data or "post_id" in finish_data or finish_resp.status_code == 200:
                    return {"id": video_id, "success": True, "type": "reel", "reels_response": finish_data}
        except Exception as e:
            print(f"[UPLOADER] Reels API warning: {e}. Falling back to standard videos endpoint...")

    # =========================================================================
    # ২. যদি HIGH QUALITY FULL LONG VIDEO হয়: Resumable Chunked Upload Protocol
    # =========================================================================
    print(f"[FULL LONG VIDEO UPLOADER] Uploading {os.path.basename(video_path)} via Resumable Chunked Protocol ({file_size / (1024*1024):.2f} MB)...")
    init_url = f"{FB_GRAPH_URL}/{page_id}/videos"
    try:
        # Phase 1: Start
        init_data = {
            "upload_phase": "start",
            "file_size": file_size,
            "access_token": token
        }
        r = requests.post(init_url, data=init_data, timeout=35)
        init_res = r.json()
        if "upload_session_id" not in init_res:
            print(f"[DIRECT FALLBACK] Resumable start not supported ({init_res}), trying direct post...")
            with open(video_path, "rb") as vf:
                r_direct = requests.post(
                    f"https://graph-video.facebook.com/v21.0/{page_id}/videos",
                    files={"source": vf},
                    data={"description": caption, "title": title[:65], "access_token": token},
                    timeout=360
                )
                return r_direct.json()

        upload_session_id = init_res["upload_session_id"]
        start_offset = int(init_res.get("start_offset", 0))

        # Phase 2: Transfer (8MB chunks)
        chunk_size = 8 * 1024 * 1024
        with open(video_path, "rb") as f:
            f.seek(start_offset)
            while start_offset < file_size:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                headers = {
                    "Authorization": f"OAuth {token}",
                    "offset": str(start_offset),
                    "file_size": str(file_size)
                }
                res_chunk = requests.post(
                    f"{FB_GRAPH_URL}/{page_id}/videos",
                    data=chunk,
                    headers=headers,
                    params={"upload_phase": "transfer", "upload_session_id": upload_session_id},
                    timeout=180
                )
                c_data = res_chunk.json()
                start_offset = int(c_data.get("start_offset", start_offset + len(chunk)))

        # Phase 3: Finish
        finish_data = {
            "upload_phase": "finish",
            "upload_session_id": upload_session_id,
            "title": title[:65],
            "description": caption,
            "access_token": token
        }
        finish_res = requests.post(f"{FB_GRAPH_URL}/{page_id}/videos", data=finish_data, timeout=60).json()
        print(f"[LONG VIDEO UPLOAD SUCCESS]: {finish_res}")
        return {"id": finish_res.get("id", upload_session_id), "success": True, "type": "hq_long_video", "response": finish_res}
    except Exception as e:
        print(f"[UPLOADER ERROR] Video upload failed: {e}")
        return {"error": str(e), "success": False}
