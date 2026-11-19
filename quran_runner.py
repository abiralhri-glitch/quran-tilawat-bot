"""
Holy Quran Automated Orchestrator & Runner for 'কুরআনের তিলাওয়াত - Quran Tilawat'
- দৈনিক মোট ১০টি পোস্ট (সকালে ২টি এবং দুপুর ১টার পর থেকে প্রতি ১ ঘণ্টা পর পর ১টি করে মোট ৮টি)
- ৫টি আল্ট্রা-এইচডি ভার্টিক্যাল রিলস (1080x1920) এবং ৫টি ফুল এইচডি লং ভিডিও (1920x1080)
- আজান পোস্ট সম্পূর্ণ বাদ (শুধুমাত্র পবিত্র কুরআনের তিলাওয়াত)
- শুধুমাত্র পবিত্র মক্কা, মদিনা ও বিশ্ববিখ্যাত পবিত্র মসজিদের ১০৮০p সিনেমাটিক ফুটেজ
- কঠোর জিরো-ডুপ্লিকেট রোটেশন: একই ভিডিও পরপর বা একই দিনে ভিন্ন সূরায় কখনো রিপিট হবে না
- পেজের স্থায়ী ব্র্যান্ডেড ওয়াটারমার্ক যুক্ত রিলস ও ভিডিও
"""

import os
import sys
import json
import time
import random
import datetime

from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN
from quran_surah_database import MAKKAH_MADINAH_IMAMS, LONG_SURAHS
from quran_downloader import download_quran_video
from caption_engine import generate_quran_caption
from fb_video_uploader import upload_quran_video_to_page
from auto_comment_responder import run_comment_responder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_HISTORY_FILE = os.path.join(BASE_DIR, "posted_history.json")

def load_posted_history() -> dict:
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    default_history = {
        "last_surah_index": -1,
        "last_imam_index": -1,
        "last_format_was_reel": False,
        "daily_stats": {
            "date": today_str,
            "reels_posted": 0,
            "hq_videos_posted": 0,
            "total_today": 0
        }
    }
    if os.path.exists(POSTED_HISTORY_FILE):
        try:
            with open(POSTED_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Check if day changed
                    ds = data.get("daily_stats", {})
                    if ds.get("date") != today_str:
                        data["daily_stats"] = {
                            "date": today_str,
                            "reels_posted": 0,
                            "hq_videos_posted": 0,
                            "total_today": 0
                        }
                    return data
        except Exception:
            return default_history
    return default_history

def save_posted_history(history: dict):
    try:
        with open(POSTED_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HISTORY WARN] {e}")

def get_next_surah_and_imam() -> tuple:
    """পরবর্তী সূরা ও মক্কা/মদিনার ইমাম নির্বাচন করে (যাতে প্রতিটি সূরা ও ইমাম সমান গুরুত্ব পান)"""
    history = load_posted_history()
    last_surah_index = history.get("last_surah_index", -1)
    last_imam_index = history.get("last_imam_index", -1)

    next_surah_index = (last_surah_index + 1) % len(LONG_SURAHS)
    next_imam_index = (last_imam_index + 1) % len(MAKKAH_MADINAH_IMAMS)

    selected_surah = LONG_SURAHS[next_surah_index]
    selected_imam = MAKKAH_MADINAH_IMAMS[next_imam_index]

    history["last_surah_index"] = next_surah_index
    history["last_imam_index"] = next_imam_index
    save_posted_history(history)

    return selected_surah, selected_imam

def determine_post_format(forced_format: str = None) -> bool:
    """
    নির্ধারণ করে বর্তমান পোস্টটি রিলস (True) নাকি হাই-কোয়ালিটি রেগুলার ভিডিও (False):
    লক্ষ্য: দৈনিক ৫টি রিলস ও ৫টি ফুল এইচডি রেগুলার ভিডিও (মোট ১০টি পোস্ট)
    """
    if forced_format == "reel":
        return True
    elif forced_format == "video":
        return False

    history = load_posted_history()
    stats = history.get("daily_stats", {})
    reels_count = stats.get("reels_posted", 0)
    videos_count = stats.get("hq_videos_posted", 0)
    last_was_reel = history.get("last_format_was_reel", False)

    # অল্টারনেটিং সিলেকশন: একবার রিলস, একবার লং ভিডিও
    if reels_count < 5 and videos_count < 5:
        is_reel = not last_was_reel
    elif reels_count < 5:
        is_reel = True
    elif videos_count < 5:
        is_reel = False
    else:
        # ১০টি পূর্ণ হলে সাধারণ অল্টারনেটিং
        is_reel = not last_was_reel

    return is_reel

def run_single_quran_cycle(forced_format: str = None):
    print("\n========================================================")
    print("🚀 'কুরআনের তিলাওয়াত' অটোমেশন সাইকেল শুরু...")
    print("========================================================")

    # ১. ফরম্যাট নির্ধারণ (রিলস বনাম ফুল এইচডি রেগুলার ভিডিও)
    is_reel = determine_post_format(forced_format)
    format_label = "১০৮০x১৯২০ আল্ট্রা-এইচডি রিলস" if is_reel else "১৯২০x১০৮০ ফুল এইচডি রেগুলার ভিডিও"
    print(f"🎯 বর্তমান পোস্টিং ফরম্যাট: {format_label}")

    # ২. পরবর্তী সূরা ও সম্মানিত ইমাম নির্বাচন
    selected_surah, selected_imam = get_next_surah_and_imam()
    print(f"📖 নির্বাচিত সূরা: {selected_surah['bangla']} ({selected_surah['arabic']})")
    print(f"🎙️ নির্বাচিত ইমাম: {selected_imam['name']} • {selected_imam['mosque']}")

    # ৩. ভিডিও প্রস্তুতকরণ (পবিত্র মসজিদ ফুটেজ ও অফিসিয়াল ওয়াটারমার্ক সহ)
    video_metadata = download_quran_video(
        is_reel=is_reel,
        surah_data=selected_surah,
        imam_data=selected_imam
    )

    video_path = video_metadata["filepath"]
    mosque_info = f"{video_metadata.get('bg_mosque', '')} ({video_metadata.get('bg_location', '')})"
    caption = generate_quran_caption(
        selected_surah,
        f"{selected_imam['name']} ({selected_imam['mosque']})",
        mosque_info=mosque_info,
        is_reel=is_reel
    )
    title = f"{selected_surah['arabic']} • {selected_surah['bangla']} | {selected_imam['name']}"

    # ৪. ফেসবুকে নির্দিষ্ট চ্যানেলে আপলোড
    print(f"📤 ফেসবুকে আপলোড করা হচ্ছে ({'Reel API' if is_reel else 'High-Definition Feed API'})...")
    upload_res = upload_quran_video_to_page(
        video_path,
        caption=caption,
        title=title,
        is_reel=is_reel
    )
    print(f"✅ সফল তিলাওয়াত পোস্ট! রেজাল্ট: {upload_res}")

    # ৫. হিস্টোরি ও দৈনিক পরিসংখ্যান আপডেট
    history = load_posted_history()
    history["last_format_was_reel"] = is_reel
    stats = history.setdefault("daily_stats", {})
    if is_reel:
        stats["reels_posted"] = stats.get("reels_posted", 0) + 1
    else:
        stats["hq_videos_posted"] = stats.get("hq_videos_posted", 0) + 1
    stats["total_today"] = stats.get("total_today", 0) + 1
    print(f"📊 আজকের পরিসংখ্যান: মোট {stats['total_today']}/১০টি (রিলস: {stats['reels_posted']}/৫, রেগুলার ভিডিও: {stats['hq_videos_posted']}/৫)")
    save_posted_history(history)

    # ৬. ক্লিনআপ
    if os.path.exists(video_path):
        try: os.remove(video_path)
        except Exception: pass

    # ৭. কমেন্ট রেসপন্ডার
    try:
        run_comment_responder(page_type="quran", max_replies=10)
    except Exception as e:
        print(f"[COMMENT RESPONDER WARN] {e}")

if __name__ == "__main__":
    forced = None
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["reel", "video"]:
        forced = sys.argv[1].lower()

    run_single_quran_cycle(forced_format=forced)
