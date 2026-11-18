"""
Watermark Generator for 'কুরআনের তিলাওয়াত - Quran Tilawat'
Creates broadcast-grade, anti-aliased watermark overlays for both 9:16 (Reels) and 16:9 (Widescreen)
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

    # Load Bengali font if available, else fallback
    font_size = int(width * 0.038)
    sub_font_size = int(width * 0.024)

    if os.path.exists(FONT_PATH):
        try:
            font = ImageFont.truetype(FONT_PATH, font_size)
            sub_font = ImageFont.truetype(FONT_PATH, sub_font_size)
        except Exception:
            font = ImageFont.load_default()
            sub_font = font
    else:
        font = ImageFont.load_default()
        sub_font = font

    # Top Watermark Badge
    pill_w = int(width * 0.68)
    pill_h = int(height * 0.045)
    pill_x1 = (width - pill_w) // 2
    pill_y1 = int(height * 0.035)
    pill_x2 = pill_x1 + pill_w
    pill_y2 = pill_y1 + pill_h

    # Rounded translucent dark pill with golden border
    draw.rounded_rectangle(
        [(pill_x1, pill_y1), (pill_x2, pill_y2)],
        radius=int(pill_h / 2),
        fill=(10, 15, 30, 200),
        outline=(218, 165, 32, 230),
        width=2
    )

    # Watermark Text: কুরআনের তিলাওয়াত • Quran Tilawat
    title_text = "কুরআনের তিলাওয়াত  •  Quran Tilawat"
    draw.text(
        ((pill_x1 + pill_x2) // 2, (pill_y1 + pill_y2) // 2),
        title_text,
        font=font,
        fill=(255, 255, 255, 245),
        anchor="mm"
    )

    # Bottom Right subtle branding badge
    bot_w = int(width * 0.45)
    bot_h = int(height * 0.032)
    bot_x1 = width - bot_w - int(width * 0.03)
    bot_y1 = height - bot_h - int(height * 0.03)
    bot_x2 = bot_x1 + bot_w
    bot_y2 = bot_y1 + bot_h

    draw.rounded_rectangle(
        [(bot_x1, bot_y1), (bot_x2, bot_y2)],
        radius=int(bot_h / 2),
        fill=(0, 0, 0, 160)
    )
    draw.text(
        ((bot_x1 + bot_x2) // 2, (bot_y1 + bot_y2) // 2),
        "📖 @QuranTilawatOfficial",
        font=sub_font,
        fill=(218, 165, 32, 220),
        anchor="mm"
    )

    img.save(output_path, "PNG")
    return output_path

if __name__ == "__main__":
    p916 = generate_watermark_overlay(720, 1280)
    p169 = generate_watermark_overlay(1280, 720)
    print("Watermarks generated:", p916, p169)
