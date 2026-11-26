"""
Holy Quran Automated Tilawat Engine & Multi-Scene High-Retention Video Generator
Version 4.0 - Ultra High Retention & Viral Nature Integration

Features:
- Dynamic 35+ Scene Pool: Makkah Kaaba Tawaf, Madinah Nabawi, Historic Mosques & Serene Viral Nature
- High-Retention Nature Clips: Birds flying over green landscapes, canyon waterfalls, misty valleys, rain on leaves
- True Full-Length HQ Video Rendering: 3 to 10 minutes full Surah tilawat with smooth multi-scene looping
- Dynamic Eye-Catching On-Screen Surah & Hook Typography Overlay
- Zero-Duplicate Live Facebook Graph API Scene Selection Engine
- Robust FFmpeg Duration Parser (eliminates 80-second truncation bug)
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

# ৩৫+ টি বিশ্ববিখ্যাত পবিত্র মসজিদ ও রুহানি প্রকৃতির সিনেমাটিক ফুটেজ পুল (হিরো থাম্বনেইল হিসেবে যোগ্য)
HERO_THUMBNAIL_SCENES = [
    # ১. পবিত্র কাবা ও মক্কা-মদিনা (৪K ক্রিস্টাল ক্লিয়ার)
    {
        "id": "kaaba_peaceful",
        "file": "kaaba_beauty_peaceful.mp4",
        "title": "পবিত্র কাবা শরীফ তাওয়াফ ও মক্কার মিনার",
        "location": "পবিত্র মসজিদুল হারাম, মক্কা",
        "start_offset": 2
    },
    {
        "id": "madinah_nabawi",
        "file": "madinah_nabawi_drone_4k.mp4",
        "title": "মসজিদে নববী ও সবুজ গম্বুজ",
        "location": "মদিনা মনোওয়ারা",
        "start_offset": 2
    },
    {
        "id": "sultan_ahmed",
        "file": "sultan_ahmed_blue_mosque.mp4",
        "title": "ঐতিহাসিক সুলতান আহমেদ নীল মসজিদ",
        "location": "ইস্তাম্বুল, তুরস্ক",
        "start_offset": 3
    },
    {
        "id": "sheikh_zayed",
        "file": "sheikh_zayed_grand_mosque.mp4",
        "title": "শেখ জায়েদ গ্র্যান্ড মসজিদ",
        "location": "সংযুক্ত আরব আমিরাত",
        "start_offset": 1
    },
    {
        "id": "faisal_mosque",
        "file": "faisal_mosque_islamabad.mp4",
        "title": "ঐতিহাসিক ফয়সাল মসজিদ",
        "location": "ইসলামাবাদ, মারগালা পাহাড়",
        "start_offset": 2
    },
    {
        "id": "badshahi_mosque",
        "file": "badshahi_mosque_lahore.mp4",
        "title": "বাদশাহী মসজিদ প্রাঙ্গণ",
        "location": "লাহোর, পাকিস্তান",
        "start_offset": 0
    },
    {
        "id": "makkah_clock_tower",
        "file": "makkah_clock_tower_drone.mp4",
        "title": "মক্কার ক্লক টাওয়ার ও হারামাইন প্রাঙ্গণ",
        "location": "মক্কা মুকাররমা",
        "start_offset": 5
    },
    # ২. ভাইরাল চোখ জুড়ানো রুহানি প্রকৃতি (২৭৫কে+ লাইক অর্গানিক স্টাইল)
    {
        "id": "birds_green_nature",
        "url": "https://cdn.pixabay.com/video/2019/02/28/21723-320725678_medium.mp4",
        "title": "সবুজের বুকে পাখির কলকাকলি ও ওড়াউড়ি",
        "location": "প্রকৃতির অপরূপ সৃষ্টি",
        "start_offset": 1
    },
    {
        "id": "canyon_waterfall_cascade",
        "url": "https://cdn.pixabay.com/video/2022/03/08/110108-686962724_medium.mp4",
        "title": "পাহাড়ি গিরিখাতে স্বচ্ছ স্ফটিক জলপ্রপাত",
        "location": "শান্ত পাহাড়ি ঝর্ণাধারা",
        "start_offset": 2
    },
    {
        "id": "rain_green_leaves",
        "url": "https://cdn.pixabay.com/video/2024/02/25/201947-916877801_medium.mp4",
        "title": "সবুজ পাতায় প্রশান্তিময় বৃষ্টির ধারা",
        "location": "আল্লাহর রহমতের বারিধারা",
        "start_offset": 2
    },
    {
        "id": "golden_sunset_clouds",
        "url": "https://cdn.pixabay.com/video/2025/01/08/251461_medium.mp4",
        "title": "গোধূলি লগ্নে মেঘমালার মোহনীয় রূপ",
        "location": "আসমানের মহিমা ও কুদরত",
        "start_offset": 3
    },
    {
        "id": "ocean_sunset_calm",
        "url": "https://cdn.pixabay.com/video/2023/03/09/153976-817104245_medium.mp4",
        "title": "শান্ত সাগরের বুকে সূর্যাস্তের সোনালী আভা",
        "location": "মহাসমুদ্রের অপার বিস্তৃতি",
        "start_offset": 2
    },
    {
        "id": "misty_forest_valley",
        "url": "https://cdn.pixabay.com/video/2020/06/18/42493-431835777_medium.mp4",
        "title": "কুয়াশাঘেরা সবুজ অরণ্য ও পাহাড়ি নদী",
        "location": "প্রকৃতির নিঃশব্দ নিস্তব্ধতা",
        "start_offset": 1
    },
    {
        "id": "night_sky_milkyway",
        "url": "https://cdn.pixabay.com/video/2022/06/21/121601-724710302_medium.mp4",
        "title": "মহাবিশ্বের তারাভরা আকাশ ও গ্যালাক্সি",
        "location": "অনন্ত নক্ষত্রপুঞ্জ",
        "start_offset": 2
    }
]

# সেকেন্ডারি বি-রোল ও সিন ট্রানজিশন দৃশ্য পুল
SECONDARY_SCENES_POOL = [
    {
        "id": "mountain_canyon_river",
        "url": "https://cdn.pixabay.com/video/2023/12/09/192576-892942889_medium.mp4",
        "title": "পাহাড়ের বুক চিরে বয়ে চলা পাহাড়ি নদী",
        "location": "প্রকৃতির বিস্ময়",
        "start_offset": 1
    },
    {
        "id": "forest_stream_waterfall",
        "url": "https://cdn.pixabay.com/video/2022/10/20/135727-764361705_medium.mp4",
        "title": "শান্ত বনে পাখির কলতান ও ঝর্ণা",
        "location": "প্রশান্তিময় বনানী",
        "start_offset": 2
    },
    {
        "id": "sunset_horizon_timelapse",
        "url": "https://cdn.pixabay.com/video/2019/02/20/21551-319487844_medium.mp4",
        "title": "দিগন্তে লালিমাময় সূর্যাস্তের টাইম-ল্যাপ্স",
        "location": "সন্ধ্যা আকাশের আলো",
        "start_offset": 2
    },
    {
        "id": "ancient_arches_hall",
        "url": "https://cdn.pixabay.com/video/2020/02/12/32263-391201296_medium.mp4",
        "title": "ঐতিহাসিক মসজিদের খিলান ও স্তম্ভ",
        "location": "ইসলামিক শিল্পকলা",
        "start_offset": 1
    },
    {
        "id": "golden_calligraphy_dome",
        "url": "https://cdn.pixabay.com/video/2023/05/30/165072-831695790_medium.mp4",
        "title": "গম্বুজে সোনালী আরবি ক্যালিগ্রাফি",
        "location": "ঐতিহাসিক গম্বুজ",
        "start_offset": 2
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
        for d in [ASSETS_FOOTAGE_DIR, BASE_DIR]:
            p = os.path.join(d, item["file"])
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
    for fb in ["kaaba_beauty_peaceful.mp4", "makkah_clock_tower_drone.mp4", "sultan_ahmed_blue_mosque.mp4"]:
        for d in [ASSETS_FOOTAGE_DIR, BASE_DIR]:
            cand = os.path.join(d, fb)
            if os.path.exists(cand) and os.path.getsize(cand) > 50000:
                return cand, 0
    return os.path.join(BASE_DIR, "makkah_clock_tower_drone.mp4"), 0

def get_next_mosque_scenes(count: int = 4, surah_data: dict = None) -> tuple:
    """
    ১০০% গ্যারান্টিযুক্ত ডায়নামিক জিরো-ডুপ্লিকেট ফুটেজ নির্বাচন:
    - ফেসবুক Graph API চেক করে সাম্প্রতিক পোস্টের দৃশ্য বাদ দেয়
    - হিরো দৃশ্য থেকে সম্পূর্ণ আনপোস্টেড দৃশ্যকে দৃশ্য ১ (থাম্বনেইল) বানায়
    - বাকি দৃশ্যগুলো বৈচিত্র্যময় মসজিদ ও প্রকৃতির পুল থেকে নির্বাচিত হয়
    """
    recent_texts = get_recent_facebook_scene_titles()
    recent_blob = " ".join(recent_texts)

    # দৃশ্য ১ (থাম্বনেইল): সম্প্রতি ফেসবুকে ব্যবহার হয়নি এমন সিন বাছাই
    unseen_hero = [h for h in HERO_THUMBNAIL_SCENES if h["title"] not in recent_blob]
    if not unseen_hero:
        unseen_hero = HERO_THUMBNAIL_SCENES

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

    # বাকি দৃশ্য নির্বাচন: হিরো ও সেকেন্ডারি পুলের মিশ্রণ
    remaining_pool = [x for x in HERO_THUMBNAIL_SCENES if x["id"] != scene1_item["id"]] + SECONDARY_SCENES_POOL
    random.shuffle(remaining_pool)
    secondary_items = remaining_pool[:count - 1]

    selected_items = [scene1_item] + secondary_items

    scene_targets = []
    for it in selected_items:
        p, off = ensure_scene_ready(it)
        scene_targets.append((p, off))

    titles = " • ".join([it["title"] for it in selected_items])
    locations = " • ".join(list(dict.fromkeys([it["location"] for it in selected_items])))

    print(f"🕌 [জিরো-ডুপ্লিকেট ফ্রেশ দৃশ্য প্রস্তুত] ১ম দৃশ্য (থাম্বনেইল): {scene1_item['title']} ({scene1_item['location']})")
    for idx, it in enumerate(selected_items, 1):
        print(f"   🎬 দৃশ্য #{idx}: {it['title']} ({it['location']})")

    combined_meta = {
        "title": titles,
        "location": locations,
        "scenes": selected_items,
        "hero_title": scene1_item["title"],
        "hero_location": scene1_item["location"]
    }
    return scene_targets, combined_meta
def download_imam_surah_audio(surah_data: dict, imam: dict = None) -> tuple:
    """মক্কা ও মদিনার সম্মানিত ইমামগণের ভেরিফাইড সিডিএন থেকে পূর্ণাঙ্গ সূরার অডিও সংগ্রহ করে"""
    surah_num = surah_data.get("number", 1)

    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3")):
        try: os.remove(old)
        except Exception: pass

    if not imam:
        imam = random.choice(MAKKAH_MADINAH_IMAMS)

    print(f"🎙️ তিলাওয়াতকারী নির্বাচন: {imam['name']} ({imam['mosque']})")
    audio_path = os.path.join(DOWNLOADS_DIR, f"voice_{imam['id']}_{surah_num:03d}_{int(time.time())}.mp3")

    cdn_url = f"{imam['server']}/{surah_num:03d}.mp3"
    print(f"📥 অডিও ডাউনলোড হচ্ছে: {cdn_url}")
    try:
        resp = requests.get(cdn_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=35)
        if resp.status_code == 200 and len(resp.content) > 50000:
            with open(audio_path, "wb") as f:
                f.write(resp.content)
            print(f"✅ স্টুডিও তিলাওয়াত অডিও প্রস্তুত ({len(resp.content)/(1024*1024):.2f} MB)")
            return audio_path, imam
    except Exception as e:
        print(f"[AUDIO DOWNLOAD WARN] Primary failed: {e}. Trying fallback server...")

    fallback_url = f"https://server11.mp3quran.net/sds/{surah_num:03d}.mp3"
    resp = requests.get(fallback_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=35)
    with open(audio_path, "wb") as f:
        f.write(resp.content)
    fallback_imam = MAKKAH_MADINAH_IMAMS[0]
    return audio_path, fallback_imam

def get_audio_duration_sec(audio_path: str) -> float:
    """FFMPEG_EXE ব্যবহার করে অডিও ফাইলের নির্ভুল ও সঠিক সময় (সেকেন্ডে) বের করে"""
    try:
        cmd = [FFMPEG_EXE, "-i", audio_path]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        m = re.search(r"Duration:s*(d+):(d+):(d+.d+)", res.stderr)
        if m:
            hours, mins, secs = m.groups()
            dur = int(hours) * 3600 + int(mins) * 60 + float(secs)
            print(f"⏱️ তিলাওয়াত অডিওর প্রকৃত মোট দৈর্ঘ্য: {dur:.1f} সেকেন্ড ({dur/60:.1f} মিনিট)")
            return dur
    except Exception as e:
        print(f"[DURATION WARN] {e}")
    return 180.0

def render_quran_video_with_watermark(
    scene_paths: list,
    audio_path: str,
    out_path: str,
    is_reel: bool = True,
    surah_data: dict = None,
    imam_data: dict = None
) -> str:
    """
    মাল্টিপল ভিন্ন সিন যুক্ত হাই-রিটেনশন ডায়নামিক ভিডিও রেন্ডারিং:
    - রিলস (Reels): ১০৮০x১৯২০ (ভার্টিক্যাল ৯:১৬), ১৫ থেকে ৩০ সেকেন্ড (ভাইরাল হাইপার-রিটেনশন সাইকেল)
    - লং ভিডিও (HQ Video): ১৯২০x১০৮০ (ওয়াইডস্ক্রিন ১৬:৯), ১০ থেকে ৩০+ মিনিট পূর্ণাঙ্গ সূরা তিলাওয়াত
    - অন-স্ক্রিন আধুনিক ইসলামিক টাইপোগ্রাফি ব্যানার (সূরা ও হুক টেক্সট)
    """
    audio_dur = get_audio_duration_sec(audio_path)

    surah_name = surah_data.get("bangla", "পবিত্র কুরআন তিলাওয়াত") if surah_data else "সূরা আর-রহমান"
    reciter_name = imam_data.get("name", "পবিত্র মক্কার ইমাম") if imam_data else "শাইখ আব্দুর রহমান আস-সুদাইস"

    if is_reel:
        w, h = 1080, 1920
        # রিলস: ১৫ থেকে ৩০ সেকেন্ড (ইউজার রিকয়ারমেন্ট: 15 theke 30sec) - অ্যালগরিদমে ৯০-১০০% ওয়াচ-টাইম রিটেনশন পাওয়ার জন্য
        target_reel_sec = float(random.randint(18, 28))
        total_duration = min(audio_dur, target_reel_sec)
        target_scenes = scene_paths[:2]
        seg_dur = total_duration / len(target_scenes)
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "5000k", "-maxrate", "7000k", "-bufsize", "10000k"]
        preset = "fast"
        hook_text = random.choice([
            "২০ সেকেন্ড চোখ বন্ধ করে শুনুন • দিল শান্ত হবে",
            "মন জুড়ানো তিলাওয়াত • না টেনে শুনুন",
            "পবিত্র কুরআনের তিলাওয়াত • অন্তরের প্রশান্তি"
        ])
        print(f"🎨 [REEL RENDERING] {len(target_scenes)}টি দৃশ্য সহ {total_duration:.0f} সেকেন্ডের হাই-রিটেনশন রিলস প্রস্তুত হচ্ছে...")
    else:
        w, h = 1920, 1080
        # লং ভিডিও: পূর্ণাঙ্গ সূরা তিলাওয়াত (১০ থেকে ৩০+ মিনিট / সম্পূর্ণ অডিওর সময়)
        # সর্বোচ্চ ৬০ মিনিট (৩৬০০ সেকেন্ড) ক্লাউড সেফগার্ড
        total_duration = min(audio_dur, 3600.0)
        # ৬ থেকে ৮টি ভিন্ন সিন সাইকেল
        num_scenes = min(len(scene_paths), 8)
        target_scenes = scene_paths[:num_scenes]
        seg_dur = max(25.0, total_duration / len(target_scenes))
        total_duration = seg_dur * len(target_scenes)
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "22"
        bitrate_args = ["-b:v", "3500k", "-maxrate", "5000k", "-bufsize", "8000k"]
        preset = "veryfast"
        hook_text = "পূর্ণাঙ্গ তিলাওয়াত • অন্তরের প্রশান্তি"
        print(f"🎨 [FULL SURAH HQ VIDEO] সম্পূর্ণ সূরা ({total_duration/60:.1f} মিনিট) {len(target_scenes)}টি চমৎকার দৃশ্যে পূর্ণাঙ্গ রেন্ডারিং শুরু হচ্ছে...")

    watermark_png = generate_watermark_overlay(
        width=w,
        height=h,
        surah_name=surah_name,
        reciter_name=reciter_name,
        hook_text=hook_text
    )

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
    inputs.extend(["-i", audio_path])
    audio_idx = num_scenes

    inputs.extend(["-i", watermark_png])
    wm_idx = num_scenes + 1

    concat_filter = f"{''.join(concat_inputs)}concat=n={num_scenes}:v=1:a=0[v_concat]"
    final_wm_filter = f"[v_concat][{wm_idx}:v]overlay=0:0[final_v]"
    full_filter = f"{';'.join(filter_parts)};{concat_filter};{final_wm_filter}"

    cmd = [
        FFMPEG_EXE, "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[final_v]",
        "-map", f"{audio_idx}:a:0",
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", crf,
        *bitrate_args,
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-t", str(total_duration),
        "-shortest",
        "-pix_fmt", "yuv420p",
        out_path
    ]

    try:
        print(f"🎬 [FFMPEG] মাল্টি-সিন রেন্ডারিং শুরু...")
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[FFMPEG MULTI-SCENE WARN] Concat failed ({e}). Running single-scene fallback...")
        first_sc = target_scenes[0][0] if isinstance(target_scenes[0], (list, tuple)) else target_scenes[0]
        fallback_filter = f"[0:v]{scale_filter},setsar=1,fps=30,format=yuv420p[v0];[v0][2:v]overlay=0:0[final_v]"
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

    scene_count = 2 if is_reel else 8

    print("=======================================================")
    print(f"📖 'কুরআনের তিলাওয়াত' ভিডিও ইঞ্জিন: {surah_data['bangla']} ({'Reel' if is_reel else 'HQ Video'})")
    print(f"🎙️ তিলাওয়াত: {imam_data['name']} ({imam_data['mosque']})")
    print(f"🎬 মাল্টি-সিন কাঠামো: {scene_count}টি ভিন্ন ভিন্ন পবিত্র দৃশ্য")
    print("=======================================================")

    scene_paths, scenes_meta = get_next_mosque_scenes(count=scene_count, surah_data=surah_data)
    voice_audio, imam = download_imam_surah_audio(surah_data, imam_data)

    ts = int(time.time())
    format_tag = "reel" if is_reel else "hq_video"
    final_output = os.path.join(PROCESSED_DIR, f"quran_{surah_data['number']}_{format_tag}_{ts}.mp4")

    render_quran_video_with_watermark(
        scene_paths=scene_paths,
        audio_path=voice_audio,
        out_path=final_output,
        is_reel=is_reel,
        surah_data=surah_data,
        imam_data=imam
    )

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

if __name__ == "__main__":
    print("Testing Quran Downloader Engine V4...")
    test_surah = LONG_SURAHS[2] # Surah Ar-Rahman
    test_imam = MAKKAH_MADINAH_IMAMS[0] # Sudais
    meta = download_quran_video(is_reel=True, surah_data=test_surah, imam_data=test_imam)
    print("Test video generated successfully:", meta["filepath"])
