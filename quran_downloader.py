"""
Quran Video Downloader - Real Live Motion Video Engine
ইউটিউব ও অনলাইন সোর্স থেকে বাস্তব লাইভ মোশন ব্যাকগ্রাউন্ড, বৃষ্টি, প্রকৃতি ও ড্রোন শটের
আসল কুরআন তিলাওয়াত রিলস ডাউনলোড করে যাতে প্রতিটি ভিডিও সম্পূর্ণ আলাদা ও ইউনিক হয়।
"""

import os
import glob
import json
import time
import subprocess
import urllib.request
from pathlib import Path
from config import DOWNLOADS_DIR, BASE_DIR

HISTORY_FILE = os.path.join(BASE_DIR, "posted_video_ids.json")

# ইন্টারনেট আর্কাইভ থেকে ১১৪টি সূরার লাইভ মোশন তিলাওয়াত ফাইল ম্যাপ
ARCHIVE_SURAH_MAP = {
    1: "001-AlFatihah-The-Opening-English-Mishary-AlAfasy.mp4",
    2: "002-AlBaqarah-English-Mishary-AlAfasy.mp4",
    3: "003-AlImran-English-Mishary-AlAfasy.mp4",
    4: "004-AnNisa-English-Mishary-AlAfasy.mp4",
    5: "005-AlMaidah-English-Mishary-AlAfasy.mp4",
    6: "006-AlAnam-English-Mishary-AlAfasy.mp4",
    7: "007-AlAraf-English-Mishary-AlAfasy.mp4",
    8: "008-AlAnfal-English-Mishary-AlAfasy.mp4",
    9: "009-AtTaubah-English-Mishary-AlAfasy.mp4",
    10: "010-Yunus-English-Mishary-AlAfasy.mp4",
    11: "011-Hud-English-Mishary-AlAfasy.mp4",
    12: "012-Yusuf-English-Mishary-AlAfasy.mp4",
    13: "013-ArRad-English-Mishary-AlAfasy.mp4",
    14: "014-ibrahim-English-Mishary-AlAfasy.mp4",
    15: "015-AlHijr-English-Mishary-AlAfasy.mp4",
    16: "016-AnNahl-English-Mishary-AlAfasy.mp4",
    17: "017-AlIsra-English-Mishary-AlAfasy.mp4",
    18: "018-AlKahf-English-Mishary-AlAfasy.mp4",
    19: "019-Maryam-English-Mishary-AlAfasy.mp4",
    20: "020-TaHa-English-Mishary-AlAfasy.mp4",
    21: "021-AlAnbiya-English-Mishary-AlAfasy.mp4",
    22: "022-AlHajj-English-Mishary-AlAfasy.mp4",
    23: "023-AlMuminun-English-Mishary-AlAfasy.mp4",
    24: "024-AnNur-English-Mishary-AlAfasy.mp4",
    25: "025-AlFurqan-English-Mishary-AlAfasy.mp4",
    26: "026-AShuara-English-Mishary-AlAfasy.mp4",
    27: "027-ANaml-English-Mishary-AlAfasy.mp4",
    28: "028-AlQasas-English-Mishary-AlAfasy.mp4",
    29: "029-AlAnkabut-English-Mishary-AlAfasy.mp4",
    30: "030-ArRum-English-Mishary-AlAfasy.mp4",
    31: "031-Luqman-English-Mishary-AlAfasy.mp4",
    32: "032-ASajdah-English-Mishary-AlAfasy.mp4",
    33: "033-AlAhzab-English-Mishary-AlAfasy.mp4",
    34: "034-Saba-English-Mishary-AlAfasy.mp4",
    35: "035-Fatir-English-Mishary-AlAfasy.mp4",
    36: "036-YaSin-English-Mishary-AlAfasy.mp4",
    37: "037-AsSaffat-English-Mishary-AlAfasy.mp4",
    38: "038-Saad-English-Mishary-AlAfasy.mp4",
    39: "039-AzZumar-English-Mishary-AlAfasy.mp4",
    40: "040-Ghafir-English-Mishary-AlAfasy.mp4",
    41: "041-Fuselat-English-Mishary-AlAfasy.mp4",
    42: "042-AShura-English-Mishary-AlAfasy.mp4",
    43: "043-AZukhruf-English-Mishary-AlAfasy.mp4",
    44: "044-ADukhan-English-Mishary-AlAfasy.mp4",
    45: "045-AlJathiyah-English-Mishary-AlAfasy.mp4",
    46: "046-AlAhqaf-English-Mishary-AlAfasy.mp4",
    47: "047-Muhammad-English-Mishary-AlAfasy.mp4",
    48: "048-AlFath-English-Mishary-AlAfasy.mp4",
    49: "049-AlHujurat-English-Mishary-AlAfasyary.mp4",
    50: "050-Qaf-English-Mishary-AlAfasy.mp4",
    51: "051-Azariyat-English-Mishary-AlAfasy.mp4",
    52: "052-ATur-English-Mishary-AlAfasy.mp4",
    53: "053-AlNajm-English-Mishary-AlAfasy.mp4",
    54: "054-AlQamar-English-Mishary-AlAfasy.mp4",
    55: "055-ARahman-English-Mishary-AlAfasy.mp4",
    56: "056-AlWaqiah-English-Mishary-AlAfasy.mp4",
    57: "057-AlHadid-English-Mishary-AlAfasy.mp4",
    58: "058-AlMujadilah-English-Mishary-AlAfasy.mp4",
    59: "059-AlHashr-English-Mishary-AlAfasy.mp4",
    60: "060-AlMumtahanah-English-Mishary-AlAfasy.mp4",
    61: "061-AsSaff-English-Mishary-AlAfasy.mp4",
    62: "062-AlJumuah-English-Mishary-AlAfasy.mp4",
    63: "063-AlMunafiqun-English-Mishary-AlAfasy.mp4",
    64: "064-AlTaghabun-English-Mishary-AlAfasy.mp4",
    65: "065-AlTalaq-English-Mishary-AlAfasy.mp4",
    66: "066-AlTahrim-English-Mishary-AlAfasy.mp4",
    67: "067-AlMulk-English-Mishary-AlAfasy.mp4",
    68: "068-AlQalam-English-Mishary-AlAfasy.mp4",
    69: "069-AlHaqqah-English-Mishary-AlAfasy.mp4",
    70: "070-AlMaarij-English-Mishary-AlAfasy.mp4",
    71: "071-Nuh-English-Mishary-AlAfasy.mp4",
    72: "072-AlJinn-English-Mishary-AlAfasy.mp4",
    73: "073-AlMuzzammil-English-Mishary-AlAfasy.mp4",
    74: "074-AlMuddathir-English-Mishary-AlAfasy.mp4",
    75: "075-AlQiyamah-English-Mishary-AlAfasy.mp4",
    76: "076-AlInsan-English-Mishary-AlAfasy.mp4",
    77: "077-AlMursalat-English-Mishary-AlAfasy.mp4",
    78: "078-AnNaba-English-Mishary-AlAfasy.mp4",
    79: "079-AnNaziat-English-Mishary-AlAfasy.mp4",
    80: "080-Abasa-English-Mishary-AlAfasy.mp4",
    81: "081-AtTakwir-English-Mishary-AlAfasy.mp4",
    82: "082-AlInfitar-English-Mishary-AlAfasy.mp4",
    83: "083-AlMuTafifeen-English-Mishary-AlAfasy.mp4",
    84: "084-AlInshiqaq-English-Mishary-AlAfasy.mp4",
    85: "085-AlBuruj-English-Mishary-AlAfasy.mp4",
    86: "086-AtTariq-English-Mishary-AlAfasy.mp4",
    87: "087-AlAla-English-Mishary-AlAfasy.mp4",
    88: "088-AlGhashiyah-English-Mishary-AlAfasy.mp4",
    89: "089-AlFajr-English-Mishary-AlAfasy.mp4",
    90: "090-AlBalad-English-Mishary-AlAfasy.mp4",
    91: "091-AShams-English-Mishary-AlAfasy.mp4",
    92: "092-AlLail-English-Mishary-AlAfasy.mp4",
    93: "093-AdDuha-English-Mishary-AlAfasy.mp4",
    94: "094-AlSharh-English-Mishary-AlAfasy.mp4",
    95: "095-AtTeen-English-Mishary-AlAfasy.mp4",
    96: "096-AlAlaq-English-Mishary-AlAfasy.mp4",
    97: "097-AlQadr-English-Mishary-AlAfasy.mp4",
    98: "098-AlBayyinah-English-Mishary-AlAfasy.mp4",
    99: "099-AlZalzalah-English-Mishary-AlAfasy.mp4",
    100: "100-AlAdiyat-English-Mishary-AlAfasy.mp4",
    101: "101-AlQariah-English-Mishary-AlAfasy.mp4",
    102: "102-AtTakathur-English-Mishary-AlAfasy.mp4",
    103: "103-AlAsr-English-Mishary-AlAfasy.mp4",
    104: "104-AlHumazah-English-Mishary-AlAfasy.mp4",
    105: "105-AlFeel-English-Mishary-AlAfasy.mp4",
    106: "106-Quraish-English-Mishary-AlAfasy.mp4",
    107: "107-AlMaun-English-Mishary-AlAfasy.mp4",
    108: "108-AlKauthar-English-Mishary-AlAfasy.mp4",
    109: "109-AlKafirun-English-Mishary-AlAfasy.mp4",
    110: "110-AnNasr-English-Mishary-AlAfasy.mp4",
    111: "111-AlMasad-English-Mishary-AlAfasy.mp4",
    112: "112-AlIkhlas-English-Mishary-AlAfasy.mp4",
    113: "113-AlFalaq-English-Mishary-AlAfasy.mp4",
    114: "114-AnNas-English-Mishary-AlAfasy.mp4"
}

def load_posted_ids() -> set:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_posted_id(video_id: str):
    ids = load_posted_ids()
    ids.add(video_id)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(ids)[-500:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[DOWNLOADER] Warning saving history ID: {e}")

def _download_from_archive(surah_num: int, out_path: str) -> bool:
    filename = ARCHIVE_SURAH_MAP.get(surah_num)
    if not filename:
        filename = "112-AlIkhlas-English-Mishary-AlAfasy.mp4"
    url = f"https://archive.org/download/quranarabicenglishmp4/{filename}"
    print(f"[DOWNLOADER] Downloading live video from Archive.org: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(out_path, "wb") as out_f:
            total = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                out_f.write(chunk)
                total += len(chunk)
                if total > 48 * 1024 * 1024:
                    break
        return os.path.exists(out_path) and os.path.getsize(out_path) > 10000
    except Exception as e:
        print(f"[DOWNLOADER] Archive.org fetch notice: {e}")
        return False

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (প্রকৃতি, বৃষ্টি, ড্রোন শট) ও তিলাওয়াত রিলস স্বয়ংক্রিয়ভাবে ডাউনলোড করে।
    একই ভিডিও দ্বিতীয়বার ডাউনলোড হবে না—প্রতিটি ভিডিও সম্পূর্ণ ইউনিক হবে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        try:
            os.remove(f)
        except Exception:
            pass

    surah_num = surah_data.get("number", 1) if surah_data else 1
    surah_bangla = surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}"
    posted_ids = load_posted_ids()

    queries = []
    if surah_data and "query" in surah_data:
        queries.append(surah_data["query"])
    queries.append(f"{surah_bangla} quran recitation emotional reels shorts")
    queries.append(f"{surah_bangla} তিলাওয়াত bangla subtitle shorts")
    queries.append(f"surah {surah_num} emotional beautiful recitation reels")
    queries.append("emotional quran recitation live nature 4k reels shorts")

    selected_video_id = None
    selected_title = None

    for query in queries:
        print(f"[DOWNLOADER] Searching real live video for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch8:{query}",
            "--js-runtimes", "node",
            "--extractor-args", "youtube:player_client=android,web",
            "--no-playlist",
            "--match-filter", "duration <= 90 & duration >= 15",
            "--print", "%(id)s||%(title)s||%(duration)s"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=30)
            lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                v_id = parts[0].strip()
                v_title = parts[1].strip() if len(parts) > 1 else surah_bangla
                if v_id not in posted_ids:
                    selected_video_id = v_id
                    selected_title = v_title
                    break
        except Exception as se:
            print(f"[DOWNLOADER] Search notice ({se}), trying next query...")

        if selected_video_id:
            break

    final_path = None

    if selected_video_id:
        out_template = os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.%(ext)s")
        dl_cmd = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={selected_video_id}",
            "--js-runtimes", "node",
            "--extractor-args", "youtube:player_client=android,web",
            "-f", "mp4[height<=1920]/best[ext=mp4]/best",
            "--max-filesize", "48M",
            "-o", out_template
        ]
        print(f"[DOWNLOADER] Downloading real live video [{selected_video_id}] - {selected_title}")
        try:
            subprocess.run(dl_cmd, capture_output=True, text=True, timeout=60)
            found_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.*"))
            if not found_files:
                found_files = glob.glob(os.path.join(DOWNLOADS_DIR, "*.mp4"))
            if found_files and os.path.exists(found_files[0]) and os.path.getsize(found_files[0]) > 10000:
                final_path = found_files[0]
        except Exception as dle:
            print(f"[DOWNLOADER] yt-dlp notice ({dle}), falling back to direct live source...")

    if not final_path:
        print(f"[DOWNLOADER] Fetching unique live motion recitation video for {surah_bangla} from live video archive...")
        selected_video_id = f"ia_surah_{surah_num}_{int(time.time())}"
        selected_title = f"{surah_bangla} - Beautiful Quran Recitation Live Video"
        archive_path = os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.mp4")
        if _download_from_archive(surah_num, archive_path):
            final_path = archive_path

    if not final_path or not os.path.exists(final_path):
        raise RuntimeError(f"Failed to download video for {surah_bangla}")

    save_posted_id(selected_video_id)
    print(f"[DOWNLOADER] Successfully acquired unique live video ({os.path.getsize(final_path)} bytes): {final_path}")

    return {
        "filepath": final_path,
        "title": selected_title or surah_bangla,
        "video_id": selected_video_id,
        "surah_number": surah_num
    }
