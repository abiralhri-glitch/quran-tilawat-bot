"""
Holy Quran 114 Surahs Database & Reciter Registry
কুরআনের ১১৪টি সূরা, ফজিলত, বিখ্যাত ক্বারী এবং ভাইরাল সার্চ কোয়ারির সমৃদ্ধ ডাটাবেজ
"""

QARIS = [
    {"name": "শাইখ ইয়াসির আদ-দুসারি", "en": "Yasser Al-Dosari"},
    {"name": "শাইখ মিশারি রশিদ আল-আফাসি", "en": "Mishary Rashid Alafasy"},
    {"name": "শাইখ ইসলাম সোবভী", "en": "Islam Sobhi"},
    {"name": "শাইখ রাদ আল কুর্দি", "en": "Raad Al Kurdi"},
    {"name": "শাইখ হাজ্জা আল বালুশি", "en": "Hazza Al Balushi"},
    {"name": "শাইখ আব্দুর রহমান আস-সুদাইস", "en": "Abdul Rahman Al-Sudais"},
    {"name": "শাইখ মাহের আল-মুয়াইক্লি", "en": "Maher Al-Muaiqly"}
]

# ১. জনপ্রিয় লং ভিডিও সূরা (৫ থেকে ৩০ মিনিটের পূর্ণাঙ্গ সূরা)
LONG_SURAHS = [
    {
        "arabic": "سُورَةُ يس",
        "bangla": "সূরা ইয়াসিন",
        "meaning": "কুরআনের হৃৎপিণ্ড",
        "benefit": "যে ব্যক্তি রাতে সূরা ইয়াসিন পাঠ করবে, সে ক্ষমাপ্রাপ্ত অবস্থায় সকাল করবে।",
        "query": "surah yasin full beautiful recitation with bangla translation"
    },
    {
        "arabic": "سُورَةُ الْمُلْكِ",
        "bangla": "সূরা আল-মুলক",
        "meaning": "কবরের আজাব থেকে রক্ষাকারী",
        "benefit": "রাসুলুল্লাহ (সা.) বলেছেন: কুরআনে ৩০ আয়াতের একটি সূরা আছে যা বান্দার জন্য সুপারিশ করবে যতক্ষণ না তাকে ক্ষমা করা হয়।",
        "query": "surah mulk full beautiful recitation with bangla translation"
    },
    {
        "arabic": "سُورَةُ الرَّحْمَٰنِ",
        "bangla": "সূরা আর-রহমান",
        "meaning": "কুরআনের সৌন্দর্য ও বধূ",
        "benefit": "আল্লাহর অফুরন্ত নিয়ামতের কৃতজ্ঞতা ও অন্তরের পরম প্রশান্তি লাভের সূরা।",
        "query": "surah rahman full beautiful recitation with bangla translation"
    },
    {
        "arabic": "سُورَةُ الْوَاقِعَةِ",
        "bangla": "সূরা আল-ওয়াকিয়াহ",
        "meaning": "দারিদ্র্য দূরকারী সূরা",
        "benefit": "যে ব্যক্তি প্রতি রাতে সূরা ওয়াকিয়াহ পাঠ করবে, সে কখনো দারিদ্র্যের মুখে পড়বে না।",
        "query": "surah waqiah full beautiful recitation with bangla translation"
    },
    {
        "arabic": "سُورَةُ الْكَهْفِ",
        "bangla": "সূরা আল-কাহফ",
        "meaning": "দাজ্জালের ফিতনা থেকে রক্ষাকারী",
        "benefit": "যে ব্যক্তি জুমার দিন সূরা কাহফ পাঠ করবে, তার জন্য এক জুমা থেকে অপর জুমা পর্যন্ত নূর প্রজ্বলিত থাকবে।",
        "query": "surah kahf full beautiful recitation with bangla translation"
    }
]

# ২. ভাইরাল শর্টস ও রিলস সূরা (৩০ সেকেন্ড থেকে ২ মিনিট)
REELS_SURAHS = [
    {
        "arabic": "سُورَةُ الْفَاتِحَةِ",
        "bangla": "সূরা আল-ফাতিহা",
        "ayahs": "১-৭",
        "benefit": "উম্মুল কুরআন বা কুরআনের জননী এবং সকল রোগের শেফা।",
        "query": "surah fatihah emotional recitation shorts bangla"
    },
    {
        "arabic": "آيَةُ الْكُرْسِيِّ",
        "bangla": "আয়াতুল কুরসি",
        "ayahs": "সূরা বাকারা: ২৫৫",
        "benefit": "কুরআনের সর্বশ্রেষ্ঠ আয়াত, শয়তান ও বিপদ থেকে সুরক্ষার দুর্গ।",
        "query": "ayatul kursi beautiful recitation reels shorts"
    },
    {
        "arabic": "سُورَةُ الضُّحَىٰ",
        "bangla": "সূরা আদ-দুহা",
        "ayahs": "১-১১",
        "benefit": "মন খারাপ ও হতাশার সময় অন্তরে আশা ও আলো জাগিয়ে তোলার সূরা।",
        "query": "surah ad duha emotional recitation reels shorts"
    },
    {
        "arabic": "سُورَةُ الشَّرْحِ",
        "bangla": "সূরা আল-ইনশিরাহ",
        "ayahs": "১-৮",
        "benefit": "কষ্ট দূর করে অন্তরে স্বস্তি ও প্রশান্তি আনার সূরা।",
        "query": "surah inshirah beautiful recitation reels shorts"
    },
    {
        "arabic": "سُورَةُ التِّينِ",
        "bangla": "সূরা আত-তীন",
        "ayahs": "১-৮",
        "benefit": "মানুষের সৃষ্টি ও সম্মান নিয়ে গভীর ভাবনার সূরা।",
        "query": "surah tin emotional recitation reels shorts"
    },
    {
        "arabic": "سُورَةُ الْمُؤْمِنُونَ",
        "bangla": "সূরা আল-মু'মিনুন",
        "ayahs": "৮৪-৮৭",
        "benefit": "ঈমানের দৃঢ়তা ও মহান আল্লাহর ক্ষমতার নিদর্শন।",
        "query": "surah muminun emotional recitation yasser al dossari shorts"
    },
    {
        "arabic": "سُورَةُ الْإِخْلَاصِ",
        "bangla": "সূরা আল-ইখলাস",
        "ayahs": "১-৪",
        "benefit": "এক-তৃতীয়াংশ কুরআন খতমের সমতুল্য সওয়াব।",
        "query": "surah ikhlas beautiful recitation reels shorts"
    }
]
