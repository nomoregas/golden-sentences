"""Draw the app icons into web/icons/. Needs Pillow: pip install pillow"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
out = root / "web/icons"
out.mkdir(parents=True, exist_ok=True)
NAVY, RED, WHITE, GRID = (27, 47, 94), (210, 69, 58), (255, 255, 255), (43, 64, 112)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def draw(size, safe=1.0):
    """safe < 1 shrinks the letter into the centre for maskable icons, which get cropped to a circle."""
    img = Image.new("RGB", (size, size), NAVY)
    d = ImageDraw.Draw(img)
    step = size / 8                      # faint squared-paper grid, like a German Schulheft
    for i in range(1, 8):
        d.line([(i * step, 0), (i * step, size)], fill=GRID, width=max(1, size // 256))
        d.line([(0, i * step), (size, i * step)], fill=GRID, width=max(1, size // 256))
    x = size * (0.5 - 0.30 * safe)       # red margin line
    d.rectangle([x, 0, x + max(2, size * 0.022), size], fill=RED)
    font = ImageFont.truetype(FONT, int(size * 0.62 * safe))
    box = d.textbbox((0, 0), "Ä", font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text((size * 0.56 - w / 2 - box[0], size * 0.53 - h / 2 - box[1]), "Ä", font=font, fill=WHITE)
    return img


draw(192).save(out / "icon-192.png")
draw(512).save(out / "icon-512.png")
draw(512, safe=0.78).save(out / "icon-maskable-512.png")
draw(180).save(out / "apple-touch-icon.png")
print("icons:", sorted(p.name for p in out.iterdir()))
