# Goldene Sätze

A small study app for English speakers learning German through "golden sentences": short sentences that reuse the same apple and a handful of people, so each one isolates a single grammar point.

48 sentences in three sets, each chosen to add something the others don't:

- **Ferriss core (13):** Tim Ferriss's original deconstruction sentences, verbatim.
- **Golden expansion (23):** from the 41 Golden Sentences, dropping the 18 that repeat Ferriss's originals or reuse another sentence's frame with one word swapped. Their small points live on in the notes.
- **Gap fillers (12):** grammar neither list covers: feminine and neuter nouns, kein, commands, formal Sie, two-way prepositions, Perfekt with sein, separable and reflexive verbs, relative clauses, time-before-place.

## Install on your phone

The app is published to GitHub Pages at **https://nomoregas.github.io/golden-sentences/** and installs as an app (PWA) that works offline, audio included.

- **iPhone:** open the link in Safari → Share → **Add to Home Screen**.
- **Android:** open the link in Chrome → ⋮ menu → **Install app** (or **Add to Home screen**).

Progress is stored on the device, separately for the installed app and for any other copy of the page.

## Modes

- **Learn**: German words underlined by case (tap one for its meaning), a word-for-word gloss, a short note, a common mistake, and expandable grammar topics with tables.
- **Practice**: flash cards by default, with three fronts: English (say it in German), German (what does it mean?) or Listen (audio only). Cards come in random order (or **In order**, 1 → 48). Tap to flip, then grade yourself. A Type it mode compares a typed answer word by word. Scheduling follows a Leitner card box (*Karteikasten*): box 1 comes back in 10 minutes, box 5 in 3 weeks, and each grade button shows when the card will return. Each practice type (EN → DE, DE → EN, Listen, Type it) keeps its own progress, with a Clear button for the current type and Reset all progress in the footer.
- **Build**: put shuffled German words back in order (sentences are dealt from a shuffled deck, each once per round, or in order), then see the sentence laid out in its frame (Vorfeld · verb · Mittelfeld · verb end), which is the model behind German word order.

Audio: every sentence and every word has a clip in `audio/`, embedded in the page so it plays anywhere, including in-app browsers with no speech voice. The committed clips use Microsoft's neural German voice Katja (`de-DE-KatjaNeural`, the voices behind Edge's Read Aloud; no API key). To regenerate them, for example after editing sentences or to switch voice, run the **Generate audio** workflow from the repo's Actions tab, or `python3 tools/make_audio.py --engine edge` on any machine with internet access. `--engine mbrola` is an offline fallback that sounds robotic. The Slow button plays clips at 70% speed. The browser's own voice is only a fallback for text without a clip.

Progress is stored in the browser's `localStorage`.

## Layout

```
tools/sentences_src.py  sentence source: text, per-word gloss/case/slot, topics, note, hint, mistake
tools/make_data.py      validates the source and writes data/sentences.json
tools/make_audio.py     generates audio/ clips and audio/manifest.json
data/sentences.json     generated sentence data
data/topics.json        grammar topics: title, summary, explanation, optional table
audio/                  sentence and word clips (MP3), plus manifest.json
src/app.html            the app (HTML/CSS/JS, no framework)
web/                    PWA files: manifest, service worker, icons
tools/make_icons.py     draws web/icons/ (needs Pillow)
build.js                inlines the data → dist/, adds the PWA files
.github/workflows/      pages.yml publishes dist/ on every push; audio.yml regenerates the clips
```

## Build and run

```sh
python3 tools/make_data.py   # after editing sentences
python3 tools/make_audio.py --engine edge   # after editing sentences; pip install edge-tts
node build.js
python3 -m http.server -d dist   # then open http://localhost:8000
```

No dependencies. `dist/` is generated output and isn't committed.

## Data model

Each sentence carries the extra information different screens need:

| Field | Used on |
|---|---|
| `tokens[]`: word, English gloss, case (N/A/D/G/verb), sentence slot | Learn (case colours, tap-for-meaning, word-for-word line), Build (sentence frame) |
| `topics[]` → `topics.json` | Learn (expandable explanations and tables) |
| `note` | all screens, after the answer |
| `hint` | Practice, before the answer |
| `mistake` (optional): a typical wrong version and why | Learn, Practice and Build, after the answer |

`make_data.py` checks that the tokens rebuild each sentence exactly, slots are in order, and every topic exists and is used.
