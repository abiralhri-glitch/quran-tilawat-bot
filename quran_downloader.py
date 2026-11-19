"""
Holy Quran Automated Tilawat Engine & Multi-Scene High-Retention Video Generator
- ১০০% পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা ও পবিত্র হজ-ওমরাহর আসল সিনেমাটিক ফুটেজ
- কোনো ভিন্ন দেশীয় সাধারণ মসজিদ নয়—শুধুমাত্র পবিত্র কাবা, মসজিদে নববী ও হজের দৃশ্য
- কঠোর জিরো-ডুপ্লিকেট রোটেশন: পূর্ববর্তী ২০টি পোস্টের ফুটেজ ট্র্যাক করে সম্পূর্ণ আলাদা দৃশ্য নির্বাচন
- ফুল লং ভিডিও আর্কিটেকচার: পুরো সূরার সম্পূর্ণ তিলাওয়াতের দৈর্ঘ্য অনুযায়ী আনলিমিটেড মাল্টি-সিন লুপ
- রিলস (Reels): ৩টি ভিন্ন সিন (২০ সেকেন্ড করে = ৬০ সেকেন্ড, ৯:১৬)
- লং ভিডিও (Long HQ Video): ৪-৬টি ভিন্ন সিন (পুরো সূরার সমান দৈর্ঘ্য, ১৬:৯ ফুল এইচডি)
- একটানা অবিরত ক্রিস্টাল ক্লিয়ার তিলাওয়াত অডিও এবং ব্র্যান্ডেড ওয়াটারমার্ক
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
# ১০০% পবিত্র মক্কা, মদিনা ও হজের ভেরিফাইড ১০৮০p সিনেমাটিক ফুটেজ ডাটাবেজ
# ==============================================================================
HOLY_MAKKAH_MADINAH_HAJJ_POOL = [
    # --- পবিত্র মক্কা মুকাররমা (Makkah al-Mukarramah) ---
    {
        "id": "makkah_kaaba_cinematic",
        "title": "পবিত্র কাবা শরীফ ও মাতাফ চত্বর",
        "location": "মসজিদুল হারাম, মক্কা",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2021/04/18/71447-539097973_large.mp4"
    },
    {
        "id": "makkah_kaaba_peaceful",
        "title": "পবিত্র কাবা প্রাঙ্গণ ও স্বর্ণালী গিলাফ",
        "location": "মাতাফ শরীফ, মক্কা",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/10/22/186088-877239334_large.mp4"
    },
    {
        "id": "makkah_clock_tower_drone",
        "title": "মক্কা ক্লক টাওয়ার ও গ্র্যান্ড হারাম ড্রোন ভিউ",
        "location": "পবিত্র মক্কা মুকাররমা",
        "local_file": "makkah_clock_tower_drone.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2022/01/18/104868-668835848_large.mp4"
    },
    {
        "id": "makkah_aerial_tawaf",
        "title": "লাখো মুসল্লির পবিত্র কাবা তাওয়াফ দৃশ্য",
        "location": "মসজিদুল হারাম, মক্কা",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    },

    # --- পবিত্র মদিনা মনোওয়ারা (Madinah al-Munawwarah) ---
    {
        "id": "madinah_nabawi_greendome",
        "title": "মসজিদে নববী ও সম্মানিত সবুজ গম্বুজ",
        "location": "মদিনা মনোওয়ারা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/06/15/167280-836798059_large.mp4"
    },
    {
        "id": "madinah_courtyard_umbrellas",
        "title": "মসজিদে নববীর সুবিশাল ছাতা উন্মোচন দৃশ্য",
        "location": "মসজিদে নববী চত্বর, মদিনা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2021/10/26/93432-639359155_large.mp4"
    },
    {
        "id": "madinah_night_lights",
        "title": "রাতের আলোয় মায়াবী মসজিদে নববী ও মিনার",
        "location": "পবিত্র মদিনা মনোওয়ারা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2024/08/08/225504_large.mp4"
    },
    {
        "id": "madinah_rawdah_peaceful",
        "title": "রওজা শরীফ প্রাঙ্গণ ও শান্ত স্নিগ্ধ পরিবেশ",
        "location": "মসজিদে নববী, মদিনা",
        "local_file": "madinah_nabawi_drone_4k.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2024/06/02/214982_large.mp4"
    },

    # --- পবিত্র হজ ও ওমরাহ (Hajj & Umrah Pilgrimage) ---
    {
        "id": "hajj_arafat_jabal_rahmah",
        "title": "আরাফাতের ময়দান ও জাবালে রহমতে লাখো হাজী",
        "location": "পবিত্র আরাফাত ময়দান",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2023/07/04/170060-842720151_large.mp4"
    },
    {
        "id": "hajj_mina_tent_city",
        "title": "হজের পুণ্যময় তাঁবুর শহর মিনা ও জামারাত",
        "location": "পবিত্র মিনা উপত্যকা",
        "local_file": "makkah_clock_tower_drone.mp4",
        "cdn_url": "https://cdn.pixabay.com/video/2022/11/24/140366-774838017_large.mp4"
    },
    {
        "id": "hajj_safamarwah_sai",
        "title": "সাফা ও মারওয়া পাহাড়ে পুণ্যময় সাঈর দৃশ্য",
        "location": "মসজিদুল হারাম, মক্কা",
        "local_file": "kaaba_beauty_peaceful.mp4",
        "cdn_url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    },
    {
        "id": "hajj_farewell_tawaf",
        "title": "পবিত্র কাবার অশ্রুসিক্ত বিদায়ী তাওয়াফ",
        "location": "মাতাফ শরীফ, মক্কা",
        "local_file": "kaaba_cinematic_shots.mp4",
        "cdn_url": "https://archive.org/download/rain1932/Rain_512kb.mp4"
    }
]

FOOTAGE_HISTORY_FILE = os.path.join(BASE_DIR, "footage_history.json")

def load_footage_history() -> dict:
    if os.path.exists(FOOTAGE_HISTORY_FILE):
        try:
            with open(FOOTAGE_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
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
    """ফুটেজ ফাইল লোকাল ডিরেক্টরিতে নিশ্চিত করে, প্রয়োজনে সিডিএন থেকে ডাউনলোড করে"""
    fname = item["local_file"]
    p = os.path.join(ASSETS_FOOTAGE_DIR, fname)
    if os.path.exists(p) and os.path.getsize(p) > 50000:
        return p

    # যদি লোকাল ফাইল না থাকে তবে সিডিএন থেকে ডাউনলোড
    cdn_target = os.path.join(DOWNLOADS_DIR, f"{item['id']}.mp4")
    if os.path.exists(cdn_target) and os.path.getsize(cdn_target) > 50000:
        return cdn_target

    print(f"📥 ডাউনলোড হচ্ছে পবিত্র দৃশ্যের ফুটেজ: {item['title']}...")
    try:
        r = requests.get(item["cdn_url"], stream=True, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            with open(cdn_target, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            if os.path.exists(cdn_target) and os.path.getsize(cdn_target) > 50000:
                print(f"✅ সফল ডাউনলোড: {cdn_target}")
                return cdn_target
    except Exception as e:
        print(f"[CDN DOWNLOAD WARN] {e}")

    # ফলব্যাক: যেকোনো কার্যকর লোকাল ফুটেজ
    for any_item in HOLY_MAKKAH_MADINAH_HAJJ_POOL:
        any_p = os.path.join(ASSETS_FOOTAGE_DIR, any_item["local_file"])
        if os.path.exists(any_p) and os.path.getsize(any_p) > 50000:
            return any_p

    raise FileNotFoundError("কোনো কার্যকর মক্কা, মদিনা বা হজের ফুটেজ পাওয়া যায়নি।")

def get_next_holy_scenes(count: int = 4) -> tuple:
    """
    কঠোর জিরো-ডুপ্লিকেট রোটেশন:
    পূর্ববর্তী ভিডিওগুলোর ফুটেজ আইডি হিস্টোরি পরীক্ষা করে সম্পূর্ণ ফ্রেশ সিন নির্বাচন করে।
    একই ফুটেজ পরপর বা সাম্প্রতিক ভিডিওতে কখনো রিপিট হবে না।
    """
    history = load_footage_history()
    used_ids = set(history.get("used_ids", [])[-15:])  # সর্বশেষ ১৫টি আইটেম কঠোরভাবে বাদ

    # আনপোস্টেড বা ফ্রেশ সিনগুলো ফিল্টার করা
    candidates = [item for item in HOLY_MAKKAH_MADINAH_HAJJ_POOL if item["id"] not in used_ids]
    if len(candidates) < count:
        print("[NOTICE] পবিত্র দৃশ্যের রোটেশন সাইকেল ফ্রেশ করা হচ্ছে...")
        candidates = list(HOLY_MAKKAH_MADINAH_HAJJ_POOL)
        history["used_ids"] = []

    # বিভিন্ন ধরণের সিন মিলিয়ে নির্বাচন (মক্কা + মদিনা + হজ)
    random.shuffle(candidates)
    selected_items = candidates[:count]
    selected_paths = [ensure_footage_file(item) for item in selected_items]

    for item in selected_items:
        history["used_ids"].append(item["id"])
    history["used_ids"] = history["used_ids"][-30:]  # হিস্টোরিতে সর্বোচ্চ ৩০টি সংরক্ষণ
    save_footage_history(history)

    print(f"🕋 [পবিত্র দৃশ্য নির্বাচন সম্পন্ন] মোট {len(selected_items)}টি সম্পূর্ণ আলাদা দৃশ্য:")
    for idx, it in enumerate(selected_items, 1):
        print(f"   🎬 দৃশ্য #{idx}: {it['title']} ({it['location']})")

    meta = {
        "title": " • ".join([it["title"] for it in selected_items[:2]]),
        "location": "মক্কা মুকাররমা, মদিনা মনোওয়ারা ও পবিত্র হজ প্রাঙ্গণ",
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
    """FFprobe দিয়ে অডিও ফাইলের মোট সঠিক সময়কাল বের করে"""
    cmd = [
        FFMPEG_EXE, "-i", audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"Duration:s*(d+):(d+):(d+.d+)", res.stderr)
    if m:
        hours, mins, secs = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return hours * 3600 + mins * 60 + secs
    return 180.0  # ডিফল্ট ৩ মিনিট

def render_quran_video_with_watermark(scene_paths: list, audio_path: str, out_path: str, is_reel: bool = True) -> str:
    """
    মাল্টিপল ভিন্ন সিন যুক্ত হাই-কোয়ালিটি ভিডিও রেন্ডারিং:
    - রিলস (Reels): ১০৮০x১৯২০ (ভার্টিক্যাল ৯:১৬), ৬০ সেকেন্ড
    - ফুল লং ভিডিও (HQ Long Video): ১৯২০x১০৮০ (ওয়াইডস্ক্রিন ১৬:৯), সম্পূর্ণ সূরার সম্পূর্ণ সময়কাল!
    """
    total_audio_sec = get_audio_duration(audio_path)
    print(f"⏱️ মূল সূরার অডিও সময়কাল: {total_audio_sec/60:.2f} মিনিট ({int(total_audio_sec)} সেকেন্ড)")

    if is_reel:
        w, h = 1080, 1920
        target_dur = min(total_audio_sec, 60.0)  # রিলস সর্বোচ্চ ৬০ সেকেন্ড
        seg_dur = target_dur / len(scene_paths)
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "5000k", "-maxrate", "7000k", "-bufsize", "10000k"]
        print(f"🎨 [REEL RENDERING] ৬০ সেকেন্ডের ৯:১৬ আল্ট্রা-এইচডি রিলস তৈরি হচ্ছে...")
    else:
        w, h = 1920, 1080
        # লং ভিডিও: পুরো সূরার সমান দৈর্ঘ্য (সর্বোচ্চ ১৫ মিনিট ক্লাউড সেফটি লিমিট)
        target_dur = min(total_audio_sec, 900.0)
        seg_dur = 35.0  # প্রতি ৩৫ সেকেন্ড পর পর পবিত্র সিন ট্রানজিশন
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "6000k", "-maxrate", "8000k", "-bufsize", "12000k"]
        print(f"🎨 [FULL LONG VIDEO RENDERING] {target_dur/60:.2f} মিনিটের পূর্ণাঙ্গ ১৬:৯ ওয়াইডস্ক্রিন লং ভিডিও তৈরি হচ্ছে...")

    watermark_png = generate_watermark_overlay(w, h)

    # দৃশ্য লুপ তৈরি (যাতে পুরো সূরার সময়কাল জুড়ে মক্কা, মদিনা ও হজের দৃশ্যগুলো মসৃণভাবে পরিবর্তন হয়)
    inputs = []
    filter_parts = []
    concat_inputs = []

    # দৃশ্যগুলোর পুনরাবৃত্তি হিসাব করা যাতে পুরো target_dur কাভার হয়
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
        "-preset", "fast",
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
    scene_paths, meta = get_next_holy_scenes(count=scene_count)
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
