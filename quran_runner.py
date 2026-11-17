"""
Quran Tilawat Master Runner
সূরা নির্বাচন, ডাউনলোড, কপিরাইট সুরক্ষা প্রক্রিয়াকরণ এবং ফেসবুকে স্বয়ংক্রিয় আপলোড
"""

import os
import random
import json
import time
from config import BASE_DIR, LOGS_FILE
from quran_surah_database import QARIS, LONG_SURAHS, REELS_SURAHS
from quran_downloader import download_quran_video
from anti_copyright_quran import process_quran_video
from caption_engine import generate_quran_caption
from fb_video_uploader import upload_quran_video_to_page

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
    
    # 75% Reels, 25% Long Surahs for high algorithm viral reach
    is_reel = random.random() < 0.75
    
    qari = random.choice(QARIS)
    qari_name = qari["name"]
    qari_en = qari["en"]
    
    if is_reel:
        available_surahs = [s for s in REELS_SURAHS if f"{s['bangla']}_{qari_en}" not in history]
        if not available_surahs:
            available_surahs = REELS_SURAHS
        surah = random.choice(available_surahs)
        search_query = f"{surah['bangla']} {qari_en} quran recitation bangla subtitle"
    else:
        available_surahs = [s for s in LONG_SURAHS if f"{s['bangla']}_{qari_en}" not in history]
        if not available_surahs:
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
