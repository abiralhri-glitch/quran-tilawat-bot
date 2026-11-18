"""
Contextual Auto-Comment Responder for Islamic Facebook Pages
('কুরআনের তিলাওয়াত - Quran Tilawat', 'Jannat', 'Islamic Waz')
স্বয়ংক্রিয়ভাবে প্রতিটি পোস্ট ও রিলের নতুন কমেন্ট শনাক্ত করে এবং পোস্টের প্রেক্ষাপট অনুযায়ী
মার্জিত, ইসলামিক দোয়া ও শুভেচ্ছা সম্বলিত রিপ্লাই প্রদান করে।
ডুপ্লিকেট রিপ্লাই সম্পূর্ণ প্রতিরোধ করে (replied_comments.json ট্র্যাকিং)।
"""

import os
import json
import time
import random
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPLIED_FILE = os.path.join(BASE_DIR, "replied_comments.json")

# প্রেক্ষাপটভিত্তিক ইসলামিক দোয়া ও উত্তরের সমৃদ্ধ ডাটাবেজ
REPLIES_DB = {
    "ameen": [
        "আমিন ইয়া রব্বাল আলামীন 🤲 মহান আল্লাহ আপনার নেক দোয়া কবুল করে নিন।",
        "আল্লাহুম্মা আমিন 🤲 আল্লাহ আপনাকে ও আপনার পরিবারকে দুনিয়া ও আখিরাতে উত্তম কল্যাণ দান করুন।",
        "আমিন 🤲 মহান আল্লাহ পাক আমাদের সবাইকে সিরাতুল মুস্তাকিমের উপর অবিচল রাখুন।",
        "আমিন ইয়া রব্বুল আলামিন 🤍 আল্লাহ আপনার মনের সকল নেক আশা পূর্ণ করুন।"
    ],
    "praise": [
        "জাযাকাল্লাহু খাইরান প্রিয় দ্বীনি ভাই/বোন 🌸 মহান আল্লাহ আপনাকে উত্তম প্রতিদান দান করুন।",
        "সুবহানাল্লাহিল আজিম 🤍 আল্লাহর কালামের নূর আপনার জীবন ও পরিবারকে আলোকিত করুক।",
        "মাশাআল্লাহ 🤲 নিয়মিত এমন হৃদয়স্পর্শী ইসলামিক বার্তা পেতে পেজটির সাথেই থাকুন।",
        "আলহামদুলিল্লাহ! মহান রবের প্রশংসায় অন্তর প্রশান্ত হোক 🌿 জাযাকাল্লাহু খাইরান।"
    ],
    "alhamdulillah": [
        "আলহামদুলিল্লাহ! সর্বাবস্থায় মহান রবের শুকরিয়া। আল্লাহ আপনার জীবনে অফুরন্ত বরকত দিন 🤲",
        "আলহামদুলিল্লাহ 🤍 কৃতজ্ঞ বান্দাদের আল্লাহ ভালোবাসেন। আল্লাহ আপনাকে সম্মানিত করুন।"
    ],
    "salam": [
        "ওয়ালাইকুম আসসালাম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহু 🌸 পেজটির সাথে থাকার জন্য আন্তরিক ধন্যবাদ ও জাযাকাল্লাহ।",
        "ওয়ালাইকুম আসসালাম 🌿 মহান আল্লাহ আপনাকে সুস্থ ও ঈমানের সাথে রাখুন।"
    ],
    "share": [
        "অনেক অনেক ধন্যবাদ ও জাযাকাল্লাহ 🤍 ভালো দ্বীনি কাজ সবার মাঝে ছড়িয়ে দেওয়াও একটি সদকায়ে জারিয়া।",
        "আল্লাহ আপনার এই খেদমত কবুল করুন 🤲 সদকায়ে জারিয়া হিসেবে এটি আপনার নাজাতের উসিলা হোক।"
    ],
    "general_quran": [
        "কুরআনের সাথে থাকুন, কুরআনকে ভালোবাসুন 📖 মহান আল্লাহ আপনাকে কুরআন বুঝে আমল করার তাওফিক দিন 🤲",
        "জাযাকাল্লাহু খাইরান 🤍 কুরআনের এই বাণী সবার মাঝে ছড়িয়ে দিতে লাইক ও শেয়ার করে পাশে থাকুন।",
        "আল্লাহ আপনার হৃদয়কে পবিত্র কুরআনের আলোয় উজ্জ্বল করে দিন 🤲 পেজটির সাথে থাকার জন্য আন্তরিক মোবারকবাদ।"
    ],
    "general_jannat": [
        "জাযাকাল্লাহু খাইরান 🤍 মহান আল্লাহ আপনাকে ও আপনার পিতা-মাতাকে জান্নাতুল ফিরদাউস নসিব করুন 🤲",
        "আল্লাহর রহমত ও বরকত আপনার জীবনে বর্ষিত হোক 🌸 পেজের সাথেই থাকুন।",
        "মহান আল্লাহ আপনার প্রতিটি নেক আমল কবুল করে নিন 🤲 জাযাকাল্লাহু খাইরান।"
    ]
}

def load_replied_history() -> set:
    if os.path.exists(REPLIED_FILE):
        try:
            with open(REPLIED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
        except Exception:
            return set()
    return set()

def save_replied_history(replied_set: set):
    try:
        with open(REPLIED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(replied_set), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[REPLY LOG ERROR] {e}")

def determine_contextual_reply(comment_text: str, post_context: str = "", page_type: str = "quran") -> str:
    """কমেন্টের ভাষা ও পোস্টের বিষয় বিশ্লেষণ করে সবচেয়ে মানানসই উত্তর নির্বাচন করে"""
    comment_lower = comment_text.lower().strip()

    # ১. আমিন বা দোয়া
    if any(k in comment_lower for k in ["আমিন", "আমীন", "ameen", "amin", "amen"]):
        return random.choice(REPLIES_DB["ameen"])

    # ২. মাশাআল্লাহ / সুবহানাল্লাহ
    if any(k in comment_lower for k in ["মাশাআল্লাহ", "সুবহানাল্লাহ", "mashaallah", "subhanallah", "mashallah"]):
        return random.choice(REPLIES_DB["praise"])

    # ৩. আলহামদুলিল্লাহ
    if any(k in comment_lower for k in ["আলহামদুলিল্লাহ", "alhamdulillah", "alhamdullilah"]):
        return random.choice(REPLIES_DB["alhamdulillah"])

    # ৪. সালাম
    if any(k in comment_lower for k in ["সালাম", "salam", "assalam", "assalamualaikum"]):
        return random.choice(REPLIES_DB["salam"])

    # ৫. শেয়ার / প্রশংসা
    if any(k in comment_lower for k in ["শেয়ার", "share", "সুন্দর", "nice", "good", "best", "valo", "ভালো"]):
        return random.choice(REPLIES_DB["share"])

    # ৬. সাধারণ উত্তর
    if page_type == "jannat":
        return random.choice(REPLIES_DB["general_jannat"])
    else:
        return random.choice(REPLIES_DB["general_quran"])

def reply_to_comment(comment_id: str, message: str, access_token: str) -> bool:
    """ফেসবুক গ্রাফ এপিআই-এর মাধ্যমে নির্দিষ্ট কমেন্টে রিপ্লাই পাঠায়"""
    url = f"https://graph.facebook.com/v21.0/{comment_id}/comments"
    params = {"access_token": access_token}
    data = {"message": message}
    try:
        r = requests.post(url, params=params, data=data, timeout=15)
        res = r.json()
        if "id" in res:
            print(f"  💬 সফল কমেন্ট রিপ্লাই: ID {comment_id} -> '{message[:40]}...'")
            return True
        else:
            print(f"  ❌ কমেন্ট রিপ্লাই ব্যর্থ: {res}")
            return False
    except Exception as e:
        print(f"  ❌ কমেন্ট রিপ্লাই এক্সেপশন: {e}")
        return False

def run_comment_responder(page_id: str = None, access_token: str = None, page_type: str = "quran", max_replies: int = 10) -> int:
    """
    পেজের সাম্প্রতিক ভিডিও এবং পোস্টের কমেন্টগুলো চেক করে এবং স্বয়ংক্রিয়ভাবে রিপ্লাই দেয়।
    """
    if not page_id:
        page_id = os.environ.get("FB_PAGE_ID")
    if not access_token:
        access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")

    if not page_id or not access_token:
        print("[AUTO-COMMENT] Page ID বা Access Token পাওয়া যায়নি। স্কিপ করা হলো।")
        return 0

    print(f"\n========================================================")
    print(f"🤖 স্মার্ট অটো-কমেন্ট রেসপন্ডার চালু: Page {page_id} ({page_type.upper()})")
    print(f"========================================================")

    replied_history = load_replied_history()
    new_replies_count = 0

    # ভিডিও এবং রিলস সংগ্রহ
    url_vids = f"https://graph.facebook.com/v21.0/{page_id}/videos"
    params_v = {
        "access_token": access_token,
        "fields": "id,title,description,created_time,comments{id,message,from,created_time,comments}",
        "limit": 10
    }

    try:
        r = requests.get(url_vids, params=params_v, timeout=20)
        videos_data = r.json().get("data", [])
    except Exception as e:
        print(f"[AUTO-COMMENT ERROR] ভিডিও লিস্ট ফেচ ব্যর্থ: {e}")
        videos_data = []

    for item in videos_data:
        if new_replies_count >= max_replies:
            break

        item_id = item.get("id")
        post_title = item.get("title") or item.get("description") or ""
        comments = item.get("comments", {}).get("data", [])

        for comment in comments:
            if new_replies_count >= max_replies:
                break

            c_id = comment.get("id")
            c_msg = comment.get("message", "").strip()
            from_info = comment.get("from", {})
            from_id = from_info.get("id")

            # ১. নিজের কমেন্ট বা খালি কমেন্ট এড়িয়ে চলা
            if not c_msg or from_id == page_id:
                continue

            # ২. ইতিপূর্বে রিপ্লাই দেওয়া কমেন্ট স্কিপ করা
            if c_id in replied_history:
                continue

            # ৩. কমেন্টে পেজ থেকে অলরেডি চাইল্ড রিপ্লাই আছে কিনা চেক
            child_comments = comment.get("comments", {}).get("data", [])
            already_replied_on_fb = any(child.get("from", {}).get("id") == page_id for child in child_comments)
            if already_replied_on_fb:
                replied_history.add(c_id)
                continue

            # ৪. প্রাসঙ্গিক উত্তর প্রস্তুতকরণ ও পোস্ট
            reply_text = determine_contextual_reply(c_msg, post_title, page_type=page_type)
            success = reply_to_comment(c_id, reply_text, access_token)
            if success:
                replied_history.add(c_id)
                new_replies_count += 1
                time.sleep(random.uniform(1.5, 3.0))

    save_replied_history(replied_history)
    print(f"✅ অটো-কমেন্ট রেসপন্ডার শেষ: {new_replies_count} টি নতুন কমেন্টে রিপ্লাই সম্পন্ন।\n")
    return new_replies_count

if __name__ == "__main__":
    run_comment_responder()
