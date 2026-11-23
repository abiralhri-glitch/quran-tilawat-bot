"""
Enhanced High-Conversion Watermark & Visual Hook Generator
for 'কুরআনের তিলাওয়াত - Quran Tilawat'
Features:
- Official Top Branding Pill ('কুরআনের তিলাওয়াত • Quran Tilawat')
- Dynamic Eye-Catching Surah & Reciter Hook Card (High-Retention Banner)
- Bottom-Right Follow Call-to-Action Badge
- Cross-platform font discovery (Ubuntu Linux & Windows)
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Candidate font paths for Bengali rendering across Windows and Linux
FONT_CANDIDATES = [
    os.path.join(BASE_DIR, "NotoSansBengali-Bold.ttf"),
    "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf",
    "C:/Windows/Fonts/kalpurush.ttf",
    "C:/Windows/Fonts/solaimanlipi.ttf",
    "C:/Windows/Fonts/vrinda.ttf",
    "C:/Windows/Fonts/Nirmala.ttf",
    "C:/Windows/Fonts/arial.ttf"
]

def get_bengali_font(size: int):
    for fpath in FONT_CANDIDATES:
        if os.path.exists(fpath):
            try:
                return ImageFont.truetype(fpath, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_english_font(size: int):
    for fpath in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(fpath):
            try:
                return ImageFont.truetype(fpath, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

def generate_watermark_overlay(
    width: int = 1080,
    height: int = 1920,
    output_path: str = None,
    surah_name: str = None,
    reciter_name: str = None,
    hook_text: str = None
) -> str:
    """
    Generates a crystal-clear transparent RGBA watermark overlay with:
    1. Top Brand Pill
    2. Dynamic Surah & Reciter Hook Banner
    3. Bottom-Right Follow CTA
    """
    if not output_path:
        output_path = os.path.join(BASE_DIR, f"watermark_{width}x{height}.png")

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    is_vertical = height > width

    # Font sizing
    top_font_size = int(width * (0.034 if is_vertical else 0.024))
    font_bn = get_bengali_font(top_font_size)
    font_en = get_english_font(int(top_font_size * 0.9))

    # 1. TOP BRANDING PILL
    pill_w = int(width * (0.86 if is_vertical else 0.45))
    pill_h = int(height * (0.038 if is_vertical else 0.055))
    pill_x1 = (width - pill_w) // 2
    pill_y1 = int(height * (0.030 if is_vertical else 0.040))
    pill_x2 = pill_x1 + pill_w
    pill_y2 = pill_y1 + pill_h

    draw.rounded_rectangle(
        [(pill_x1, pill_y1), (pill_x2, pill_y2)],
        radius=int(pill_h / 2),
        fill=(8, 14, 28, 220),
        outline=(218, 165, 32, 240),
        width=2
    )

    bn_brand = "কুরআনের তিলাওয়াত"
    sep = "  •  "
    en_brand = "Quran Tilawat"

    bbox_bn = draw.textbbox((0, 0), bn_brand, font=font_bn)
    w_bn = bbox_bn[2] - bbox_bn[0]
    bbox_sep = draw.textbbox((0, 0), sep, font=font_en)
    w_sep = bbox_sep[2] - bbox_sep[0]
    bbox_en = draw.textbbox((0, 0), en_brand, font=font_en)
    w_en = bbox_en[2] - bbox_en[0]

    tot_w = w_bn + w_sep + w_en
    sx = (width - tot_w) / 2
    cy = (pill_y1 + pill_y2) / 2

    draw.text((sx, cy), bn_brand, font=font_bn, fill=(255, 255, 255, 255), anchor="lm")
    draw.text((sx + w_bn, cy), sep, font=font_en, fill=(230, 185, 45, 245), anchor="lm")
    draw.text((sx + w_bn + w_sep, cy), en_brand, font=font_en, fill=(255, 255, 255, 255), anchor="lm")

    # 2. DYNAMIC SURAH & HOOK BANNER (Upper Third)
    if surah_name:
        banner_w = int(width * (0.88 if is_vertical else 0.55))
        banner_h = int(height * (0.090 if is_vertical else 0.115))
        bx1 = (width - banner_w) // 2
        by1 = pill_y2 + int(height * 0.020)
        bx2 = bx1 + banner_w
        by2 = by1 + banner_h

        # Modern glassmorphism translucent gradient card
        draw.rounded_rectangle(
            [(bx1, by1), (bx2, by2)],
            radius=int(banner_h * 0.18),
            fill=(10, 16, 32, 205),
            outline=(212, 175, 55, 210),
            width=2
        )

        surah_fsize = int(width * (0.040 if is_vertical else 0.026))
        sub_fsize = int(width * (0.028 if is_vertical else 0.019))
        font_surah = get_bengali_font(surah_fsize)
        font_sub = get_bengali_font(sub_fsize)

        # Line 1: Surah Title (clean text, no emojis)
        clean_title = re.sub(r'[^\w\s\u0980-\u09FF\.\-•\|\:]', '', surah_name).strip()
        draw.text(
            ((bx1 + bx2) // 2, by1 + int(banner_h * 0.35)),
            clean_title,
            font=font_surah,
            fill=(255, 235, 120, 255),
            anchor="mm"
        )

        # Line 2: Reciter or Spiritual Hook (clean text, no emojis)
        raw_line2 = hook_text if hook_text else (f"{reciter_name}" if reciter_name else "মন জুড়ানো তিলাওয়াত • না টেনে শুনুন")
        clean_line2 = re.sub(r'[^\w\s\u0980-\u09FF\.\-•\|\:]', '', raw_line2).strip()
        draw.text(
            ((bx1 + bx2) // 2, by1 + int(banner_h * 0.72)),
            clean_line2,
            font=font_sub,
            fill=(235, 245, 255, 240),
            anchor="mm"
        )

    # 3. BOTTOM-RIGHT FOLLOW CTA BADGE
    cta_w = int(width * (0.50 if is_vertical else 0.30))
    cta_h = int(height * (0.038 if is_vertical else 0.050))
    cta_x1 = width - cta_w - int(width * 0.04)
    cta_y1 = height - cta_h - int(height * 0.04)
    cta_x2 = cta_x1 + cta_w
    cta_y2 = cta_y1 + cta_h

    draw.rounded_rectangle(
        [(cta_x1, cta_y1), (cta_x2, cta_y2)],
        radius=int(cta_h / 2),
        fill=(12, 18, 35, 220),
        outline=(255, 215, 0, 245),
        width=2
    )

    cta_font = get_english_font(int(cta_h * 0.45))
    draw.text(
        ((cta_x1 + cta_x2) // 2, (cta_y1 + cta_y2) // 2),
        "+ Follow For Daily Tilawat",
        font=cta_font,
        fill=(255, 225, 20, 255),
        anchor="mm"
    )

    img.save(output_path, "PNG")
    return output_path

if __name__ == "__main__":
    p_reel = generate_watermark_overlay(
        1080, 1920,
        output_path="test_wm_reel.png",
        surah_name="সূরা আর-রহমান • পূর্ণাঙ্গ তিলাওয়াত",
        reciter_name="শাইখ আব্দুর রহমান আস-সুদাইস",
        hook_text="দিল শান্ত করা তিলাওয়াত • না টেনে শুনুন 🌿"
    )
    print("Reel watermark created:", p_reel)
    p_long = generate_watermark_overlay(
        1920, 1080,
        output_path="test_wm_long.png",
        surah_name="সূরা আল-মুলক • কবরের আজাব থেকে মুক্তি",
        reciter_name="শাইখ মিশারি রশিদ আল-আফাসি",
        hook_text="পবিত্র কুরআনের অফুরন্ত রহমত ও বরকত 🤲"
    )
    print("Long video watermark created:", p_long)
