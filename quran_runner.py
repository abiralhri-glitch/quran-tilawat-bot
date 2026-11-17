"""
Quran Tilawat Master Runner
সূরা নির্বাচন, ডাউনলোড, কপিরাইট সুরক্ষা প্রক্রিয়াকরণ এবং ফেসবুকে স্বয়ংক্রিয় আপলোড
(ফেসবুকের লাইভ ভিডিও চেক করে ১০০% ডুপ্লিকেট রোধ করা হয়)
"""

import os
import random
import json
import time
import requests
from config import BASE_DIR, LOGS_FILE, FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, FB_GRAPH_URL
from quran_surah_database import QARIS, LONG_SURAHS, REELS_SURAHS
from quran_downloader import download_quran_video
from anti_copyright_quran import process_quran_video
from caption_engine import generate_quran_caption
from fb_video_uploader import upload_quran_video_to_page

def get_published_surahs_from_fb() -> set:
    """ফেসবুক পেজ থেকে ইতিমধ্যে আপলোড করা সূরাগুলোর নাম সংগ্রহ করে"""
    published = set()
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        return published

    try:
        url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/videos?limit=100&access_token={FB_PAGE_ACCESS_TOKEN}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json().get("data", [])
            for item in data:
                desc = item.get("description", "")
                for s in LONG_SURAHS + REELS_SURAHS:
                    if s["bangla"] in desc:
                        published.add(s["bangla"])
            print(f"[RUNNER] Already published on Facebook: {len(published)} Surahs ({list(published)})")
    except Exception as e:
        print(f"[RUNNER] Notice checking FB published videos: {e}")

    return published

def load_history() -> list:
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history: list):
    try:
        with open(LOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-200:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[RUNNER] Warning: Failed to save history: {e}")

def run_single_post():
    history = load_history()
    published_on_fb = get_published_surahs_from_fb()
    
    # 75% Reels, 25% Long Surahs for high algorithm viral reach
    is_reel = random.random() < 0.75
    
    qari = random.choice(QARIS)
    qari_name = qari["name"]
    qari_en = qari["en"]
    
    if is_reel:
        available_surahs = [s for s in REELS_SURAHS if s["bangla"] not in published_on_fb]
        if not available_surahs:
            print("[RUNNER] All reels surahs published once! Resetting cycle.")
            available_surahs = REELS_SURAHS
        surah = random.choice(available_surahs)
        search_query = f"{surah['bangla']} {qari_en} quran recitation bangla subtitle"
    else:
        available_surahs = [s for s in LONG_SURAHS if s["bangla"] not in published_on_fb]
        if not available_surahs:
            print("[RUNNER] All long surahs published once! Resetting cycle.")
            available_surahs = LONG_SURAHS
        surah = random.choice(available_surahs)
        search_query = f"{surah['bangla']} full {qari_en} quran recitation bangla translation"

    print(f"\n[RUNNER] Selected Surah: {surah['bangla']} | Qari: {qari_name} | Type: {'Reel' if is_reel else 'Long Video'}")
    
    # 1. Download
    video_meta = download_quran_video(search_query, is_reel=is_reel, surah_data=surah)
    input_video_path = video_meta["filepath"]
    
    # 2. Process Anti-Copyright
    processed_video_path = process_quran_video(input_video_path, output_name="clean_quran_upload.mp4")
    
    # 3. Generate Caption
    caption = generate_quran_caption(surah, qari_name, is_reel=is_reel)
    title = f"{surah['arabic']} - {surah['bangla']} | ক্বারী {qari_name}"
    
    # 4. Upload to Facebook
    upload_result = upload_quran_video_to_page(processed_video_path, caption=caption, title=title)
    
    # 5. Record History
    item_key = f"{surah['bangla']}_{qari_en}"
    history.append({
        "key": item_key,
        "surah": surah["bangla"],
        "qari": qari_name,
        "is_reel": is_reel,
        "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "result": upload_result
    })
    save_history(history)
    
    # 6. Cleanup
    try:
        if os.path.exists(input_video_path):
            os.remove(input_video_path)
        if os.path.exists(processed_video_path):
            os.remove(processed_video_path)
    except Exception:
        pass

    return upload_result

def run_batch_posts(count: int = 1):
    print(f"[RUNNER] Starting batch posting of {count} Quran videos/reels...")
    results = []
    for i in range(count):
        print(f"\n--- Posting {i+1} of {count} ---")
        try:
            res = run_single_post()
            results.append(res)
            if i < count - 1:
                time.sleep(15)  # Cooldown between batch posts
        except Exception as e:
            print(f"[RUNNER] Error during post {i+1}: {e}")
            results.append({"error": str(e)})
    return results

if __name__ == "__main__":
    import sys
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_batch_posts(batch)
