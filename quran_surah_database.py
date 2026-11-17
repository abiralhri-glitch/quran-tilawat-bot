"""
Holy Quran 114 Surahs Database & Reciter Registry
পবিত্র কুরআনের ১১৪টি পূর্ণাঙ্গ সূরা, জনপ্রিয় আয়াত ও ফজিলতের সমৃদ্ধ ডাটাবেজ
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

# ১. জনপ্রিয় লং ভিডিও সূরা (পূর্ণাঙ্গ তিলাওয়াত)
LONG_SURAHS = [
    {
        "number": 1,
        "arabic": "سُورَةُ الْفَاتِحَةِ",
        "bangla": "সূরা আল-ফাতিহা",
        "ayahs": "১-৭ (পূর্ণাঙ্গ)",
        "meaning": "কুরআনের ভূমিকা ও শেফা",
        "benefit": "উম্মুল কুরআন বা কুরআনের জননী এবং সকল রোগের শেফা।",
        "query": "surah fatihah full beautiful recitation with bangla translation"
    },
    {
        "number": 36,
        "arabic": "سُورَةُ يس",
        "bangla": "সূরা ইয়াসিন",
        "ayahs": "১-৮৩ (পূর্ণাঙ্গ)",
        "meaning": "কুরআনের হৃৎপিণ্ড",
        "benefit": "যে ব্যক্তি রাতে সূরা ইয়াসিন পাঠ করবে, সে ক্ষমাপ্রাপ্ত অবস্থায় সকাল করবে।",
        "query": "surah yasin full beautiful recitation with bangla translation"
    },
    {
        "number": 55,
        "arabic": "سُورَةُ الرَّحْمَٰنِ",
        "bangla": "সূরা আর-রহমান",
        "ayahs": "১-৭৮ (পূর্ণাঙ্গ)",
        "meaning": "কুরআনের বধূ ও পরম দয়া",
        "benefit": "আল্লাহর অফুরন্ত নিয়ামতের কৃতজ্ঞতা ও অন্তরের পরম প্রশান্তি লাভের সূরা।",
        "query": "surah rahman full beautiful recitation with bangla translation"
    },
    {
        "number": 56,
        "arabic": "سُورَةُ الْوَاقِعَةِ",
        "bangla": "সূরা আল-ওয়াকিয়াহ",
        "ayahs": "১-৯৬ (পূর্ণাঙ্গ)",
        "meaning": "দারিদ্র্য দূরকারী সূরা",
        "benefit": "যে ব্যক্তি প্রতি রাতে সূরা ওয়াকিয়াহ পাঠ করবে, সে কখনো দারিদ্র্যের মুখে পড়বে না।",
        "query": "surah waqiah full beautiful recitation with bangla translation"
    },
    {
        "number": 67,
        "arabic": "سُورَةُ الْمُلْكِ",
        "bangla": "সূরা আল-মুলক",
        "ayahs": "১-৩০ (পূর্ণাঙ্গ)",
        "meaning": "কবরের আজাব থেকে রক্ষাকারী",
        "benefit": "রাসুলুল্লাহ (সা.) বলেছেন: কুরআনে ৩০ আয়াতের একটি সূরা আছে যা বান্দার জন্য সুপারিশ করবে।",
        "query": "surah mulk full beautiful recitation with bangla translation"
    },
    {
        "number": 18,
        "arabic": "سُورَةُ الْكَهْفِ",
        "bangla": "সূরা আল-কাহফ",
        "ayahs": "১-১১০ (পূর্ণাঙ্গ)",
        "meaning": "দাজ্জালের ফিতনা থেকে রক্ষাকারী",
        "benefit": "যে ব্যক্তি জুমার দিন সূরা কাহফ পাঠ করবে, তার জন্য নূর প্রজ্বলিত থাকবে।",
        "query": "surah kahf full beautiful recitation with bangla translation"
    },
    {
        "number": 12,
        "arabic": "سُورَةُ يُوسُفَ",
        "bangla": "সূরা ইউসুফ",
        "ayahs": "১-১১১ (পূর্ণাঙ্গ)",
        "meaning": "সর্বোত্তম কাহিনী",
        "benefit": "ধৈর্য, পরীক্ষা ও আল্লাহর পরিকল্পনার অপার সৌন্দর্য বোঝার সর্বোত্তম সূরা।",
        "query": "surah yusuf full beautiful recitation with bangla translation"
    },
    {
        "number": 19,
        "arabic": "سُورَةُ مَرْيَمَ",
        "bangla": "সূরা মারিয়াম",
        "ayahs": "১-৯৮ (পূর্ণাঙ্গ)",
        "meaning": "আল্লাহর অপরিসীম রহমত",
        "benefit": "অসম্ভবকে সম্ভব করার জন্য এবং নেক সন্তানের জন্য দোয়ার সূরা।",
        "query": "surah maryam full beautiful recitation with bangla translation"
    },
    {
        "number": 20,
        "arabic": "سُورَةُ طٰهٰ",
        "bangla": "সূরা ত্বা-হা",
        "ayahs": "১-১৩৫ (পূর্ণাঙ্গ)",
        "meaning": "অন্তরের প্রশান্তি",
        "benefit": "কঠিন পরিস্থিতি সহজ করা ও অন্তরের ভার দূর করার অনন্য সূরা।",
        "query": "surah taha full beautiful recitation with bangla translation"
    },
    {
        "number": 73,
        "arabic": "سُورَةُ الْمُزَّمِّلِ",
        "bangla": "সূরা আল-মুযযাম্মিল",
        "ayahs": "১-২০ (পূর্ণাঙ্গ)",
        "meaning": "রাতের তাহাজ্জুদ ও আমল",
        "benefit": "কুরআন তিলাওয়াত ও গভীর রাতে আল্লাহর নৈকট্য লাভের প্রেরণা।",
        "query": "surah muzzammil full beautiful recitation with bangla translation"
    }
]

# ২. ভাইরাল রিলস ও শর্টস সূরা (১১৪টি সূরার বিভিন্ন আয়াত ও সংক্ষিপ্ত তিলাওয়াত)
REELS_SURAHS = [
    {"number": 1, "arabic": "سُورَةُ الْفَاتِحَةِ", "bangla": "সূরা আল-ফাতিহা", "ayahs": "১-৭", "benefit": "উম্মুল কুরআন ও সকল রোগের শেফা।", "query": "surah fatihah emotional recitation shorts bangla"},
    {"number": 2, "arabic": "آيَةُ الْكُرْسِيِّ", "bangla": "সূরা আল-বাকারা (আয়াতুল কুরসি)", "ayahs": "২৫৫", "benefit": "কুরআনের সর্বশ্রেষ্ঠ আয়াত, সুরক্ষার দুর্গ।", "query": "ayatul kursi beautiful recitation reels shorts"},
    {"number": 2, "arabic": "آمَنَ الرَّسُولُ", "bangla": "সূরা আল-বাকারা (শেষ ২ আয়াত)", "ayahs": "২৮৫-২৮৬", "benefit": "রাতে যে পড়বে তার জন্য এটিই যথেষ্ট হবে।", "query": "amanar rasulu surah baqarah last 2 ayats shorts"},
    {"number": 2, "arabic": "فَاذْكُرُونِي أَذْكُرْكُمْ", "bangla": "সূরা আল-বাকারা (স্মরণ ও সবর)", "ayahs": "১৫২-১৫৭", "benefit": "বিপদে ধৈর্য ও আল্লাহর রহমতের সান্ত্বনা।", "query": "surah baqarah 152 157 emotional shorts"},
    {"number": 3, "arabic": "سُورَةُ آلِ عِمْرَانَ", "bangla": "সূরা আলে ইমরান", "ayahs": "১৩৩-১৩৬", "benefit": "তওবা ও ক্ষমার দিকে দ্রুত ধাবিত হওয়ার আহ্বান।", "query": "surah ali imran emotional recitation shorts"},
    {"number": 3, "arabic": "سُورَةُ آلِ عِمْرَانَ", "bangla": "সূরা আলে ইমরান (দোয়ার আয়াত)", "ayahs": "১৯০-১৯৪", "benefit": "আকাশ ও জমিন সৃষ্টির গভীর চিন্তা ও আকুল মোনাজাত।", "query": "surah ali imran 190 194 shorts bangla"},
    {"number": 9, "arabic": "سُورَةُ التَّوْبَةِ", "bangla": "সূরা আত-তাওবাহ (হাসবিয়াল্লাহ)", "ayahs": "১২৮-১২৯", "benefit": "রাসূল (ﷺ)-এর দয়া ও আল্লাহর ওপর পূর্ণ নির্ভরতা।", "query": "surah tawbah last 2 ayats emotional shorts"},
    {"number": 13, "arabic": "سُورَةُ الرَّعْدِ", "bangla": "সূরা আর-রাদ (অন্তরের প্রশান্তি)", "ayahs": "২৮-২৯", "benefit": "আল্লাহর স্মরণেই কেবল অন্তরসমূহ প্রশান্ত হয়।", "query": "surah rad ayat 28 emotional recitation shorts"},
    {"number": 14, "arabic": "سُورَةُ إِبْرَاهِيمَ", "bangla": "সূরা ইব্রাহিম (শুকরিয়ার আয়াত)", "ayahs": "৭", "benefit": "কৃতজ্ঞতা প্রকাশ করলে নিয়ামত বাড়িয়ে দেওয়া হয়।", "query": "surah ibrahim ayat 7 shorts bangla"},
    {"number": 17, "arabic": "سُورَةُ الْإِسْرَاءِ", "bangla": "সূরা আল-ইসরা (পিতা-মাতার হক)", "ayahs": "২৩-২৪", "benefit": "মা-বাবার জন্য রহমতের দোয়া।", "query": "surah isra parents ayat emotional shorts"},
    {"number": 18, "arabic": "سُورَةُ الْكَهْفِ", "bangla": "সূরা আল-কাহফ (প্রথম ১০ আয়াত)", "ayahs": "১-১০", "benefit": "দাজ্জালের ফিতনা থেকে নিরাপত্তা পাওয়ার দোয়া।", "query": "surah kahf first 10 ayats shorts"},
    {"number": 18, "arabic": "سُورَةُ الْكَهْفِ", "bangla": "সূরা আল-কাহফ (শেষ আয়াতসমূহ)", "ayahs": "১০৭-১১০", "benefit": "জান্নাতুল ফেরদাউসের সুসংবাদ ও তাওহীদ।", "query": "surah kahf last ayats emotional shorts"},
    {"number": 21, "arabic": "سُورَةُ الْأَنْبِيَاءِ", "bangla": "সূরা আল-আম্বিয়া (দোয়ায়ে ইউনুস)", "ayahs": "৮৭-৮৮", "benefit": "যেকোনো বিপদ ও কষ্ট থেকে নিশ্চিত মুক্তির দোয়া।", "query": "surah anbiya dua yunus emotional shorts"},
    {"number": 23, "arabic": "سُورَةُ الْمُؤْمِنُونَ", "bangla": "সূরা আল-মু'মিনুন", "ayahs": "১-১১", "benefit": "সফল মুমিনের বৈশিষ্ট্য ও জান্নাতুল ফেরদাউসের উত্তরাধিকার।", "query": "surah muminun 1 11 emotional shorts"},
    {"number": 23, "arabic": "سُورَةُ الْمُؤْمِنُونَ", "bangla": "সূরা আল-মু'মিনুন", "ayahs": "৮৪-৮৭", "benefit": "মহান আল্লাহর কুদরত ও মহাবিশ্ব পরিচালনা।", "query": "surah muminun emotional recitation shorts"},
    {"number": 24, "arabic": "آيَةُ النُّورِ", "bangla": "সূরা আন-নূর (আয়াতুন নূর)", "ayahs": "৩৫", "benefit": "আকাশ ও পৃথিবীর নূরের অনন্য রূপক বর্ণনা।", "query": "ayatun nur surah nur 35 emotional shorts"},
    {"number": 25, "arabic": "سُورَةُ الْفُرْقَانِ", "bangla": "সূরা আল-ফুরকান (রহমানের বান্দা)", "ayahs": "৬৩-৭৭", "benefit": "রহমানের প্রিয় বান্দাদের বিনম্র গুণাবলী।", "query": "surah furqan ibadur rahman shorts"},
    {"number": 36, "arabic": "سُورَةُ يس", "bangla": "সূরা ইয়াসিন (কুন ফায়াকুন)", "ayahs": "৭৮-৮৩", "benefit": "আল্লাহ যখন ইচ্ছা করেন শুধু বলেন 'হও', আর হয়ে যায়।", "query": "surah yasin kun fayakun emotional shorts"},
    {"number": 39, "arabic": "سُورَةُ الزُّمَرِ", "bangla": "সূরা আয-যুমার (রহমতের ডাক)", "ayahs": "৫৩-৫৪", "benefit": "আল্লাহর অসীম রহমত থেকে কখনো নিরাশ হয়ো না।", "query": "surah zumar 53 emotional recitation shorts"},
    {"number": 40, "arabic": "سُورَةُ غَافِرٍ", "bangla": "সূরা গাফির (দোয়ার নিশ্চয়তা)", "ayahs": "৬০", "benefit": "তোমরা আমাকে ডাকো, আমি তোমাদের ডাকে সাড়া দেব।", "query": "surah ghafir ayat 60 shorts bangla"},
    {"number": 48, "arabic": "سُورَةُ الْفَتْحِ", "bangla": "সূরা আল-ফাতহ", "ayahs": "১-৪", "benefit": "সুস্পষ্ট বিজয় ও অন্তরে পরম প্রশান্তি নাজিল।", "query": "surah fath emotional recitation shorts"},
    {"number": 50, "arabic": "سُورَةُ ق", "bangla": "সূরা কাফ", "ayahs": "১৬-২২", "benefit": "আল্লাহ মানুষের গলার শিরা থেকেও বেশি নিকটে আছেন।", "query": "surah qaf emotional recitation shorts"},
    {"number": 54, "arabic": "سُورَةُ الْقَمَرِ", "bangla": "সূরা আল-কামার", "ayahs": "১৭, ২২, ৩২, ৪০", "benefit": "কুরআন শিক্ষা করাকে আল্লাহ সহজ করে দিয়েছেন।", "query": "surah qamar emotional recitation shorts"},
    {"number": 55, "arabic": "سُورَةُ الرَّحْمَٰنِ", "bangla": "সূরা আর-রহমান", "ayahs": "১-১৩", "benefit": "তোমরা তোমাদের রবের কোন কোন নিয়ামতকে অস্বীকার করবে?", "query": "surah rahman emotional recitation shorts"},
    {"number": 55, "arabic": "سُورَةُ الرَّحْمَٰنِ", "bangla": "সূরা আর-রহমান (সবকিছু ধ্বংসশীল)", "ayahs": "২৬-২৮", "benefit": "সবকিছু নশ্বর, কেবল রবের সত্তাই চিরস্থায়ী।", "query": "surah rahman kullu man alayha fan shorts"},
    {"number": 56, "arabic": "سُورَةُ الْوَاقِعَةِ", "bangla": "সূরা আল-ওয়াকিয়াহ", "ayahs": "১-১৪", "benefit": "কিয়ামতের আগমন ও তিন শ্রেণির মানুষ।", "query": "surah waqiah emotional recitation shorts"},
    {"number": 59, "arabic": "سُورَةُ الْحَشْرِ", "bangla": "সূরা আল-হাশর (শেষ ৩ আয়াত)", "ayahs": "২২-২৪", "benefit": "আল্লাহর মহান গুণবাচক নামসমূহ।", "query": "surah hashr last 3 ayats emotional shorts"},
    {"number": 65, "arabic": "سُورَةُ الطَّلَاقِ", "bangla": "সূরা আত-তালাক (তাওয়াক্কুল)", "ayahs": "২-৩", "benefit": "যে আল্লাহর ওপর ভরসা করে, আল্লাহই তার জন্য যথেষ্ট।", "query": "surah talaq ayat 2 3 emotional shorts"},
    {"number": 67, "arabic": "سُورَةُ الْمُلْكِ", "bangla": "সূরা আল-মুলক", "ayahs": "১-৫", "benefit": "কবরের সুরক্ষা ও সুন্দর সৃষ্টির রহস্য।", "query": "surah mulk emotional recitation shorts"},
    {"number": 75, "arabic": "سُورَةُ الْقِيَامَةِ", "bangla": "সূরা আল-কিয়ামাহ", "ayahs": "১-২৫", "benefit": "মানুষের পুনরুত্থান ও হিসাবের দিনের বাস্তবতা।", "query": "surah qiyamah emotional recitation shorts"},
    {"number": 78, "arabic": "سُورَةُ النَّبَإِ", "bangla": "সূরা আন-নাবা", "ayahs": "১-১৬", "benefit": "মহাসংবাদ ও মহান রবের সৃষ্টির মহিমা।", "query": "surah naba emotional recitation shorts"},
    {"number": 79, "arabic": "سُورَةُ النَّازِعَاتِ", "bangla": "সূরা আন-নাযিআত", "ayahs": "৩৪-৪১", "benefit": "জাহান্নামের ভয় ও জান্নাতের আনন্দ।", "query": "surah naziat emotional recitation shorts"},
    {"number": 81, "arabic": "سُورَةُ التَّكْوِيرِ", "bangla": "সূরা আত-তাকভীর", "ayahs": "১-১৪", "benefit": "সূর্য যখন আলোহীন হবে—হৃদয় নাড়া দেওয়া দৃশ্য।", "query": "surah takwir emotional recitation shorts"},
    {"number": 82, "arabic": "سُورَةُ الْإِنْفِطَارِ", "bangla": "সূরা আল-ইনফিতার", "ayahs": "১-১২", "benefit": "হে মানুষ! কোন জিনিস তোমাকে তোমার দয়াময় রব থেকে দূরে রাখল?", "query": "surah infitar emotional recitation shorts"},
    {"number": 84, "arabic": "سُورَةُ الْإِنْشِقَاقِ", "bangla": "সূরা আল-ইনশিকাক", "ayahs": "১-১৫", "benefit": "বান্দার আমলনামা ডান হাতে প্রাপ্তির সৌভাগ্য।", "query": "surah inshiqaq emotional recitation shorts"},
    {"number": 85, "arabic": "سُورَةُ الْبُرُوجِ", "bangla": "সূরা আল-বুরুজ", "ayahs": "১-১১", "benefit": "মুমিনদের আত্মত্যাগ ও চিরস্থায়ী জান্নাতের প্রতিশ্রুতি।", "query": "surah buruj emotional recitation shorts"},
    {"number": 86, "arabic": "سُورَةُ الطَّارِقِ", "bangla": "সূরা আত-তারিক", "ayahs": "১-১০", "benefit": "মানুষের সৃষ্টি ও প্রতিটি আত্মার ওপর সংরক্ষণকারী প্রহরী।", "query": "surah tariq emotional recitation shorts"},
    {"number": 87, "arabic": "سُورَةُ الْأَعْلَىٰ", "bangla": "সূরা আল-আ'লা", "ayahs": "১-১৯", "benefit": "পবিত্রতম রবের পবিত্রতা ঘোষণা।", "query": "surah ala emotional recitation shorts"},
    {"number": 88, "arabic": "سُورَةُ الْغَاشِيَةِ", "bangla": "সূরা আল-গাশিয়াহ", "ayahs": "১-২৬", "benefit": "জান্নাতবাসীদের প্রফুল্ল চেহারা ও নেয়ামত।", "query": "surah ghashiyah emotional recitation shorts"},
    {"number": 89, "arabic": "سُورَةُ الْفَجْرِ", "bangla": "সূরা আল-ফজর", "ayahs": "২৭-৩০", "benefit": "হে প্রশান্ত আত্মা! ফিরে এসো তোমার রবের সান্নিধ্যে।", "query": "surah fajr ya ayyatuhan nafsul mutmainnah shorts"},
    {"number": 90, "arabic": "سُورَةُ الْبَلَدِ", "bangla": "সূরা আল-বালাদ", "ayahs": "১-১৮", "benefit": "কষ্টের দুনিয়া ও সৎকর্মশীলদের পথ।", "query": "surah balad emotional recitation shorts"},
    {"number": 91, "arabic": "سُورَةُ الشَّمْسِ", "bangla": "সূরা আশ-শামস", "ayahs": "১-১৫", "benefit": "যে নিজের আত্মাকে পরিশুদ্ধ করল, সে সফল হলো।", "query": "surah shams emotional recitation shorts"},
    {"number": 92, "arabic": "سُورَةُ اللَّيْلِ", "bangla": "সূরা আল-লায়ল", "ayahs": "১-২১", "benefit": "আল্লাহর রাস্তায় দানকারীদের পথ সহজ করার ওয়াদা।", "query": "surah layl emotional recitation shorts"},
    {"number": 93, "arabic": "سُورَةُ الضُّحَىٰ", "bangla": "সূরা আদ-দুহা", "ayahs": "১-১১", "benefit": "মন খারাপ ও হতাশার সময় অন্তরে আশা ও আলো জাগিয়ে তোলার সূরা।", "query": "surah ad duha emotional recitation reels shorts"},
    {"number": 94, "arabic": "سُورَةُ الشَّرْحِ", "bangla": "সূরা আল-ইনশিরাহ", "ayahs": "১-৮", "benefit": "কষ্ট দূর করে অন্তরে স্বস্তি ও প্রশান্তি আনার সূরা।", "query": "surah inshirah beautiful recitation reels shorts"},
    {"number": 95, "arabic": "سُورَةُ التِّينِ", "bangla": "সূরা আত-তীন", "ayahs": "১-৮", "benefit": "মানুষের সৃষ্টি ও সম্মান নিয়ে গভীর ভাবনার সূরা।", "query": "surah tin emotional recitation reels shorts"},
    {"number": 96, "arabic": "سُورَةُ الْعَلَقِ", "bangla": "সূরা আল-আলাক (ইকরা)", "ayahs": "১-৫", "benefit": "কুরআনের সর্বপ্রথম নাজিলকৃত বাণী।", "query": "surah alaq iqra emotional recitation shorts"},
    {"number": 97, "arabic": "سُورَةُ الْقَدْرِ", "bangla": "সূরা আল-কদর", "ayahs": "১-৫", "benefit": "হাজার মাসের চেয়েও উত্তম লাইলাতুল কদরের সূরা।", "query": "surah qadr emotional recitation reels shorts"},
    {"number": 99, "arabic": "سُورَةُ الزَّلْزَلَةِ", "bangla": "সূরা আয-যালযালাহ", "ayahs": "১-৮", "benefit": "অণু পরিমাণ ভালো কাজও কিয়ামতে বৃথা যাবে না।", "query": "surah zalzalah emotional recitation shorts"},
    {"number": 100, "arabic": "سُورَةُ الْعَادِيَاتِ", "bangla": "সূরা আল-আদিয়াত", "ayahs": "১-১১", "benefit": "আল্লাহর নিয়ামতের অকৃতজ্ঞ না হওয়ার শিক্ষা।", "query": "surah adiyat emotional recitation shorts"},
    {"number": 101, "arabic": "سُورَةُ الْقَارِعَةِ", "bangla": "সূরা আল-কারিয়াহ", "ayahs": "১-১১", "benefit": "মিজানের পাল্লা ভারী হওয়ার সুসংবাদ।", "query": "surah qariah emotional recitation shorts"},
    {"number": 102, "arabic": "سُورَةُ التَّكَاثُرِ", "bangla": "সূরা আত-তাকাসুর", "ayahs": "১-৮", "benefit": "অতিরিক্ত পাওয়ার মোহ মানুষকে কবর পর্যন্ত নিয়ে যায়।", "query": "surah takathur emotional recitation shorts"},
    {"number": 103, "arabic": "سُورَةُ الْعَصْرِ", "bangla": "সূরা আল-আসর", "ayahs": "১-৩", "benefit": "সময়ের মূল্যায়ন, ঈমান, সৎকাজ ও ধৈর্যের শিক্ষা।", "query": "surah asr beautiful recitation reels shorts"},
    {"number": 104, "arabic": "سُورَةُ الْهُمَزَةِ", "bangla": "সূরা আল-হুমাযাহ", "ayahs": "১-৯", "benefit": "পরনিন্দা ও মানুষের পেছনে কুৎসা রটানোর বিরুদ্ধে সতর্কবার্তা।", "query": "surah humazah emotional recitation shorts"},
    {"number": 105, "arabic": "سُورَةُ الْفِيلِ", "bangla": "সূরা আল-ফিল", "ayahs": "১-৫", "benefit": "কা'বা শরীফ রক্ষায় আবাবিল পাখির মাধ্যমে কুদরতের প্রকাশ।", "query": "surah fil beautiful recitation reels shorts"},
    {"number": 106, "arabic": "سُورَةُ قُرَيْشٍ", "bangla": "সূরা কুরাইশ", "ayahs": "১-৪", "benefit": "ক্ষুধা ও ভীতি থেকে নিরাপত্তার দোয়া।", "query": "surah quraysh emotional recitation shorts"},
    {"number": 107, "arabic": "سُورَةُ الْمَاعُونِ", "bangla": "সূরা আল-মাউন", "ayahs": "১-৭", "benefit": "এতিম ও মিসকিনদের সাহায্য করার আহ্বান।", "query": "surah maun emotional recitation shorts"},
    {"number": 108, "arabic": "سُورَةُ الْكَوْثَرِ", "bangla": "সূরা আল-কাউসার", "ayahs": "১-৩", "benefit": "কুরআনের সবচেয়ে ছোট সূরা ও হাউজে কাউসারের সুসংবাদ।", "query": "surah kawthar emotional recitation reels shorts"},
    {"number": 109, "arabic": "سُورَةُ الْكَافِرُونَ", "bangla": "সূরা আল-কাফিরুন", "ayahs": "১-৬", "benefit": "শিরকমুক্ত নিখাদ তাওহীদের ঘোষণা।", "query": "surah kafirun emotional recitation reels shorts"},
    {"number": 110, "arabic": "سُورَةُ النَّصْرِ", "bangla": "সূরা আন-নাসর", "ayahs": "১-৩", "benefit": "আল্লাহর সাহায্য, বিজয় ও বেশি বেশি ইস্তিগফারের নির্দেশ।", "query": "surah nasr emotional recitation reels shorts"},
    {"number": 112, "arabic": "سُورَةُ الْإِخْلَاصِ", "bangla": "সূরা আল-ইখলাস", "ayahs": "১-৪", "benefit": "এক-তৃতীয়াংশ কুরআন খতমের সমতুল্য সওয়াব।", "query": "surah ikhlas beautiful recitation reels shorts"},
    {"number": 113, "arabic": "سُورَةُ الْفَلَقِ", "bangla": "সূরা আল-ফালাক", "ayahs": "১-৫", "benefit": "জাদু, হিংসা ও অকল্যাণ থেকে সুরক্ষার সর্বোত্তম সূরা।", "query": "surah falaq emotional recitation reels shorts"},
    {"number": 114, "arabic": "سُورَةُ النَّاسِ", "bangla": "সূরা আন-নাস", "ayahs": "১-৬", "benefit": "শয়তানের কুমন্ত্রণা ও অনিষ্ট থেকে সুরক্ষার মহৌষধ।", "query": "surah nas beautiful recitation reels shorts"}
]
