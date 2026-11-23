
# Shorts Auto Studio

Automated local Python pipeline for generating 1080x1920 vertical YouTube Shorts and Instagram Reels using Google Gemini, Edge TTS neural voiceovers, and Pillow + MoviePy kinetic word-highlighted captions.

## Features
- **Automated Script Generation:** Uses Gemini (`gemini-2.5-flash` / `gemini-2.0-flash`) with built-in fallback scripts so rendering never stalls on API rate limits.
- **Free Neural Voiceovers & Word Sync:** Uses `edge-tts` (`WordBoundary` events) to generate studio-grade `.mp3` audio and exact per-word timestamps without extra API keys.
- **1080x1920 Obsidian & Gold Renderer:** Renders crisp Full HD vertical videos with active word-by-word gold highlighting and progress tracking.

## Project Structure
```text
shorts-auto-studio/
├── generate_script.py  # Generates hook script + edge-tts audio & word timings
├── render_video.py     # Renders 1080x1920 obsidian & gold kinetic caption MP4
├── config.json         # Brand name, topic, niche, voice, and duration settings
├── requirements.txt    # Python dependencies
├── assets/             # Optional background clips/assets
├── temp/               # Generated voiceover.mp3, script.txt, timings.json (excluded from Git)
└── output/             # Final rendered short_01.mp4 videos (excluded from Git)
Setup & Usage
Install dependencies:

pip install -r requirements.txt

Configure API key & settings:
Add GEMINI_API_KEY=your_key_here to .env, edit config.json, and run:

python generate_script.py
python render_video.py

The final video is exported to output/short_01.mp4.


## requirements.txt

```text
edge-tts
pillow
moviepy
google-genai
python-dotenv

