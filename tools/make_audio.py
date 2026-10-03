"""Generate audio/ clips for every sentence and every distinct word.

Two engines, same output (audio/s/<key>.mp3, audio/w/<n>.mp3, audio/manifest.json),
which build.js inlines into the page:

  edge   Microsoft's neural voices (what Edge's Read Aloud uses). Natural-sounding,
         no API key, needs internet access and a WebSocket connection.
             pip install edge-tts
             python3 tools/make_audio.py --engine edge
  mbrola Offline, robotic but accurate. Used for the clips currently committed.
             sudo apt-get install espeak-ng mbrola mbrola-de7 lame
             python3 tools/make_audio.py --engine mbrola

Human recordings can replace any file directly; the manifest maps text to file.
"""
import argparse
import asyncio
import json
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
out = root / "audio"

ap = argparse.ArgumentParser()
ap.add_argument("--engine", choices=["edge", "mbrola"], default="edge")
ap.add_argument("--voice", help="edge: e.g. de-DE-KatjaNeural (default), de-DE-ConradNeural; mbrola: mb-de7 (default), mb-de6")
args = ap.parse_args()
voice = args.voice or ("de-DE-KatjaNeural" if args.engine == "edge" else "mb-de7")


def synth_mbrola(text, dest):
    with tempfile.NamedTemporaryFile(suffix=".wav") as wav:
        subprocess.run(["espeak-ng", "-v", voice, "-s", "135", "-w", wav.name, text], check=True)
        subprocess.run(["lame", "--quiet", "-m", "m", "-b", "40", wav.name, str(dest)], check=True)


async def synth_edge(text, dest):
    import edge_tts
    # A slightly slower rate suits learners; the app's Slow button slows it further.
    await edge_tts.Communicate(text, voice, rate="-10%").save(str(dest))


async def main():
    data = json.loads((root / "data/sentences.json").read_text(encoding="utf-8"))
    (out / "s").mkdir(parents=True, exist_ok=True)
    (out / "w").mkdir(parents=True, exist_ok=True)
    # Every version of every sentence: der Apfel (the sentence itself) plus the Birne/Bonbon versions in "alt".
    versions = []
    for x in data["sentences"]:
        versions.append((x["key"], x["de"], x["tokens"]))
        for g, alt in x.get("alt", {}).items():
            if "de" in alt:
                versions.append((f"{x['key']}-{g}", alt["de"], alt["tokens"]))
    jobs = [(de, out / "s" / f"{name}.mp3", "sentences") for name, de, _ in versions]
    words = sorted({t["w"].rstrip(",") for _, _, toks in versions for t in toks})
    jobs += [(w, out / "w" / f"{i:03d}.mp3", "words") for i, w in enumerate(words, 1)]

    manifest = {"engine": args.engine, "voice": voice, "sentences": {}, "words": {}}
    for n, (text, dest, kind) in enumerate(jobs, 1):
        if args.engine == "edge":
            await synth_edge(text, dest)
        else:
            synth_mbrola(text, dest)
        manifest[kind][text] = dest.relative_to(root).as_posix()
        print(f"\r{n}/{len(jobs)}", end="", flush=True)
    print()

    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    size = sum(p.stat().st_size for p in out.rglob("*.mp3"))
    for old in (out / "s").glob("*.mp3"):     # drop clips for sentences that no longer exist
        if old.relative_to(root).as_posix() not in manifest["sentences"].values():
            old.unlink()
    print(f"{len(manifest['sentences'])} sentence clips, {len(words)} word clips, {size / 1024:.0f} KB ({args.engine}, {voice})")


asyncio.run(main())
