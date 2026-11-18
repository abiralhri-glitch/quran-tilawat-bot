"""
Quran Tilawat Master Runner
সূরা নির্বাচন, ডাউনলোড, কপিরাইট সুরক্ষা প্রক্রিয়াকরণ এবং ফেসবুকে স্বয়ংক্রিয় আপলোড
(১. একই দিনে একই সূরা ডাবল আপলোড হবে না
 ২. একই আয়াত কখনো ডুপ্লিকেট হবে না)
"""

import os
import random
import json
import time
import datetime
import requests
from config import BASE_DIR, LOGS_FILE, FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, FB_GRAPH_URL
from quran_surah_database import QARIS, LONG_SURAHS, REELS_SURAHS
from quran_downloader import download_quran_video
from anti_copyright_quran import process_quran_video
from caption_engine import generate_quran_caption
from fb_video_uploader import upload_quran_video_to_page

def get_fb_posted_records() -> tuple:
    """
    ফেসবুক পেজের ভিডিওগুলো বিশ্লেষণ করে:
    ১. আজকের দিনে (Today) কোন কোন সূরা আপলোড হয়েছে
    ২. কোন কোন আয়াত (Ayat range) ইতিমধ্যে পেজে বিদ্যমান
    """
    surahs_posted_today = set()
    exact_ayats_posted = set()

    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        return surahs_posted_today, exact_ayats_posted

    utc_now = datetime.datetime.now(datetime.timezone.utc)
    bd_now = utc_now + datetime.timedelta(hours=6)
    today_bd_str = bd_now.strftime("%Y-%m-%d")

    try:
        url = f"{FB_GRAPH_URL}/{FB_PAGE_ID}/videos?limit=100&fields=id,description,created_time&access_token={FB_PAGE_ACCESS_TOKEN}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            items = r.json().get("data", [])
            for item in items:
                desc = item.get("description", "")
                created_utc = item.get("created_time", "")
                # বাংলাদেশ সময় অনুযায়ী ডেট বের করা
                is_today = False
                if created_utc:
                    try:
                        # e.g. 2026-11-17T11:22:15+0000
                        dt_utc = datetime.datetime.fromisoformat(created_utc.replace("+0000", "+00:00"))
                        dt_bd = dt_utc + datetime.timedelta(hours=6)
                        if dt_bd.strftime("%Y-%m-%d") == today_bd_str:
                            is_today = True
                    except Exception:
                        pass

                all_catalog = LONG_SURAHS + REELS_SURAHS
                for s in all_catalog:
                    s_name = s["bangla"]
                    s_ayahs = s.get("ayahs", "")
                    if s_name in desc:
                        if is_today:
                            surahs_posted_today.add(s_name)
                        if s_ayahs and s_ayahs in desc:
                            exact_ayats_posted.add(f"{s_name}_{s_ayahs}")

            print(f"[SMART-SCHEDULER] আজকের দিনে আপলোড হওয়া সূরা ({len(surahs_posted_today)}টি): {list(surahs_posted_today)}")
            print(f"[SMART-SCHEDULER] ইতিমধ্যে পেজে থাকা নির্দিষ্ট আয়াত ({len(exact_ayats_posted)}টি): {list(exact_ayats_posted)}")
    except Exception as e:
        print(f"[RUNNER] Notice checking FB live records: {e}")

    return surahs_posted_today, exact_ayats_posted

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
            json.dump(history[-300:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[RUNNER] Warning: Failed to save history: {e}")

def select_smart_surah(is_reel: bool = True) -> tuple:
    """
    ১. আজকের দিনে এই সূরা ইতিমধ্যে আপলোড হয়ে থাকলে বাদ দেবে।
    ২. এই নির্দিষ্ট আয়াত ইতিমধ্যে পেজে থাকলে বাদ দেবে।
    ৩. ক্বারী দৈবচয়ন করবে।
    """
    surahs_posted_today, exact_ayats_posted = get_fb_posted_records()
    catalog = REELS_SURAHS if is_reel else LONG_SURAHS

    # ফিল্টার ১: একই দিনে একই সূরা না + একই আয়াত না
    valid_candidates = []
    for s in catalog:
        s_name = s["bangla"]
        s_ayahs = s.get("ayahs", "")
        ayat_key = f"{s_name}_{s_ayahs}"
        
        # শর্ত ১: আজ এই সূরা ইতিমধ্যে আপলোড হয়েছে কি না
        if s_name in surahs_posted_today:
            continue
        # শর্ত ২: এই নির্দিষ্ট আয়াত ইতিমধ্যে পোস্ট হয়েছে কি না
        if ayat_key in exact_ayats_posted:
            continue
            
        valid_candidates.append(s)

    # যদি সব শেষ হয়ে যায় (সব ১১৪ সূরা বা আয়াত শেষ হলে)
    if not valid_candidates:
        print("[SMART-SCHEDULER] সমস্ত সূরা আজকের জন্য রোটেশনে শেষ হয়েছে। শুধুমাত্র আজকের জন্য পোস্ট না হওয়া সূরা নেওয়া হচ্ছে...")
        valid_candidates = [s for s in catalog if s["bangla"] not in surahs_posted_today]
        if not valid_candidates:
            valid_candidates = catalog

    chosen_surah = random.choice(valid_candidates)
    chosen_qari = random.choice(QARIS)
    return chosen_surah, chosen_qari

def run_single_post():
    history = load_history()
    
    # 75% Reels, 25% Long Surahs
    is_reel = random.random() < 0.75
    
    surah, qari = select_smart_surah(is_reel=is_reel)
    qari_name = qari["name"]
    qari_en = qari["en"]
    ayahs_text = surah.get("ayahs", "পূর্ণাঙ্গ")

    if is_reel:
        search_query = f"{surah['bangla']} {qari_en} quran recitation bangla subtitle"
    else:
        search_query = f"{surah['bangla']} full {qari_en} quran recitation bangla translation"

    print(f"\n========================================================")
    print(f"📖 সিলেক্টেড সূরা: {surah['bangla']} [আয়াত: {ayahs_text}]")
    print(f"🎙️ ক্বারী: {qari_name} ({qari_en}) | টাইপ: {'রিলস (Reel)' if is_reel else 'লং ভিডিও (Long)'}")
    print(f"========================================================")
    
    # ১. ডাউনলোড (Pinterest/Pixabay HD + YouTube Tilawat Voice + Anti-Copyright)
    video_meta = download_quran_video(search_query, is_reel=is_reel, surah_data=surah)
    input_video_path = video_meta.get("filepath") or video_meta.get("file_path")
    
    # ২. এন্টি-কপিরাইট ফিল্টারিং
    processed_video_path = process_quran_video(input_video_path, output_name="clean_quran_upload.mp4")
    
    # ৩. ক্যাপশন ও টাইটেল প্রস্তুত (ভিডিওর সাথে ১০০% সামঞ্জস্যপূর্ণ)
    if video_meta.get("caption"):
        caption = video_meta["caption"]
        title = video_meta.get("title", f"{surah['arabic']} • {surah['bangla']} | ক্বারী {qari_name}")
    else:
        caption = generate_quran_caption(surah, qari_name, is_reel=is_reel)
        title = f"{surah['arabic']} • {surah['bangla']} [আয়াত: {ayahs_text}] | ক্বারী {qari_name}"
    
    # ৪. ফেসবুকে আপলোড
    upload_result = upload_quran_video_to_page(processed_video_path, caption=caption, title=title)
    
    # ৫. হিস্ট্রি রেকর্ড
    item_key = f"{surah['bangla']}_{ayahs_text}_{qari_en}"
    history.append({
        "key": item_key,
        "surah": surah["bangla"],
        "ayahs": ayahs_text,
        "qari": qari_name,
        "is_reel": is_reel,
        "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "result": upload_result
    })
    save_history(history)
    
    # ৬. ক্লিনআপ
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
                time.sleep(15)
        except Exception as e:
            print(f"[RUNNER] Error during post {i+1}: {e}")
            results.append({"error": str(e)})
    return results

if __name__ == "__main__":
    import sys
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_batch_posts(batch)
