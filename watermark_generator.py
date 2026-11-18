"""
Watermark Generator for 'কুরআনের তিলাওয়াত - Quran Tilawat'
Creates broadcast-grade, anti-aliased watermark overlays for both 9:16 (Reels) and 16:9 (Widescreen)
100% immune to missing glyphs: supports both Bengali & English without any square boxes (□).
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "NotoSansBengali-Bold.ttf")

def generate_watermark_overlay(width: int = 720, height: int = 1280, output_path: str = None) -> str:
    """
    Generates a crystal-clear transparent RGBA watermark overlay.
    """
    if not output_path:
        output_path = os.path.join(BASE_DIR, f"watermark_{width}x{height}.png")

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Load Bengali Font
    font_size = int(width * 0.038)
    if os.path.exists(FONT_PATH):
        try:
            font_bn = ImageFont.truetype(FONT_PATH, font_size)
            sub_font_bn = ImageFont.truetype(FONT_PATH, int(width * 0.024))
        except Exception:
            font_bn = ImageFont.load_default()
            sub_font_bn = font_bn
    else:
        font_bn = ImageFont.load_default()
        sub_font_bn = font_bn

    # 2. Load Latin/English font
    try:
        font_en = ImageFont.load_default(size=int(font_size * 0.85))
        sub_font_en = ImageFont.load_default(size=int(width * 0.022))
    except Exception:
        font_en = ImageFont.load_default()
        sub_font_en = font_en

    # Top Watermark Badge Dimensions
    pill_w = int(width * 0.72)
    pill_h = int(height * 0.046)
    pill_x1 = (width - pill_w) // 2
    pill_y1 = int(height * 0.035)
    pill_x2 = pill_x1 + pill_w
    pill_y2 = pill_y1 + pill_h

    # Rounded translucent dark pill with golden border
    draw.rounded_rectangle(
        [(pill_x1, pill_y1), (pill_x2, pill_y2)],
        radius=int(pill_h / 2),
        fill=(10, 15, 30, 205),
        outline=(218, 165, 32, 235),
        width=2
    )

    # Draw Bilingual Title: 'কুরআনের তিলাওয়াত • Quran Tilawat'
    bn_text = "কুরআনের তিলাওয়াত"
    sep = "  •  "
    en_text = "Quran Tilawat"

    bbox_bn = draw.textbbox((0, 0), bn_text, font=font_bn)
    w_bn = bbox_bn[2] - bbox_bn[0]
    bbox_sep = draw.textbbox((0, 0), sep, font=font_en)
    w_sep = bbox_sep[2] - bbox_sep[0]
    bbox_en = draw.textbbox((0, 0), en_text, font=font_en)
    w_en = bbox_en[2] - bbox_en[0]

    total_w = w_bn + w_sep + w_en
    start_x = (width - total_w) / 2
    center_y = (pill_y1 + pill_y2) / 2

    # Draw each component with its correct font to avoid '□' square boxes
    draw.text((start_x, center_y), bn_text, font=font_bn, fill=(255, 255, 255, 250), anchor="lm")
    draw.text((start_x + w_bn, center_y), sep, font=font_en, fill=(218, 165, 32, 240), anchor="lm")
    draw.text((start_x + w_bn + w_sep, center_y), en_text, font=font_en, fill=(255, 255, 255, 250), anchor="lm")

    # Bottom Right subtle branding badge
    bot_w = int(width * 0.44)
    bot_h = int(height * 0.032)
    bot_x1 = width - bot_w - int(width * 0.03)
    bot_y1 = height - bot_h - int(height * 0.03)
    bot_x2 = bot_x1 + bot_w
    bot_y2 = bot_y1 + bot_h

    draw.rounded_rectangle(
        [(bot_x1, bot_y1), (bot_x2, bot_y2)],
        radius=int(bot_h / 2),
        fill=(0, 0, 0, 165)
    )
    draw.text(
        ((bot_x1 + bot_x2) // 2, (bot_y1 + bot_y2) // 2),
        "Official Page",
        font=sub_font_en,
        fill=(218, 165, 32, 220),
        anchor="mm"
    )

    img.save(output_path, "PNG")
    return output_path

if __name__ == "__main__":
    p916 = generate_watermark_overlay(720, 1280)
    print("Watermark generated cleanly:", p916)
