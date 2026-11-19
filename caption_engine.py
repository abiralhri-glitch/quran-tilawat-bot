"""
Viral Quran Caption & Hashtag Generator
কুরআনের প্রতিটি সূরা ও আয়াতের জন্য হৃদয়স্পর্শী ক্যাপশন, অর্থ, ফজিলত এবং হ্যাশট্যাগ জেনারেটর
"""

import random

VIRAL_ISLAMIC_HASHTAGS = [
    "#Quran", "#QuranTilawat", "#Surah", "#IslamicReels", "#QuranRecitation",
    "#HolyQuran", "#Islam", "#IslamicReminders", "#Peace", "#Jannat",
    "#MakkahHaramain", "#MaherAlMuaiqly", "#AbdurRahmanSudais", "#YasserAlDosari", "#BengaliQuran", "#Sunnah", "#Dua"
]

ENGAGEMENT_HOOKS = [
    "কুরআনের এই মিষ্টি তিলাওয়াত শুনলে অন্তর শান্ত হয়ে যায়। সুবহানাল্লাহ! 🤍✨",
    "দিনে অন্তত একবার হলেও আল্লাহর পবিত্র কালাম শুনুন, দিলের দুশ্চিন্তা দূর হবে। 📖🌸",
    "আল্লাহ যাকে ভালোবাসেন, তাকে দ্বীনের সঠিক বুঝ ও কুরআনের মহব্বত দান করেন। ❤️🤲",
    "যে ব্যক্তি একটি আয়াত পাঠ করে বা শোনে, সে অফুরন্ত নেক আমল অর্জন করে। 🌿💫",
    "অন্তরের প্রশান্তি খুঁজতে গিয়ে কুরআন শুনুন, এক অদ্ভুত নীরব শান্তি অনুভব করবেন। 🤲🤍"
]

CTA_OPTIONS = [
    "👉 তিলাওয়াতটি ভালো লাগলে শেয়ার করে অন্য ভাই-বোনদের শোনার সুযোগ করে দিন। পেজটি ফলো দিয়ে সাথে থাকুন। 🌸",
    "👉 কুরআন প্রচারে আমাদের সাথে থাকুন—একটি শেয়ার হয়তো কারো হেদায়েতের কারণ হতে পারে। 📖✨",
    "👉 প্রতিনিয়ত অন্তরের প্রশান্তিময় এমন কুরআন তিলাওয়াত পেতে পেজটিতে লাইক ও ফলো দিয়ে রাখুন। 🤲❤️"
]

def generate_quran_caption(surah_data: dict, qari_name: str, mosque_info: str = "", is_reel: bool = True) -> str:
    """
    Generates a full Facebook post caption for a Quran recitation.
    """
    arabic_name = surah_data.get("arabic", "القرآن الكريم")
    bangla_name = surah_data.get("bangla", "পবিত্র কুরআন")
    meaning = surah_data.get("meaning", "আল্লাহর পবিত্র কালাম")
    benefit = surah_data.get("benefit", "")
    ayahs = surah_data.get("ayahs", "")

    hook = random.choice(ENGAGEMENT_HOOKS)
    cta = random.choice(CTA_OPTIONS)
    hashtags = " ".join(random.sample(VIRAL_ISLAMIC_HASHTAGS, 8))

    lines = []
    if is_reel:
        lines.append(f"📖 {arabic_name} • {bangla_name} {'[আয়াত: ' + ayahs + ']' if ayahs else ''}")
    else:
        lines.append(f"🎧 পূর্ণাঙ্গ তিলাওয়াত: {arabic_name} ({bangla_name})")

    lines.append(f"🎙️ ইমাম/ক্বারী: {qari_name}")
    if mosque_info:
        lines.append(f"🕌 দৃশ্যপট: {mosque_info}")
    lines.append(f"✨ অর্থ ও তাৎপর্য: {meaning}")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append(hook)
    
    if benefit:
        lines.append(f"\n💡 ফজিলত ও গুরুত্ব:\n{benefit}")

    lines.append("\n" + cta)
    lines.append("\n" + hashtags)

    return "\n".join(lines)
