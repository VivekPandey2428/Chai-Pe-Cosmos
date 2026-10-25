"""Pulls frames at given times from a video into one labelled contact sheet (for review before the final render)."""
import subprocess, sys, tempfile, os
from PIL import Image, ImageDraw, ImageFont
video, out, cols = sys.argv[1], sys.argv[2], int(sys.argv[3])
times = [float(x) for x in sys.argv[4].split(",")]
labels = sys.argv[5].split("|") if len(sys.argv) > 5 else [""] * len(times)
tmp = tempfile.mkdtemp()
w, h = 360, 640
ims = []
for i, t in enumerate(times):
    f = os.path.join(tmp, f"{i}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1", f], check=True)
    ims.append(Image.open(f).resize((w, h)))
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, (h + 44) * rows), "#1b1b2f")
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except OSError:
    font = None
for i, im in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * (h + 44)
    sheet.paste(im, (x, y))
    d.text((x + 8, y + h + 10), f"{times[i]:.1f}s  {labels[i]}", fill="white", font=font)
sheet.save(out, quality=88)
print(out)
