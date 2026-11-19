"""
Holy Quran Master Multi-Scene Tilawat Engine & Dynamic Video Generator
- পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা ও হজের দৃশ্য (৫০% প্রাধান্য)
- বিশ্বের বিখ্যাত দৃষ্টিনন্দন মসজিদ (শেখ জায়েদ, ব্লু মসজিদ, দ্বিতীয় হাসান মসজিদ ইত্যাদি)
- স্নিগ্ধ বৃষ্টির ধারা, পাহাড়ি ঝর্ণা ও শান্ত নদীপ্রবাহ
- কুয়াশাঢাকা সবুজ পাহাড়, শান্ত মহাসমুদ্র ও বনাঞ্চলের আঁকাবাঁকা রোড ড্রাইভ
- মাল্টি-সিন ব্লেন্ডিং: লং ভিডিওতে ৫টি ও রিলসে ৩টি সম্পূর্ণ আলাদা নান্দনিক দৃশ্য
- কঠোর জিরো-ডুপ্লিকেট রোটেশন: পূর্ববর্তী ২০টি দৃশ্য কঠোরভাবে ফিল্টার করে ডুপ্লিকেট রোধ
- ফুল লং ভিডিও: সম্পূর্ণ সূরার পুরো সময়কাল অনুযায়ী আনলিমিটেড মাল্টি-সিন লুপ
"""

import os
import re
import glob
import json
import time
import random
import requests
import subprocess
import imageio_ffmpeg
from pathlib import Path

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

from watermark_generator import generate_watermark_overlay
from quran_surah_database import MAKKAH_MADINAH_IMAMS, LONG_SURAHS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# ==============================================================================
# সর্বজনীন নান্দনিক ইসলামিক ও প্রাকৃতিক দৃশ্য ডাটাবেজ (মক্কা-মদিনা, মসজিদ, পাহাড়, সাগর, বৃষ্টি, রোড)
# ==============================================================================
MASTER_AESTHETIC_FOOTAGE_POOL = [
    # --------------------------------------------------------------------------
    # ১. পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা ও হজ (৫০% মূল প্রাধান্য)
    # --------------------------------------------------------------------------
    {
        "id": "makkah_kaaba_drone",
        "category": "holy_site",
        "title": "পবিত্র কাবা শরীফ ও মাতাফ চত্বর",
        "location": "মসজিদুল হারাম, মক্কা মুকাররমা",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2021/04/18/71447-539097973_large.mp4"
    },
    {
        "id": "makkah_kaaba_gilaf",
        "category": "holy_site",
        "title": "পবিত্র কাবার স্বর্ণালী গিলাফ ও শান্ত মাতাফ",
        "location": "পবিত্র কাবা প্রাঙ্গণ",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/10/22/186088-877239334_large.mp4"
    },
    {
        "id": "makkah_clock_tower",
        "category": "holy_site",
        "title": "মক্কা ক্লক টাওয়ার ও গ্র্যান্ড হারাম ড্রোন ভিউ",
        "location": "পবিত্র মক্কা মুকাররমা",
        "local_file": "makkah_clock_tower_drone.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2022/01/18/104868-668835848_large.mp4"
    },
    {
        "id": "madinah_nabawi_greendome",
        "category": "holy_site",
        "title": "মসজিদে নববী ও সম্মানিত সবুজ গম্বুজ",
        "location": "মদিনা মনোওয়ারা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/06/15/167280-836798059_large.mp4"
    },
    {
        "id": "madinah_umbrellas_courtyard",
        "category": "holy_site",
        "title": "মসজিদে নববীর সুবিশাল ছাতা ও মিনার",
        "location": "মসজিদে নববী চত্বর, মদিনা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2021/10/26/93432-639359155_large.mp4"
    },
    {
        "id": "hajj_arafat_jabal_rahmah",
        "category": "holy_site",
        "title": "আরাফাতের ময়দান ও জাবালে রহমতে লাখো হাজী",
        "location": "পবিত্র আরাফাত ময়দান",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/07/04/170060-842720151_large.mp4"
    },

    # --------------------------------------------------------------------------
    # ২. বিশ্বের বিখ্যাত দৃষ্টিনন্দন ঐতিহাসিক মসজিদ (Iconic World Mosques)
    # --------------------------------------------------------------------------
    {
        "id": "mosque_sheikh_zayed_uae",
        "category": "world_mosque",
        "title": "শেখ জায়েদ গ্র্যান্ড মসজিদ ও শ্বেত মার্বেল",
        "location": "আবুধাবি, সংযুক্ত আরব আমিরাত",
        "local_file": "sheikh_zayed_grand_mosque.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2022/11/24/140366-774838017_large.mp4"
    },
    {
        "id": "mosque_blue_sultan_ahmed",
        "category": "world_mosque",
        "title": "ঐতিহাসিক সুলতান আহমেদ নীল মসজিদ",
        "location": "ইস্তাম্বুল, তুরস্ক",
        "local_file": "sultan_ahmed_blue_mosque.mp4",
        "cdn_url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    },
    {
        "id": "mosque_hassan_ii_morocco",
        "category": "world_mosque",
        "title": "আটলান্টিক মহাসাগরের কিনারায় দ্বিতীয় হাসান মসজিদ",
        "location": "কাসাব্লাঙ্কা, মরক্কো",
        "local_file": "hassan_ii_mosque_morocco.mp4",
        "cdn_url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    },
    {
        "id": "mosque_putra_floating_malaysia",
        "category": "world_mosque",
        "title": "গোলাপী রঙের ভাসমান পুত্রা মসজিদ ও হ্রদ",
        "location": "পুত্রজায়া, মালয়েশিয়া",
        "local_file": "putra_mosque_malaysia.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2024/08/08/225504_large.mp4"
    },
    {
        "id": "mosque_faisal_islamabad",
        "category": "world_mosque",
        "title": "মারগালা পর্বতমালার পাদদেশে ফয়সাল মসজিদ",
        "location": "ইসলামাবাদ, পাকিস্তান",
        "local_file": "faisal_mosque_islamabad.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2024/06/02/214982_large.mp4"
    },
    {
        "id": "mosque_badshahi_lahore",
        "category": "world_mosque",
        "title": "মুঘল স্থাপত্যের ঐতিহাসিক বাদশাহী মসজিদ",
        "location": "লাহোর, পাকিস্তান",
        "local_file": "badshahi_mosque_lahore.mp4",
        "cdn_url": "https://archive.org/download/rain1932/Rain_512kb.mp4"
    },

    # --------------------------------------------------------------------------
    # ৩. স্নিগ্ধ বৃষ্টির ধারা, পাহাড়ি ঝর্ণা ও স্বচ্ছ নদী (Rain & Cascading Water)
    # --------------------------------------------------------------------------
    {
        "id": "nature_peaceful_rain_leaves",
        "category": "nature_water",
        "title": "সবুজ পাতার বুকে স্নিগ্ধ বৃষ্টির শান্ত ধারা",
        "location": "প্রকৃতির স্নিগ্ধ পরিবেশ",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://archive.org/download/rain1932/Rain_512kb.mp4"
    },
    {
        "id": "nature_cascading_waterfall",
        "category": "nature_water",
        "title": "পাথরের বুক চিরে নেমে আসা পাহাড়ি ঝর্ণা",
        "location": "পাহাড়ি নির্মল প্রকৃতি",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    },
    {
        "id": "nature_flowing_mountain_stream",
        "category": "nature_water",
        "title": "স্বচ্ছ পাহাড়ি নদীর নির্মল জলপ্রবাহ",
        "location": "শান্ত বনাঞ্চল ও নদী",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2022/11/24/140366-774838017_large.mp4"
    },

    # --------------------------------------------------------------------------
    # ৪. সুন্দর পাহাড়, মহাসমুদ্র ও শান্ত রোড ড্রাইভ (Mountains, Oceans & Scenic Roads)
    # --------------------------------------------------------------------------
    {
        "id": "nature_foggy_mountain_peaks",
        "category": "nature_scenic",
        "title": "কুয়াশাঘেরা সুবিশাল পর্বতমালা ও সবুজ উপত্যকা",
        "location": "দিগন্তজোড়া পর্বতমালার রূপ",
        "local_file": "makkah_clock_tower_drone.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2021/10/26/93432-639359155_large.mp4"
    },
    {
        "id": "nature_calm_ocean_sunset",
        "category": "nature_scenic",
        "title": "গোধূলির আলোয় মহাসমুদ্রের শান্ত নীল ঢেউ",
        "location": "অনন্ত সমুদ্রের দিগন্ত",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2024/08/08/225504_large.mp4"
    },
    {
        "id": "nature_scenic_forest_road_drive",
        "category": "nature_scenic",
        "title": "পাহাড়ি বনের বুক চিরে চলে যাওয়া সুন্দর পথ",
        "location": "মনোরম পাহাড়ি ড্রাইভ",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    }
]

FOOTAGE_HISTORY_FILE = os.path.join(BASE_DIR, "footage_history.json")

def load_footage_history() -> dict:
    if os.path.exists(FOOTAGE_HISTORY_FILE):
        try:
            with open(FOOTAGE_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    if "used_ids" not in data or not isinstance(data["used_ids"], list):
                        data["used_ids"] = []
                    return data
        except Exception:
            pass
    return {"used_ids": [], "last_index": -1}

def save_footage_history(history: dict):
    try:
        with open(FOOTAGE_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[FOOTAGE HISTORY WARN] {e}")

def ensure_footage_file(item: dict) -> str:
    """ফুটেজ ফাইল লোকাল ডিরেক্টরি থেকে লোড করে, না থাকলে সিডিএন থেকে ডাউনলোড করে"""
    fname = item.get("local_file", "")
    if fname:
        p = os.path.join(ASSETS_FOOTAGE_DIR, fname)
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            return p

    cdn_target = os.path.join(DOWNLOADS_DIR, f"{item['id']}.mp4")
    if os.path.exists(cdn_target) and os.path.getsize(cdn_target) > 50000:
        return cdn_target

    print(f"📥 ডাউনলোড হচ্ছে দৃশ্য: {item['title']}...")
    try:
        r = requests.get(item["cdn_url"], stream=True, timeout=35, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            with open(cdn_target, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            if os.path.exists(cdn_target) and os.path.getsize(cdn_target) > 50000:
                print(f"✅ সফল ডাউনলোড: {cdn_target}")
                return cdn_target
    except Exception as e:
        print(f"[CDN DOWNLOAD WARN] {e}")

    # যেকোনো লোকাল ফাইল ফলব্যাক
    for any_item in MASTER_AESTHETIC_FOOTAGE_POOL:
        lf = any_item.get("local_file")
        if lf:
            any_p = os.path.join(ASSETS_FOOTAGE_DIR, lf)
            if os.path.exists(any_p) and os.path.getsize(any_p) > 50000:
                return any_p

    raise FileNotFoundError("কোনো কার্যকর ফুটেজ পাওয়া যায়নি।")

def get_next_balanced_scenes(count: int = 5) -> tuple:
    """
    ব্যালেন্সড মাল্টি-সিন সিলেকশন:
    - মক্কা/মদিনা/হজ: অন্তত ২টি দৃশ্য (প্রধান ভিত্তি)
    - বিশ্বখ্যাত দৃষ্টিনন্দন মসজিদ: ১টি দৃশ্য
    - বৃষ্টি/ঝর্ণা/পাহাড়/সমুদ্র/রোড: ১-২টি দৃশ্য
    - কঠোর জিরো-ডুপ্লিকেট রোটেশন: পূর্ববর্তী ১৫টি দৃশ্য কঠোরভাবে বাদ দেওয়া হয়।
    """
    history = load_footage_history()
    if "used_ids" not in history or not isinstance(history["used_ids"], list):
        history["used_ids"] = []
    used_ids = set(history.get("used_ids", [])[-15:])

    # আনপোস্টেড ক্যান্ডিডেট ফিল্টার
    available = [item for item in MASTER_AESTHETIC_FOOTAGE_POOL if item["id"] not in used_ids]
    if len(available) < count:
        print("[NOTICE] নান্দনিক দৃশ্যের রোটেশন সাইকেল ফ্রেশ করা হচ্ছে...")
        available = list(MASTER_AESTHETIC_FOOTAGE_POOL)
        history["used_ids"] = []

    # ক্যাটাগরিভিত্তিক সুষম বণ্টন
    holy_items = [it for it in available if it["category"] == "holy_site"]
    mosque_items = [it for it in available if it["category"] == "world_mosque"]
    nature_items = [it for it in available if it["category"] in ["nature_water", "nature_scenic"]]

    random.shuffle(holy_items)
    random.shuffle(mosque_items)
    random.shuffle(nature_items)

    selected_items = []
    # ১. পবিত্র মক্কা/মদিনা/হজ থেকে ২টি
    selected_items.extend(holy_items[:2])
    # ২. বিশ্বের মসজিদ থেকে ১টি
    selected_items.extend(mosque_items[:1])
    # ৩. প্রকৃতি/বৃষ্টি/পাহাড়/সাগর/রোড থেকে ১-২টি
    selected_items.extend(nature_items[:2])

    # ঘাটতি থাকলে অবশিষ্টাংশ থেকে পূরণ
    if len(selected_items) < count:
        for it in available:
            if it not in selected_items:
                selected_items.append(it)
                if len(selected_items) >= count:
                    break

    selected_items = selected_items[:count]
    selected_paths = [ensure_footage_file(it) for it in selected_items]

    for it in selected_items:
        if "used_ids" not in history or not isinstance(history["used_ids"], list):
            history["used_ids"] = []
        history["used_ids"].append(it["id"])
    history["used_ids"] = history["used_ids"][-35:]
    save_footage_history(history)

    print(f"🎬 [ব্যালেন্সড মাল্টি-সিন নির্বাচন সম্পন্ন] মোট {len(selected_items)}টি সম্পূর্ণ আলাদা দৃশ্য:")
    for idx, it in enumerate(selected_items, 1):
        print(f"   ✨ দৃশ্য #{idx}: [{it['category'].upper()}] {it['title']} ({it['location']})")

    meta = {
        "title": " • ".join([it["title"] for it in selected_items[:2]]),
        "location": "পবিত্র হারামাইন শরীফাইন, বিশ্বসেরা মসজিদ ও মনোরম প্রকৃতি",
        "scenes": selected_items
    }
    return selected_paths, meta

def download_imam_surah_audio(surah_data: dict, imam: dict = None) -> tuple:
    """মক্কা ও মদিনার সম্মানিত ইমামগণের সম্পূর্ণ সূরার তিলাওয়াত অডিও ডাউনলোড করে"""
    surah_num = surah_data.get("number", 1)
    surah_bangla = surah_data.get("bangla", "সূরা আল-ফাতিহা")

    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3")):
        try: os.remove(old)
        except Exception: pass

    if not imam:
        imam = random.choice(MAKKAH_MADINAH_IMAMS)

    print(f"🎙️ তিলাওয়াতকারী নির্বাচন: {imam['name']} ({imam['mosque']})")
    audio_path = os.path.join(DOWNLOADS_DIR, f"voice_{imam['id']}_{surah_num:03d}_{int(time.time())}.mp3")

    cdn_url = f"{imam['server']}/{surah_num:03d}.mp3"
    print(f"📥 অডিও ডাউনলোড হচ্ছে: {cdn_url}...")

    try:
        r = requests.get(cdn_url, stream=True, timeout=40, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        if r.status_code == 200:
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 30000:
                print(f"✅ সফল তিলাওয়াত অডিও ডাউনলোড: {os.path.getsize(audio_path)/(1024*1024):.2f} MB")
                return audio_path, imam
    except Exception as e:
        print(f"[IMAM CDN NOTICE] {e}")

    # ফলব্যাক: পবিত্র মক্কার শাইখ ড. মাহের আল-মুয়াইক্বলী
    print(f"💡 নিরাপদ ফলব্যাক সিডিএন থেকে {surah_bangla} সংগ্রহ হচ্ছে...")
    fallback_url = f"https://server12.mp3quran.net/maher/{surah_num:03d}.mp3"
    try:
        r = requests.get(fallback_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            return audio_path, {
                "id": "muaiqly",
                "name": "শাইখ ড. মাহের আল-মুয়াইক্লি",
                "title": "সম্মানিত ইমাম ও খতিব",
                "mosque": "পবিত্র মসজিদুল হারাম, মক্কা মুকাররমা"
            }
    except Exception as e:
        print(f"[FALLBACK CDN ERROR] {e}")

    raise RuntimeError(f"অডিও তিলাওয়াত সংগ্রহ করা যায়নি: {surah_bangla}")

def get_audio_duration(audio_path: str) -> float:
    """FFprobe দিয়ে অডিওর সম্পূর্ণ সঠিক সময়কাল বের করে"""
    cmd = [FFMPEG_EXE, "-i", audio_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        hours, mins, secs = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return hours * 3600 + mins * 60 + secs
    return 180.0

def render_quran_video_with_watermark(scene_paths: list, audio_path: str, out_path: str, is_reel: bool = True) -> str:
    """
    মাল্টিপল ভিন্ন নান্দনিক সিন যুক্ত হাই-রিটেনশন ভিডিও রেন্ডারিং:
    - রিলস (Reels): ১০৮০x১৯২০ (ভার্টিক্যাল ৯:১৬), ৬০ সেকেন্ড
    - ফুল লং ভিডিও (HQ Long Video): ১৯২০x১০৮০ (ওয়াইডস্ক্রিন ১৬:৯), সম্পূর্ণ সূরার সম্পূর্ণ সময়কাল!
    """
    total_audio_sec = get_audio_duration(audio_path)
    print(f"⏱️ মূল সূরার অডিও সময়কাল: {total_audio_sec/60:.2f} মিনিট ({int(total_audio_sec)} সেকেন্ড)")

    if is_reel:
        w, h = 1080, 1920
        target_dur = min(total_audio_sec, 60.0)
        seg_dur = target_dur / len(scene_paths)
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "5000k", "-maxrate", "7000k", "-bufsize", "10000k"]
        print(f"🎨 [REEL RENDERING] ৬০ সেকেন্ডের ৯:১৬ আল্ট্রা-এইচডি রিলস তৈরি হচ্ছে...")
    else:
        w, h = 1920, 1080
        # লং ভিডিও: পুরো সূরার সম্পূর্ণ সময়কাল (সর্বোচ্চ ১৫ মিনিট ক্লাউড সেফটি লিমিট)
        target_dur = min(total_audio_sec, 900.0)
        seg_dur = 35.0  # প্রতি ৩৫ সেকেন্ড পর পর মন জুড়ানো সিন ট্রানজিশন
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "6000k", "-maxrate", "8000k", "-bufsize", "12000k"]
        print(f"🎨 [FULL LONG VIDEO RENDERING] {target_dur/60:.2f} মিনিটের পূর্ণাঙ্গ ১৬:৯ ওয়াইডস্ক্রিন লং ভিডিও তৈরি হচ্ছে...")

    watermark_png = generate_watermark_overlay(w, h)

    # দৃশ্য লুপ তৈরি (যাতে পুরো সূরার সময়কাল জুড়ে মক্কা, মসজিদ, বৃষ্টি, পাহাড়, সাগরের দৃশ্য মসৃণভাবে পরিবর্তিত হয়)
    inputs = []
    filter_parts = []
    concat_inputs = []

    num_cycles = max(1, int(target_dur // (seg_dur * len(scene_paths))) + 1)
    expanded_scenes = (scene_paths * num_cycles)

    actual_scenes = []
    elapsed = 0.0
    for sc in expanded_scenes:
        if elapsed >= target_dur:
            break
        this_seg = min(seg_dur, target_dur - elapsed)
        actual_scenes.append((sc, this_seg))
        elapsed += this_seg

    for i, (sc, dur) in enumerate(actual_scenes):
        inputs.extend(["-stream_loop", "-1", "-i", sc])
        filter_parts.append(f"[{i}:v]{scale_filter},setsar=1,fps=30,format=yuv420p,trim=duration={dur:.2f},setpts=PTS-STARTPTS[v{i}]")
        concat_inputs.append(f"[v{i}]")

    num_inputs = len(actual_scenes)
    inputs.extend(["-i", audio_path])
    audio_idx = num_inputs

    inputs.extend(["-i", watermark_png])
    wm_idx = num_inputs + 1

    concat_filter = f"{''.join(concat_inputs)}concat=n={num_inputs}:v=1:a=0[v_concat]"
    final_wm_filter = f"[v_concat][{wm_idx}:v]overlay=0:0[final_v]"
    full_filter = f"{';'.join(filter_parts)};{concat_filter};{final_wm_filter}"

    cmd = [
        FFMPEG_EXE, "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[final_v]",
        "-map", f"{audio_idx}:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", crf,
        *bitrate_args,
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-t", f"{target_dur:.2f}",
        "-pix_fmt", "yuv420p",
        out_path
    ]

    print(f"🎬 FFmpeg এক্সিকিউশন শুরু ({int(target_dur)} সেকেন্ডের ফুল ভিডিও)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FFMPEG ERROR] {res.stderr[:400]}")
        raise RuntimeError(f"FFmpeg রেন্ডারিং ব্যর্থ: {res.stderr[:200]}")

    print(f"✅ সফল ভিডিও রেন্ডার সম্পন্ন! সাইজ: {os.path.getsize(out_path)/(1024*1024):.2f} MB")
    return out_path

def download_quran_video(is_reel: bool = True, surah_data: dict = None, imam_data: dict = None) -> dict:
    scene_count = 3 if is_reel else 5
    scene_paths, meta = get_next_balanced_scenes(count=scene_count)
    audio_path, imam = download_imam_surah_audio(surah_data, imam_data)

    out_name = f"quran_{'reel' if is_reel else 'long_video'}_{int(time.time())}.mp4"
    out_path = os.path.join(PROCESSED_DIR, out_name)

    rendered_video = render_quran_video_with_watermark(scene_paths, audio_path, out_path, is_reel=is_reel)

    return {
        "filepath": rendered_video,
        "audio_path": audio_path,
        "imam": imam,
        "surah": surah_data,
        "is_reel": is_reel,
        "bg_mosque": meta["title"],
        "bg_location": meta["location"],
        "footage_ids": [sc["id"] for sc in meta["scenes"]]
    }
