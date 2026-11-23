import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, AudioFileClip

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open(os.path.join("temp", "timings.json"), "r", encoding="utf-8") as f:
    timings = json.load(f)

audio = AudioFileClip(os.path.join("temp", "voiceover.mp3"))
DURATION = audio.duration + 0.6
W, H = 1080, 1920

# Load bold Windows font with clean fallback
def get_font(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/calibrib.ttf"
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

TITLE_FONT = get_font(42)
CAPTION_FONT = get_font(74)
SMALL_FONT = get_font(34)

# Group words into 3-word punchy caption chunks
CHUNKS = []
for i in range(0, len(timings), 3):
    group = timings[i:i+3]
    CHUNKS.append({
        "words": group,
        "start": group[0]["start"],
        "end": group[-1]["end"] + 0.15
    })

def make_frame(t):
    # Deep Obsidian background (#0B0D12)
    img = Image.new("RGB", (W, H), (11, 13, 18))
    draw = ImageDraw.Draw(img)

    # Subtle gold accent frame & top brand header
    draw.rectangle([48, 80, W - 48, H - 120], outline=(45, 40, 28), width=2)
    brand = config.get("brand_name", "THE 28TH CODE").upper()
    bbox = draw.textbbox((0, 0), brand, font=TITLE_FONT)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, 140), brand, font=TITLE_FONT, fill=(212, 175, 55))

    # Animated gold progress bar along the bottom
    progress = min(1.0, max(0.0, t / DURATION))
    draw.rectangle([80, H - 180, W - 80, H - 168], fill=(30, 34, 45))
    draw.rectangle([80, H - 180, 80 + int((W - 160) * progress), H - 168], fill=(212, 175, 55))

    # Find active 3-word caption group
    active_chunk = None
    for ch in CHUNKS:
        if ch["start"] <= t <= ch["end"]:
            active_chunk = ch
            break

    if active_chunk:
        words = active_chunk["words"]
        y_start = (H // 2) - (len(words) * 55)
        for idx, w_info in enumerate(words):
            word_text = w_info["word"].upper()
            is_active = w_info["start"] <= t <= (w_info["end"] + 0.08)
            color = (245, 197, 66) if is_active else (240, 242, 245)  # Metallic Gold vs Platinum White

            wb = draw.textbbox((0, 0), word_text, font=CAPTION_FONT)
            ww = wb[2] - wb[0]
            x = (W - ww) // 2
            y = y_start + (idx * 110)

            # Drop shadow for crisp readability
            draw.text((x + 4, y + 4), word_text, font=CAPTION_FONT, fill=(0, 0, 0))
            draw.text((x, y), word_text, font=CAPTION_FONT, fill=color)

    return np.array(img)

print("Rendering 1080x1920 Full HD Short...")
os.makedirs("output", exist_ok=True)
out_path = os.path.join("output", "short_01.mp4")

clip = VideoClip(make_frame, duration=DURATION).with_audio(audio)
clip.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", logger="bar")
print(f"Done! Video saved to {out_path}")
