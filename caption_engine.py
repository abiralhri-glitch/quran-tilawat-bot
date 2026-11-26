"""
Viral Quran Caption & Recommendation-Compliant Hook Generator
ফেসবুক রিকমেন্ডেশন গাইডলাইন (Recommendation Guidelines) ও কমিউনিটি স্ট্যান্ডার্ড ১০০% মেনে
কুরআনের প্রতিটি সূরা ও আয়াতের জন্য হৃদয়স্পর্শী হুক, অর্থ, ফজিলত, স্ট্রং ফলো কল-টু-অ্যাকশন এবং ভাইরাল হ্যাশট্যাগ
"""

import random

VIRAL_ISLAMIC_HASHTAGS = [
    "#Quran", "#QuranTilawat", "#HolyQuran", "#QuranRecitation", "#ViralReels",
    "#TrendingReels", "#IslamicReels", "#Makkah", "#Madinah", "#PeacefulRecitation",
    "#EmotionalTilawat", "#QuranLovers", "#Islam", "#ForYou", "#ReelsViral",
    "#SubhanAllah", "#Alhamdulillah", "#Allah", "#IslamicVideo", "#Sunnah",
    "#DailyQuran", "#Reels2026", "#IslamicShorts", "#Surah", "#IslamicStatus",
    "#FBReelsViral", "#IslamicReminder", "#Deen"
]

REEL_ENGAGEMENT_HOOKS = [
    "🌸 মাত্র ২০ সেকেন্ড চোখ বন্ধ করে শুনুন—পবিত্র কুরআনের এই তিলাওয়াত আপনার অন্তরে গভীর প্রশান্তি এনে দেবে ইনশাআল্লাহ। 🤲✨",
    "🌿 মাত্র ২০ সেকেন্ডে চোখ ও দিল জুড়িয়ে নেওয়ার মতো একটি দৃশ্য ও পবিত্র তিলাওয়াত। 🤍",
    "✨ আসুন ২০ সেকেন্ডের জন্য দুনিয়ার সব ক্লান্তি ভুলে রবের কালামে মন জুড়াই—আল্লাহ আমাদের ক্ষমা করুন। 🤲",
    "💡 দিনে অন্তত ২০ সেকেন্ড হলেও আল্লাহর কালাম শুনুন, আপনার জীবনে ও পরিবারে অফুরন্ত বরকত নেমে আসবে ইনশাআল্লাহ। 🌸",
    "🤍 খুব বেশি মন খারাপ বা মানসিক চাপে আছেন? ২০ সেকেন্ড এই তিলাওয়াতটি শুনুন, দিল শান্ত হয়ে যাবে। 🤲🌿",
    "📖 মহাগ্রন্থ আল-কুরআনের শান্তিময় এই ২০ সেকেন্ড মনোযোগ দিয়ে শুনুন। 🤍🤲"
]

LONG_VIDEO_ENGAGEMENT_HOOKS = [
    "🌸 সম্পূর্ণ সূরাটির পূর্ণাঙ্গ তিলাওয়াত মনোযোগ দিয়ে শুনুন—আল্লাহ আপনার জীবন ও পরিবারে অফুরন্ত বরকত ও রহমত দান করুন। 🤲✨",
    "🌿 কাজ, পড়াশোনা বা বিশ্রামের সময় মন শান্ত রাখতে এই পূর্ণাঙ্গ পবিত্র কুরআন তিলাওয়াতটি শুনুন। 🤍",
    "✨ অন্তরের গভীর প্রশান্তি ও শেফার নিয়ামত পেতে সম্পূর্ণ সূরাটি গভীর মনোযোগের সাথে শুনুন। 🤲",
    "💡 পরিবারে রহমত ও রোগমুক্তির নিয়ামত পেতে পুরো সূরাটি ঘরে চালু রাখুন এবং মনোযোগ দিয়ে শুনুন। 🌸",
    "🤍 মনকে সকল দুশ্চিন্তা ও মানসিক চাপ থেকে মুক্ত রাখতে এই পবিত্র দীর্ঘ তিলাওয়াতটি শুনুন। 🤲🌿"
]

FOLLOW_CTAS = [
    "👇 প্রতিদিন অন্তরের প্রশান্তিময় এমন পবিত্র কুরআন তিলাওয়াত শুনতে এখনই আমাদের পেজটিতে [ফলো / + Follow] দিয়ে সাথে থাকুন! 👆",
    "👇 এমন হৃদয়স্পর্শী তিলাওয়াত নিয়মিত পেতে পেজটিতে লাইক ও [ফলো / + Follow] দিয়ে রাখুন এবং শেয়ার করে সদকায়ে জারিয়ার অংশীদার হোন। 🌸🤲",
    "👇 পবিত্র কুরআনের আলো সবার মাঝে ছড়িয়ে দিতে পেজটি [ফলো / + Follow] করে রাখুন এবং দ্বীনি স্বার্থে ভিডিওটি শেয়ার করুন। 📖✨"
]

def generate_quran_caption(surah_data: dict, qari_name: str, mosque_info: str = "", is_reel: bool = True) -> str:
    """
    Generates a high-conversion, recommendation-safe Facebook post caption.
    Strictly follows Meta Community Standards (No clickbait, no false claims, 100% authentic Quranic value).
    """
    arabic_name = surah_data.get("arabic", "القرآن الكريم")
    bangla_name = surah_data.get("bangla", "পবিত্র কুরআন")
    meaning = surah_data.get("meaning", "আল্লাহর পবিত্র কালাম")
    benefit = surah_data.get("benefit", "")
    ayahs = surah_data.get("ayahs", "")

    hook = random.choice(REEL_ENGAGEMENT_HOOKS if is_reel else LONG_VIDEO_ENGAGEMENT_HOOKS)
    cta = random.choice(FOLLOW_CTAS)
    
    # 20+ High-Reach Trending Hashtags
    selected_tags = random.sample(VIRAL_ISLAMIC_HASHTAGS, min(22, len(VIRAL_ISLAMIC_HASHTAGS)))
    hashtags_str = " ".join(selected_tags)

    lines = []
    # 1. First Line: Powerful Clean Spiritual Hook (visible before "... See more")
    lines.append(hook)
    lines.append("")

    # 2. Surah & Reciter Details
    if is_reel:
        lines.append(f"📖 {arabic_name} • {bangla_name} {'[আয়াত: ' + ayahs + ']' if ayahs else ''}")
    else:
        lines.append(f"🎧 পূর্ণাঙ্গ পবিত্র তিলাওয়াত: {arabic_name} ({bangla_name})")

    lines.append(f"🎙️ ইমাম/ক্বারী: {qari_name}")
    if mosque_info:
        lines.append(f"🕌 দৃশ্যপট: {mosque_info}")
    lines.append(f"✨ অর্থ ও তাৎপর্য: {meaning}")
    lines.append("━━━━━━━━━━━━━━━━━━━━")

    if benefit:
        lines.append(f"💡 ফজিলত ও গুরুত্ব:\n{benefit}\n")

    # 3. Clean Follow CTA
    lines.append(cta)
    lines.append("")

    # 4. Trending Mega Hashtags
    lines.append(hashtags_str)

    return "\n".join(lines)
