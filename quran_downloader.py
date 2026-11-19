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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# ১০টি বিশ্ববিখ্যাত পবিত্র মসজিদ ও হারামাইন শরীফাইনের আসল 1080p সিনেমাটিক ফুটেজ
REAL_MOSQUE_FOOTAGES = [
    {
        "file": "makkah_clock_tower_drone.mp4",
        "title": "মক্কা ক্লক টাওয়ার ও গ্র্যান্ড হারাম",
        "location": "মক্কা মুকাররমা"
    },
    {
        "file": "kaaba_cinematic_shots.mp4",
        "title": "পবিত্র কাবা শরীফ ও গিলাফ",
        "location": "পবিত্র কাবা চত্বর"
    },
    {
        "file": "madinah_nabawi_drone_4k.mp4",
        "title": "মসজিদে নববী ও সবুজ গম্বুজ",
        "location": "মদিনা মনোওয়ারা"
    },
    {
        "file": "sheikh_zayed_grand_mosque.mp4",
        "title": "শেখ জায়েদ গ্র্যান্ড মসজিদ",
        "location": "সংযুক্ত আরব আমিরাত"
    },
    {
        "file": "sultan_ahmed_blue_mosque.mp4",
        "title": "ঐতিহাসিক সুলতান আহমেদ নীল মসজিদ",
        "location": "ইস্তাম্বুল, তুরস্ক"
    },
    {
        "file": "faisal_mosque_islamabad.mp4",
        "title": "ঐতিহাসিক ফয়সাল মসজিদ",
        "location": "ইসলামাবাদ, পাকিস্তান"
    },
    {
        "file": "putra_mosque_malaysia.mp4",
        "title": "পুত্রা মসজিদ",
        "location": "পুত্রজায়া, মালয়েশিয়া"
    },
    {
        "file": "hassan_ii_mosque_morocco.mp4",
        "title": "ঐতিহাসিক দ্বিতীয় হাসান মসজিদ",
        "location": "কাসাব্লাঙ্কা, মরক্কো"
    },
    {
        "file": "badshahi_mosque_lahore.mp4",
        "title": "ঐতিহাসিক বাদশাহী মসজিদ",
        "location": "লাহোর, পাকিস্তান"
    },
    {
        "file": "kaaba_beauty_peaceful.mp4",
        "title": "পবিত্র কাবা প্রাঙ্গণ ও মাতাফ",
        "location": "মসজিদুল হারাম, মক্কা"
    }
]

FOOTAGE_HISTORY_FILE = os.path.join(BASE_DIR, "footage_history.json")

def get_next_mosque_scenes(count: int = 4, surah_data: dict = None) -> tuple:
    """
    মাল্টি-সিন সিলেকশন:
    একটি ভিডিওর জন্য count সংখ্যক সম্পূর্ণ আলাদা পবিত্র মসজিদ ফুটেজ নির্বাচন করে।
    ভিডিওর ভেতর কোনো ক্লিপ রিপিট হবে না।
    পরবর্তী পোস্টের জন্য স্বয়ংক্রিয়ভাবে রোটেশন অনুযায়ী পরবর্তী দৃশ্যগুলো নির্বাচন করবে।
    """
    history = {"last_index": -1, "used_records": []}
    if os.path.exists(FOOTAGE_HISTORY_FILE):
        try:
            with open(FOOTAGE_HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    available = []
    for item in REAL_MOSQUE_FOOTAGES:
        p = os.path.join(ASSETS_FOOTAGE_DIR, item["file"])
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            available.append(item)

    if not available:
        raise FileNotFoundError("কোনো পবিত্র মসজিদ বা হারামাইনের সিনেমাটিক ফুটেজ পাওয়া যায়নি।")

    last_index = history.get("last_index", -1)
    selected_items = []
    selected_paths = []

    # count সংখ্যক ভিন্ন ভিন্ন সিন রোটেশন থেকে পিক করা
    for i in range(count):
        idx = (last_index + 1 + i) % len(available)
        item = available[idx]
        selected_items.append(item)
        selected_paths.append(os.path.join(ASSETS_FOOTAGE_DIR, item["file"]))

    history["last_index"] = (last_index + count) % len(available)
    if "used_records" not in history or not isinstance(history["used_records"], list):
        history["used_records"] = []

    for item in selected_items:
        history["used_records"].append({
            "file": item["file"],
            "surah": surah_data.get("bangla") if surah_data else "Unknown",
            "timestamp": int(time.time())
        })
    if len(history["used_records"]) > 50:
        history["used_records"] = history["used_records"][-50:]

    try:
        with open(FOOTAGE_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HISTORY WARN] {e}")

    titles = " • ".join([it["title"] for it in selected_items])
    locations = " • ".join(list(dict.fromkeys([it["location"] for it in selected_items])))

    print(f"🕌 [মাল্টি-সিন নির্বাচন সম্পন্ন] মোট {len(selected_items)}টি ভিন্ন ভিন্ন দৃশ্য:")
    for idx, it in enumerate(selected_items, 1):
        print(f"   🎬 দৃশ্য #{idx}: {it['title']} ({it['location']})")

    combined_meta = {
        "title": titles,
        "location": locations,
        "scenes": selected_items
    }
    return selected_paths, combined_meta

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

def render_quran_video_with_watermark(scene_paths: list, audio_path: str, out_path: str, is_reel: bool = True) -> str:
    """
    মাল্টিপল ভিন্ন সিন যুক্ত হাই-রিটেনশন ডায়নামিক ভিডিও রেন্ডারিং:
    - রিলস (Reels): ১০৮০x১৯২০ (ভার্টিক্যাল ৯:১৬), ৩টি সিন x ২০ সেকেন্ড = ৬০ সেকেন্ড
    - লং ভিডিও (HQ Video): ১৯২০x১০৮০ (ওয়াইডস্ক্রিন ১৬:৯), ৪টি সিন x ২৫ সেকেন্ড = ১০০ সেকেন্ড
    - একটানা অবিরত তিলাওয়াত অডিও এবং অফিশিয়াল ক্রিস্টাল ক্লিয়ার ওয়াটারমার্ক
    """
    if is_reel:
        w, h = 1080, 1920
        seg_dur = 20  # ৩টি সিন x ২০ সেকেন্ড = ৬০ সেকেন্ড
        target_scenes = scene_paths[:3]
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "18"
        bitrate_args = ["-b:v", "6000k", "-maxrate", "8000k", "-bufsize", "12000k"]
        print(f"🎨 [REEL MULTI-SCENE RENDERING] {len(target_scenes)}টি ভিন্ন সিন সহ ৬০ সেকেন্ডের রিলস তৈরি হচ্ছে...")
    else:
        w, h = 1920, 1080
        seg_dur = 25  # ৪টি সিন x ২৫ সেকেন্ড = ১০০ সেকেন্ড
        target_scenes = scene_paths[:4]
        scale_filter = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        crf = "17"
        bitrate_args = ["-b:v", "8000k", "-maxrate", "12000k", "-bufsize", "16000k"]
        print(f"🎨 [HQ VIDEO MULTI-SCENE RENDERING] {len(target_scenes)}টি ভিন্ন সিন সহ ১০০ সেকেন্ডের ফুল এইচডি লং ভিডিও তৈরি হচ্ছে...")

    watermark_png = generate_watermark_overlay(w, h)

    inputs = []
    filter_parts = []
    concat_inputs = []

    for i, sc in enumerate(target_scenes):
        inputs.extend(["-stream_loop", "-1", "-i", sc])
        filter_parts.append(f"[{i}:v]{scale_filter},trim=duration={seg_dur},setpts=PTS-STARTPTS[v{i}]")
        concat_inputs.append(f"[v{i}]")

    num_scenes = len(target_scenes)
    # তিলাওয়াত অডিও হচ্ছে ইনপুট ইনডেক্স `num_scenes`
    inputs.extend(["-i", audio_path])
    audio_idx = num_scenes

    # ওয়াটারমার্ক হচ্ছে ইনপুট ইনডেক্স `num_scenes + 1`
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

    subprocess.run(cmd, check=True)
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

    print("\n=======================================================")
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
