#!/usr/bin/env python3
"""Composite the GTA 6 meme: base scene + real make.fun ghost + captions.
Output: /home/hatch/workspace/makefun/gta6-meme-x-/meme.png (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = "/home/hatch/workspace/makefun/gta6-meme-x-/"
BASE = REPO + "media-generation-base-scene-0-b270d047-fb44-4e1f-9df1-f621c1bd6ada.png"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-x-assets/mark-1024.png"
OUT = REPO + "meme.png"

FONT_COND = "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBold.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

W = H = 1024

# 1. Base: center-crop to square, resize to 1024x1024
base = Image.open(BASE).convert("RGB")
bw, bh = base.size
side = min(bw, bh)
left = (bw - side) // 2
top = (bh - side) // 2
img = base.crop((left, top, left + side, top + side)).resize((W, H), Image.LANCZOS).convert("RGBA")

# 2. Legibility gradients: darken top (captions) and bottom (caption) bands
overlay = Image.new("L", (W, H), 0)
od = ImageDraw.Draw(overlay)
for y in range(0, 270):
    od.line([(0, y), (W, y)], fill=int(85 * (1 - y / 270)))
for y in range(830, H):
    od.line([(0, y), (W, y)], fill=int(95 * ((y - 830) / (H - 830))))
black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
img = Image.composite(black, img, overlay)

d = ImageDraw.Draw(img)

def caption(text, y, size, stroke=8):
    f = ImageFont.truetype(FONT_COND, size)
    d.text((W // 2, y), text, font=f, fill="white", anchor="ma",
           stroke_width=stroke, stroke_fill="black")

# 3. Captions (huge, readable at 480x480)
caption("WAITED 13 YEARS", 22, 108)
caption("FOR GTA 6", 132, 108)
caption("DOWNLOAD STILL AT 99%", 912, 84, stroke=7)

# 4. Real make.fun ghost, lower-left, large (260px), with drop shadow
ghost = Image.open(GHOST).convert("RGBA").resize((260, 260), Image.LANCZOS)
gx, gy = 18, 600
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
alpha = ghost.split()[3]
sh.putalpha(alpha.point(lambda a: int(a * 0.75)))
sh = sh.filter(ImageFilter.GaussianBlur(7))
shadow.paste(sh, (gx + 9, gy + 11), sh)
img = Image.alpha_composite(img, shadow)
img.paste(ghost, (gx, gy), ghost)

# 5. Speech bubble, right of the ghost, tail pointing down-left to it
bx0, by0, bx1, by1 = 300, 428, 724, 562
d = ImageDraw.Draw(img)
d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill="white",
                    outline="#111111", width=5)
# tail: triangle from bubble bottom edge to the ghost
d.polygon([(392, by1 - 2), (452, by1 - 2), (300, 640)], fill="white",
          outline="#111111")
d.line([(392, by1 - 2), (300, 640)], fill="#111111", width=5)
d.line([(452, by1 - 2), (300, 640)], fill="#111111", width=5)
# cover the tail's top edge so the bubble edge stays clean
d.line([(392, by1 - 2), (452, by1 - 2)], fill="white", width=5)
bf = ImageFont.truetype(FONT_BOLD, 31)
lines = ["My agent already", "got paid", "on make.fun"]
ly = by0 + 14
for ln in lines:
    d.text(((bx0 + bx1) // 2, ly), ln, font=bf, fill="#14142b", anchor="ma")
    ly += 40

img.convert("RGB").save(OUT, "PNG")
print("saved", OUT, img.size)
