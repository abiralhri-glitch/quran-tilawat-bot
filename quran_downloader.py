"""
Quran Video Downloader
উচ্চমানের বাংলা অনুবাদসহ পবিত্র কুরআনের ১১৪টি সূরার সরাসরি ও দ্রুততম ডাউনলোড ইঞ্জিন
"""

import os
import glob
import urllib.request
import requests
from config import DOWNLOADS_DIR

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    পবিত্র কুরআনের সূরা ও রিলস সরাসরি হাই-স্পিড ইসলামিক আর্কাইভ থেকে ডাউনলোড করে
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    
    # পূর্ববর্তী অস্থায়ী ফাইল মুছে ফেলা
    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        try:
            os.remove(f)
        except Exception:
            pass

    surah_num = surah_data.get("number", 1) if surah_data else 1
    file_id = f"{surah_num:03d}"
    out_video_path = os.path.join(DOWNLOADS_DIR, f"quran_{file_id}.mp4")
    
    # সরাসরি ইন্টারনেট আর্কাইভ (BANGLAQURAN) হাই-স্পিড লিঙ্ক
    direct_url = f"https://archive.org/download/BANGLAQURAN_20160813/{file_id}.mp4"
    print(f"[DOWNLOADER] Downloading Surah #{surah_num} directly from Islamic Archive: {direct_url}")
    
    download_success = False
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        r = requests.get(direct_url, headers=headers, stream=True, timeout=60)
        if r.status_code == 200:
            with open(out_video_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            if os.path.exists(out_video_path) and os.path.getsize(out_video_path) > 100000:
                download_success = True
                print(f"[DOWNLOADER] Successfully downloaded: {os.path.getsize(out_video_path)} bytes")
    except Exception as e:
        print(f"[DOWNLOADER] Archive direct download failed: {e}")

    # ফলব্যাক: যদি সরাসরি লিঙ্ক ব্যর্থ হয় তবে বিকল্প সার্কিট
    if not download_success:
        alt_url = f"https://ia800305.us.archive.org/15/items/BANGLAQURAN_20160813/{file_id}.mp4"
        try:
            r = requests.get(alt_url, headers=headers, stream=True, timeout=60)
            if r.status_code == 200:
                with open(out_video_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                if os.path.exists(out_video_path) and os.path.getsize(out_video_path) > 100000:
                    download_success = True
        except Exception as e2:
            print(f"[DOWNLOADER] Alt archive failed: {e2}")

    if not download_success or not os.path.exists(out_video_path):
        raise RuntimeError(f"Could not download Quran video for Surah #{surah_num}")

    # যদি রিলস হয় এবং ভিডিও দীর্ঘ হয়, তবে MoviePy দিয়ে প্রথম ৬০ সেকেন্ড কেটে রিলস তৈরি
    final_path = out_video_path
    if is_reel:
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(out_video_path)
            duration = min(clip.duration, 60.0)
            reel_path = os.path.join(DOWNLOADS_DIR, f"quran_{file_id}_reel.mp4")
            sub_clip = clip.subclip(0, duration)
            sub_clip.write_videofile(reel_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
            clip.close()
            sub_clip.close()
            final_path = reel_path
            print(f"[DOWNLOADER] Reel segment extracted successfully: {duration}s")
        except Exception as me:
            print(f"[DOWNLOADER] Reel clip creation failed, using full file: {me}")
            final_path = out_video_path

    metadata = {
        "filepath": final_path,
        "title": surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}",
        "surah_number": surah_num
    }
    return metadata
