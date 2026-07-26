from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "og-suns-signal-003-burden-of-proof.png"
W, H = 1200, 630


def font(path, size):
    return ImageFont.truetype(str(path), size)


def cover_crop(img, size):
    src_w, src_h = img.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = img.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - dst_w) // 2
    top = (resized.height - dst_h) // 2
    return resized.crop((left, top, left + dst_w, top + dst_h))


FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
regular = font(FONT_REG, 28)
tiny = font(FONT_BOLD, 18)
label = font(FONT_BOLD, 25)
display = font(FONT_BOLD, 76)

cover = Image.open(ASSETS / "burden-of-proof-cover.png").convert("RGB")
cover = cover_crop(cover, (W, H)).filter(ImageFilter.GaussianBlur(0.5))
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.rectangle((0, 0, W, H), fill=(10, 13, 18, 92))
od.rectangle((0, 0, 735, H), fill=(10, 13, 18, 138))
od.line((70, 510, 1130, 510), fill=(241, 152, 67, 180), width=3)
for x in range(76, 640, 34):
    height = 12 + ((x * 11) % 68)
    od.line((x, 510, x, 510 - height), fill=(39, 200, 194, 95), width=2)

bg = Image.alpha_composite(cover.convert("RGBA"), overlay)
draw = ImageDraw.Draw(bg)
draw.text((68, 46), "SUNS SIGNAL WEEKLY 003", font=label, fill=(255, 255, 255, 248))
draw.text((70, 84), "SUNDAY EDITION  |  JULY 26, 2026", font=tiny, fill=(241, 152, 67, 245))
draw.text((68, 150), "The Burden", font=display, fill=(255, 255, 255, 255))
draw.text((68, 230), "of Proof", font=display, fill=(255, 255, 255, 255))
draw.text((72, 344), "Miles Bridges' Phoenix introduction,", font=regular, fill=(230, 234, 239, 238))
draw.text((72, 382), "the offseason ledger, and what comes next.", font=regular, fill=(230, 234, 239, 238))

chips = [("ACCOUNTABILITY", 72), ("BASKETBALL FIT", 278), ("CALENDAR AHEAD", 502)]
for text, x in chips:
    box = draw.textbbox((0, 0), text, font=tiny)
    width = box[2] - box[0] + 28
    draw.rounded_rectangle((x, 444, x + width, 485), radius=5, outline=(241, 152, 67, 165), fill=(19, 24, 32, 235))
    draw.text((x + 14, 455), text, font=tiny, fill=(255, 255, 255, 245))

team_logo = Image.open(ASSETS / "teams" / "suns" / "phoenix-suns-logo.png").convert("RGBA")
team_logo.thumbnail((112, 112), Image.Resampling.LANCZOS)
bg.alpha_composite(team_logo, (1020, 48))
draw = ImageDraw.Draw(bg)
draw.text((72, 548), "CURATED FOR MAT ISHBIA", font=tiny, fill=(241, 152, 67, 250))
draw.text((72, 580), "Prepared by Accelerated Velocity Consulting", font=tiny, fill=(215, 222, 232, 180))

bg.convert("RGB").save(OUT, quality=95)
print(OUT)
