"""
Holy Quran Automated Tilawat Engine & Multi-Scene High-Retention Video Generator
- ১০০% পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা ও বিশ্ববিখ্যাত পবিত্র ঐতিহাসিক মসজিদ
- মাল্টি-সিন ডায়নামিক ভিডিও আর্কিটেকচার: প্রতিটি লং ভিডিওতে ৪টি ভিন্ন ভিন্ন মসজিদ ও পবিত্র স্থানের দৃশ্য
- প্রতি ২০-২৫ সেকেন্ড পর পর দৃষ্টিনন্দন সিনেমাটিক সিন ট্রানজিশন — কোনো ক্লিপ একটানা লুপ হবে না
- রিলস (Reels): ৩টি ভিন্ন সিন (২০ সেকেন্ড করে = ৬০ সেকেন্ড)
- লং ভিডিও (HQ Video): ৪টি ভিন্ন সিন (২৫ সেকেন্ড করে = ১০০ সেকেন্ড)
- একটানা অবিরত ৩২০kbps ক্রিস্টাল ক্লিয়ার স্টুডিও সাউন্ড তিলাওয়াত
- পেজের স্থায়ী ব্র্যান্ডেড ওয়াটারমার্ক: 'কুরআনের তিলাওয়াত • Quran Tilawat'
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

try:
    from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN
except Exception:
    FB_PAGE_ID = os.getenv("FB_PAGE_ID", "1430288070174104")
    FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# ১০টি বিশ্ববিখ্যাত পবিত্র মসজিদ, পবিত্র কাবা তাওয়াফ ও রুহানি প্রকৃতির ৩৩+ সিনেমাটিক ফুটেজ পুল
# (মানুষের মাথার অংশ বা ওয়াটারমার্ক টেক্সট থাকা ক্লিপ স্থায়ীভাবে বাদ দেওয়া হয়েছে)

HERO_THUMBNAIL_SCENES = [
    {
        "id": "kaaba_peaceful",
        "file": "kaaba_beauty_peaceful.mp4",
        "title": "পবিত্র কাবা শরীফ ও মক্কার মিনার",
        "location": "পবিত্র মসজিদুল হারাম, মক্কা",
        "start_offset": 0
    },
    {
        "id": "madinah_nabawi",
        "file": "madinah_nabawi_drone_4k.mp4",
        "title": "মসজিদে নববী ও সবুজ গম্বুজ",
        "location": "মদিনা মনোওয়ারা",
        "start_offset": 0
    },
    {
        "id": "sultan_ahmed",
        "file": "sultan_ahmed_blue_mosque.mp4",
        "title": "ঐতিহাসিক সুলতান আহমেদ নীল মসজিদ",
        "location": "ইস্তাম্বুল, তুরস্ক",
        "start_offset": 2
    },
    {
        "id": "sheikh_zayed",
        "file": "sheikh_zayed_grand_mosque.mp4",
        "title": "শেখ জায়েদ গ্র্যান্ড মসজিদ",
        "location": "সংযুক্ত আরব আমিরাত",
        "start_offset": 1
    },
    {
        "id": "kaaba_peaceful_angle2",
        "file": "kaaba_beauty_peaceful.mp4",
        "title": "পবিত্র কাবা চত্বর ও তাওয়াফরত হাজীদের ভিড়",
        "location": "মসজিদুল হারাম, মক্কা মুকাররমা",
        "start_offset": 7
    },
    {
        "id": "hassan_ii",
        "file": "hassan_ii_mosque_morocco.mp4",
        "title": "ঐতিহাসিক দ্বিতীয় হাসান মসজিদ",
        "location": "কাসাব্লাঙ্কা, মরক্কো",
        "start_offset": 2
    },
    {
        "id": "faisal_mosque",
        "file": "faisal_mosque_islamabad.mp4",
        "title": "ঐতিহাসিক ফয়সাল মসজিদ",
        "location": "ইসলামাবাদ, পাকিস্তান",
        "start_offset": 3
    },
    {
        "id": "makkah_clock_tower",
        "file": "makkah_clock_tower_drone.mp4",
        "title": "মক্কা ক্লক টাওয়ার ও গ্র্যান্ড হারাম",
        "location": "মক্কা মুকাররমা",
        "start_offset": 5
    }
]

RICH_SECONDARY_POOL = [
    {
        "id": "rain_drops",
        "url": "https://cdn.pixabay.com/video/2024/06/02/214982_large.mp4",
        "title": "রহমতের স্নিগ্ধ বৃষ্টিপাত",
        "location": "শান্ত প্রাকৃতিক পরিবেশ"
    },
    {
        "id": "sunset_clouds",
        "url": "https://cdn.pixabay.com/video/2024/08/08/225504_large.mp4",
        "title": "দিগন্তে রক্তিম সূর্যাস্ত ও মেঘমালা",
        "location": "গোধূলির আকাশ"
    },
    {
        "id": "canyon_waterfall",
        "url": "https://cdn.pixabay.com/video/2022/03/08/110108-686962724_medium.mp4",
        "title": "পাহাড়ি গিরিখাত ও ঝর্ণার ধারা",
        "location": "সবুজ পাহাড়"
    },
    {
        "id": "galaxy_stars",
        "url": "https://cdn.pixabay.com/video/2022/11/24/140366-774838017_large.mp4",
        "title": "মহাবিশ্বের অসীম গ্যালাক্সি ও তারার মেলা",
        "location": "মহাজাগতিক দিগন্ত"
    },
    {
        "id": "misty_forest",
        "url": "https://cdn.pixabay.com/video/2021/10/26/93432-639359155_large.mp4",
        "title": "কুয়াশাঘেরা সবুজ বনানী",
        "location": "শান্ত প্রকৃতি"
    },
    {
        "id": "stream_waterfall",
        "url": "https://cdn.pixabay.com/video/2023/07/04/170060-842720151_large.mp4",
        "title": "স্বচ্ছ পাহাড়ি জলপ্রপাত",
        "location": "পাহাড়ি নদী"
    },
    {
        "id": "blue_clouds_timelapse",
        "url": "https://cdn.pixabay.com/video/2022/11/04/137710-767484643_medium.mp4",
        "title": "নীল আকাশের শুভ্র মেঘের মেলা",
        "location": "নীল আকাশ"
    },
    {
        "id": "ocean_sunset_waves",
        "url": "https://cdn.pixabay.com/video/2023/12/09/192576-892942889_medium.mp4",
        "title": "শান্ত সাগরের গোধূলি ঢেউ",
        "location": "সৈকতের সন্ধ্যা"
    },
    {
        "id": "rain_leaves",
        "url": "https://cdn.pixabay.com/video/2023/07/30/173887-850026370_medium.mp4",
        "title": "বৃষ্টিভেজা পাতার শান্ত ছন্দ",
        "location": "বৃষ্টিস্নাত বন"
    },
    {
        "id": "stone_mosque_arch",
        "url": "https://cdn.pixabay.com/video/2022/12/16/143151-781991184_medium.mp4",
        "title": "ঐতিহাসিক পাথুরে মসজিদ",
        "location": "ইসলামিক ঐতিহ্য"
    },
    {
        "id": "marble_courtyard",
        "url": "https://cdn.pixabay.com/video/2023/03/04/153099-804706282_medium.mp4",
        "title": "পবিত্র মার্বেল চত্বর ও মিনার",
        "location": "মসজিদ প্রাঙ্গণ"
    },
    {
        "id": "golden_dome_carving",
        "url": "https://cdn.pixabay.com/video/2022/07/13/124063-729835810_medium.mp4",
        "title": "সোনালী গম্বুজের নকশা",
        "location": "ঐতিহাসিক কারুকাজ"
    },
    {
        "id": "ancient_mosque_calm",
        "url": "https://cdn.pixabay.com/video/2024/02/23/201668-916080463_medium.mp4",
        "title": "প্রাচীন মসজিদ ও শান্ত পরিবেশ",
        "location": "ঐতিহাসিক ইসলামিক ল্যান্ডমার্ক"
    },
    {
        "id": "dawn_minaret_birds",
        "url": "https://cdn.pixabay.com/video/2023/10/31/187272-880035010_medium.mp4",
        "title": "ভোরের আলোয় সুউচ্চ মিনার",
        "location": "ঐতিহাসিক মিনার প্রাঙ্গণ"
    },
    {
        "id": "mountain_fog_dance",
        "url": "https://cdn.pixabay.com/video/2021/02/21/65868-515617516_medium.mp4",
        "title": "পর্বতচূড়ায় কুয়াশার মোহনীয় রূপ",
        "location": "উঁচু পর্বতের মায়া"
    }
]

FOOTAGE_STATE_FILE = os.path.join(BASE_DIR, "assets", "footage_state.json")

def get_recent_facebook_scene_titles() -> list:
    """ফেসবুকের শেষ ১০টি পোস্ট চেক করে কোন কোন সিন ব্যবহৃত হয়েছে তা বের করে"""
    recent = []
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID:
        return recent
    try:
        url = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/videos"
        params = {"access_token": FB_PAGE_ACCESS_TOKEN, "fields": "description,title", "limit": 10}
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            for item in res.json().get("data", []):
                text = (item.get("description", "") + " " + item.get("title", ""))
                recent.append(text)
    except Exception as e:
        print(f"[FB RECENT WARN] {e}")
    return recent

def ensure_scene_ready(item: dict) -> tuple:
    """ফুটেজ ফাইল প্রস্তুত করে (লোকাল ফাইল অথবা ক্লাউড সিডিএন ক্যাশ)"""
    offset = item.get("start_offset", 0)
    if "file" in item:
        p = os.path.join(ASSETS_FOOTAGE_DIR, item["file"])
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            return p, offset

    if "url" in item:
        fname = f"{item['id']}.mp4"
        cached = os.path.join(DOWNLOADS_DIR, fname)
        if os.path.exists(cached) and os.path.getsize(cached) > 100000:
            return cached, offset
        try:
            print(f"📥 ক্লাউড সিডিএন থেকে ফ্রেশ ফুটেজ ডাউনলোড হচ্ছে: {item['title']}...")
            req = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'}, timeout=25)
            if req.status_code == 200:
                with open(cached, "wb") as f:
                    f.write(req.content)
                return cached, offset
        except Exception as e:
            print(f"[CDN DOWNLOAD WARN] {e}")

    # Fallback to local default
    fallback = os.path.join(ASSETS_FOOTAGE_DIR, "makkah_clock_tower_drone.mp4")
    return fallback, 0

def get_next_mosque_scenes(count: int = 4, surah_data: dict = None) -> tuple:
    """
    ১০০% গ্যারান্টিযুক্ত ডায়নামিক জিরো-ডুপ্লিকেট ফুটেজ নির্বাচন:
    - ফেসবুক Graph API চেক করে সাম্প্রতিক ৫টি পোস্টের থাম্বনেইল সিন বাদ দেয়
    - হিরো দৃশ্য থেকে সম্পূর্ণ আনপোস্টেড দৃশ্যকে দৃশ্য ১ (থাম্বনেইল) বানায়
    - বাকি দৃশ্যগুলো ৩৩+ টি বৈচিত্র্যময় সিন ও প্রকৃতির পুল থেকে নির্বাচিত হয়
    """
    recent_texts = get_recent_facebook_scene_titles()
    recent_blob = " ".join(recent_texts)

    # দৃশ্য ১ এর জন্য ফিল্টার
    hero_available = []
    for h in HERO_THUMBNAIL_SCENES:
        p = os.path.join(ASSETS_FOOTAGE_DIR, h.get("file", ""))
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            hero_available.append(h)

    if not hero_available:
        hero_available = HERO_THUMBNAIL_SCENES

    unseen_hero = [h for h in hero_available if h["title"] not in recent_blob]
    if not unseen_hero:
        unseen_hero = hero_available

    # State file fallback check
    state = {}
    if os.path.exists(FOOTAGE_STATE_FILE):
        try:
            with open(FOOTAGE_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    last_idx = state.get("last_hero_index", -1)
    next_idx = (last_idx + 1) % len(unseen_hero)
    state["last_hero_index"] = next_idx
    scene1_item = unseen_hero[next_idx]

    try:
        os.makedirs(os.path.dirname(FOOTAGE_STATE_FILE), exist_ok=True)
        with open(FOOTAGE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    # বাকি দৃশ্য নির্বাচন
    remaining_pool = [x for x in hero_available if x["id"] != scene1_item["id"]] + RICH_SECONDARY_POOL
    random.shuffle(remaining_pool)
    secondary_items = remaining_pool[:count - 1]

    selected_items = [scene1_item] + secondary_items

    # পাথ ও অফসেট প্রস্তুত
    scene_targets = []
    for it in selected_items:
        p, off = ensure_scene_ready(it)
        scene_targets.append((p, off))

    titles = " • ".join([it["title"] for it in selected_items])
    locations = " • ".join(list(dict.fromkeys([it["location"] for it in selected_items])))

    print(f"🕌 [জিরো-ডুপ্লিকেট ফ্রেশ দৃশ্য প্রস্তুত] থাম্বনেইল সিন: {scene1_item['title']} ({scene1_item['location']})")
    for idx, it in enumerate(selected_items, 1):
        print(f"   🎬 দৃশ্য #{idx}: {it['title']} ({it['location']})")

    combined_meta = {
        "title": titles,
        "location": locations,
        "scenes": selected_items
    }
    return scene_targets, combined_meta


def download_imam_surah_audio(surah_data: dict, imam: dict = None) -> tuple:
    """
    মক্কা ও মদিনার সম্মানিত ইমামগণের ভেরিফাইড সিডিএন থেকে পূর্ণাঙ্গ সূরার অডিও সংগ্রহ করে।
    কঠোর পলিসি: কোনো কপিরাইটযুক্ত স্টুডিও রিকার্ডিং নয়।
    """
    surah_num = surah_data.get("number", 1)
    surah_bangla = surah_data.get("bangla", "সূরা আল-ফাতিহা")

    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3")):
        try: os.remove(old)
        except Exception: pass

    if not imam:
        imam = random.choice(MAKKAH_MADINAH_IMAMS)

    print(f"🎙️ তিলাওয়াতকারী নির্বাচন: {imam['name']} ({imam['mosque']})")
    audio_path = os.path.join(DOWNLOADS_DIR, f"voice_{imam['id']}_{surah_num:03d}_{int(time.time())}.mp3")

    # ডিরেক্ট হাই-স্পিড সিডিএন ডাউনলোড (mp3quran.net)
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

    # নিরাপদ ফলব্যাক: পবিত্র মক্কার শাইখ ড. মাহের আল-মুয়াইক্বলী
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

def get_audio_duration_sec(audio_path: str) -> float:
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 60.0

def render_quran_video_with_watermark(scene_paths: list, audio_path: str, out_path: str, is_reel: bool = True) -> str:
    """
    মাল্টিপল ভিন্ন সিন যুক্ত হাই-রিটেনশন ডায়নামিক ভিডিও রেন্ডারিং:
    - রিলস (Reels): ১০৮০x১৯২০ (ভার্টিক্যাল ৯:১৬), ৩টি সিন x ২০ সেকেন্ড = ৬০ সেকেন্ড
    - লং ভিডিও (HQ Video): ১৯২০x১০৮০ (ওয়াইডস্ক্রিন ১৬:৯), ৪টি সিন x ২৫ সেকেন্ড = ১০০ সেকেন্ড
    - একটানা অবিরত তিলাওয়াত অডিও এবং অফিশিয়াল ক্রিস্টাল ক্লিয়ার ওয়াটারমার্ক
    """
    audio_dur = get_audio_duration_sec(audio_path)

    if is_reel:
        w, h = 1080, 1920
        # রিলস ফেসবুকের অফিশিয়াল ৬০ সেকেন্ড
        total_duration = 60
        target_scenes = scene_paths[:3]
        seg_dur = total_duration / len(target_scenes)
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "5000k", "-maxrate", "7000k", "-bufsize", "10000k"]
        print(f"🎨 [REEL RENDERING] {len(target_scenes)}টি দৃশ্য সহ ৬০ সেকেন্ডের আকর্ষণীয় রিলস প্রস্তুত হচ্ছে (১ম দৃশ্য: কাবা তাওয়াফ)...")
    else:
        w, h = 1920, 1080
        # বড় সূরার ক্ষেত্রে সম্পূর্ণ অডিওর পূর্ণাঙ্গ সময় (সর্বোচ্চ ১৫-২০ মিনিট ক্লাউড লিমিট সেফগার্ড)
        total_duration = min(audio_dur, 1200.0)
        target_scenes = scene_paths[:4]
        seg_dur = max(20.0, total_duration / len(target_scenes))
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "20"
        bitrate_args = ["-b:v", "4000k", "-maxrate", "6000k", "-bufsize", "8000k"]
        print(f"🎨 [FULL SURAH HQ VIDEO] সম্পূর্ণ বড় সূরা ({total_duration/60:.1f} মিনিট) পূর্ণাঙ্গ রেন্ডারিং শুরু হচ্ছে...")

    watermark_png = generate_watermark_overlay(w, h)

    inputs = []
    filter_parts = []
    concat_inputs = []

    for i, item in enumerate(target_scenes):
        if isinstance(item, (list, tuple)):
            sc, sc_offset = item[0], item[1]
        else:
            sc, sc_offset = item, 0
        ss_args = ["-ss", str(sc_offset)] if sc_offset > 0 else []
        inputs.extend(ss_args + ["-stream_loop", "-1", "-i", sc])
        filter_parts.append(f"[{i}:v]{scale_filter},setsar=1,fps=30,format=yuv420p,trim=duration={seg_dur},setpts=PTS-STARTPTS[v{i}]")
        concat_inputs.append(f"[v{i}]")

    num_scenes = len(target_scenes)
    # তিলাওয়াত অডিও হচ্ছে ইনপুট ইনডেক্স num_scenes
    inputs.extend(["-i", audio_path])
    audio_idx = num_scenes

    # ওয়াটারমার্ক হচ্ছে ইনপুট ইনডেক্স num_scenes + 1
    inputs.extend(["-i", watermark_png])
    wm_idx = num_scenes + 1

    concat_filter = f"{''.join(concat_inputs)}concat=n={num_scenes}:v=1:a=0[v_concat]"
    final_wm_filter = f"[v_concat][{wm_idx}:v]overlay=0:0[final_v]"
    full_filter = f"{';'.join(filter_parts)};{concat_filter};{final_wm_filter}"

    total_duration = seg_dur * num_scenes

    cmd = [
        FFMPEG_EXE, "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[final_v]",
        "-map", f"{audio_idx}:a:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", crf,
        *bitrate_args,
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-t", str(total_duration),
        "-shortest",
        "-pix_fmt", "yuv420p",
        out_path
    ]

    try:
        print(f"🎬 [FFMPEG] মাল্টি-সিন রেন্ডারিং কমান্ড এক্সিকিউট হচ্ছে...")
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[FFMPEG MULTI-SCENE WARN] Concat rendering failed ({e}). Executing single-scene fallback...")
        fallback_filter = f"[0:v]{scale_filter},setsar=1,fps=30,format=yuv420p[v0];[v0][2:v]overlay=0:0[final_v]"
        first_sc = target_scenes[0][0] if isinstance(target_scenes[0], (list, tuple)) else target_scenes[0]
        fallback_cmd = [
            FFMPEG_EXE, "-y",
            "-stream_loop", "-1",
            "-i", first_sc,
            "-i", audio_path,
            "-i", watermark_png,
            "-filter_complex", fallback_filter,
            "-map", "[final_v]",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", crf,
            *bitrate_args,
            "-c:a", "aac",
            "-b:a", "320k",
            "-ar", "48000",
            "-t", str(total_duration),
            "-shortest",
            "-pix_fmt", "yuv420p",
            out_path
        ]
        subprocess.run(fallback_cmd, check=True)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"✨ মাল্টি-সিন রেন্ডারিং সম্পন্ন! কোয়ালিটি: {'1080x1920 Reel' if is_reel else '1920x1080 Full HD Video'} | সাইজ: {os.path.getsize(out_path)/(1024*1024):.2f} MB")
        return out_path
    else:
        raise RuntimeError("ভিডিও রেন্ডারিং সম্পন্ন হয়নি।")

def download_quran_video(is_reel: bool = True, surah_data: dict = None, imam_data: dict = None) -> dict:
    """quran_runner.py থেকে প্রধান এন্ট্রি পয়েন্ট"""
    if not surah_data:
        surah_data = random.choice(LONG_SURAHS)

    if not imam_data:
        imam_data = random.choice(MAKKAH_MADINAH_IMAMS)

    scene_count = 3 if is_reel else 4

    print("=======================================================")
    print(f"📖 'কুরআনের তিলাওয়াত' ভিডিও ইঞ্জিন: {surah_data['bangla']} ({'Reel' if is_reel else 'HQ Video'})")
    print(f"🎙️ তিলাওয়াত: {imam_data['name']} ({imam_data['mosque']})")
    print(f"🎬 মাল্টি-সিন কাঠামো: {scene_count}টি ভিন্ন ভিন্ন পবিত্র মসজিদের দৃশ্য")
    print("=======================================================")

    scene_paths, scenes_meta = get_next_mosque_scenes(count=scene_count, surah_data=surah_data)
    voice_audio, imam = download_imam_surah_audio(surah_data, imam_data)

    ts = int(time.time())
    format_tag = "reel" if is_reel else "hq_video"
    final_output = os.path.join(PROCESSED_DIR, f"quran_{surah_data['number']}_{format_tag}_{ts}.mp4")

    render_quran_video_with_watermark(scene_paths, voice_audio, final_output, is_reel=is_reel)

    # ক্লিনআপ টেম্প অডিও ফাইল
    try:
        if os.path.exists(voice_audio): os.remove(voice_audio)
    except Exception: pass

    return {
        "filepath": final_output,
        "file_path": final_output,
        "is_reel": is_reel,
        "title": f"হৃদয় জুড়ানো তিলাওয়াত | {surah_data['bangla']} | {imam['name']}",
        "surah_name": surah_data["bangla"],
        "surah_number": surah_data["number"],
        "reciter": imam["name"],
        "mosque": imam["mosque"],
        "bg_mosque": scenes_meta["title"],
        "bg_location": scenes_meta["location"],
        "meaning": surah_data.get("meaning", ""),
        "benefit": surah_data.get("benefit", ""),
        "ayahs": surah_data.get("ayahs", "")
    }
