"""Generate audio/ clips for every sentence and every distinct word.

Needs espeak-ng, the MBROLA German voice and lame:
    sudo apt-get install espeak-ng mbrola mbrola-de7 lame
    python3 tools/make_audio.py

Writes audio/s/<key>.mp3, audio/w/<n>.mp3 and audio/manifest.json, which
build.js inlines into the page. Swap VOICE or replace files with human
recordings; the manifest maps text to file, so nothing else changes.
"""
import json
import subprocess
import tempfile
from pathlib import Path

VOICE = "mb-de7"   # MBROLA German female; mb-de6 is male
SPEED = "135"      # words per minute; the app's Slow button lowers playback rate further
BITRATE = "40"     # kbps, mono

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "data/sentences.json").read_text(encoding="utf-8"))
out = root / "audio"
(out / "s").mkdir(parents=True, exist_ok=True)
(out / "w").mkdir(parents=True, exist_ok=True)


def synth(text, dest):
    with tempfile.NamedTemporaryFile(suffix=".wav") as wav:
        subprocess.run(["espeak-ng", "-v", VOICE, "-s", SPEED, "-w", wav.name, text], check=True)
        subprocess.run(["lame", "--quiet", "-m", "m", "-b", BITRATE, wav.name, str(dest)], check=True)


manifest = {"voice": VOICE, "sentences": {}, "words": {}}
for s in data["sentences"]:
    f = out / "s" / f"{s['key']}.mp3"
    synth(s["de"], f)
    manifest["sentences"][s["de"]] = f.relative_to(root).as_posix()

words = sorted({t["w"].rstrip(",") for s in data["sentences"] for t in s["tokens"]})
for i, w in enumerate(words, 1):
    f = out / "w" / f"{i:03d}.mp3"
    synth(w, f)
    manifest["words"][w] = f.relative_to(root).as_posix()

(out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
size = sum(p.stat().st_size for p in out.rglob("*.mp3"))
print(f"{len(manifest['sentences'])} sentence clips, {len(words)} word clips, {size / 1024:.0f} KB")
