import os
import re
import json
import asyncio
import edge_tts
from dotenv import load_dotenv
from google import genai

load_dotenv()

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

os.makedirs("temp", exist_ok=True)

FALLBACK_LINES = [
    "If you were born on the 1st, 10th, 19th, or 28th, your money blueprint is wired for ownership.",
    "In Chaldean numerology, these dates carry the vibration of the Sun, Number 1.",
    "Number 1 minds rarely thrive in rigid routines where someone else caps their income.",
    "Your biggest financial breakthroughs happen when you build scalable assets instead of trading hours.",
    "Focus on one high-leverage skill, automate the repetitive work, and lead from the front.",
    "Follow The 28th Code to decode your numbers and master your financial architecture."
]

def get_script_lines():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found, using built-in script...")
        return FALLBACK_LINES

    client = genai.Client(api_key=api_key)
    prompt = f"""
    Write a punchy {config['target_duration_sec']}-second YouTube Short / Instagram Reel script.
    Brand: {config['brand_name']}
    Topic: {config['topic']}
    Niche: {config['niche']}
    Rules:
    - Return ONLY 6 to 7 short, high-retention sentences, one per line.
    - First line must be an irresistible 3-second scroll-stopping hook.
    - Last line must be a short CTA mentioning {config['brand_name']}.
    - No numbering, no emojis, no stage directions.
    """
    for model_name in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            res = client.models.generate_content(model=model_name, contents=prompt)
            lines = [re.sub(r"^[\d\-\*\.\s]+", "", l.strip()) for l in res.text.strip().split("\n") if l.strip()]
            if len(lines) >= 4:
                print(f"Script generated via {model_name}!")
                return lines[:7]
        except Exception as e:
            print(f"{model_name} skipped ({e})")
    print("Gemini quota active—using built-in test script so you can render immediately!")
    return FALLBACK_LINES

async def synthesize_voice(full_text):
    communicate = edge_tts.Communicate(
        full_text,
        config["voice"],
        rate=config.get("voice_rate", "+5%"),
        boundary="WordBoundary"
    )
    word_timings = []
    audio_path = os.path.join("temp", "voiceover.mp3")

    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = chunk["offset"] / 10_000_000
                dur_sec = chunk["duration"] / 10_000_000
                word_timings.append({
                    "word": chunk["text"],
                    "start": start_sec,
                    "end": start_sec + dur_sec
                })

    with open(os.path.join("temp", "timings.json"), "w", encoding="utf-8") as tf:
        json.dump(word_timings, tf, indent=2)
    print(f"Voiceover saved ({len(word_timings)} synced words).")

if __name__ == "__main__":
    lines = get_script_lines()
    full_script = " ".join(lines)
    with open(os.path.join("temp", "script.txt"), "w", encoding="utf-8") as sf:
        sf.write("\n".join(lines))
    asyncio.run(synthesize_voice(full_script))
