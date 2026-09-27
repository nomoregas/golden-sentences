# Goldene Sätze

A small study app for English speakers learning German through "golden sentences": short sentences that reuse the same apple and a handful of people, so each one isolates a single grammar point.

48 sentences in three sets, each chosen to add something the others don't:

- **Ferriss core (13):** Tim Ferriss's original deconstruction sentences, verbatim.
- **Golden expansion (23):** from the 41 Golden Sentences, dropping the 18 that repeat Ferriss's originals or reuse another sentence's frame with one word swapped. Their small points live on in the notes.
- **Gap fillers (12):** grammar neither list covers: feminine and neuter nouns, kein, commands, formal Sie, two-way prepositions, Perfekt with sein, separable and reflexive verbs, relative clauses, time-before-place.

## Modes

- **Learn**: German words underlined by case (tap one for its meaning), a word-for-word gloss, a short note, a common mistake, and expandable grammar topics with tables.
- **Practice**: see the English and produce the German, typed or said aloud, with an optional hint, then grade yourself. Scheduling follows a Leitner card box (*Karteikasten*): box 1 comes back in 10 minutes, box 5 in 3 weeks.
- **Build**: put shuffled German words back in order, then see the sentence laid out in its frame (Vorfeld · verb · Mittelfeld · verb end), which is the model behind German word order.

Audio: every sentence and every word has a clip in `audio/`, embedded in the page so it plays anywhere, including in-app browsers with no speech voice. The committed clips use eSpeak NG with the MBROLA German voice (`de7`), which works offline but sounds robotic. For natural-sounding audio, run `python3 tools/make_audio.py --engine edge` on a machine with internet access: it uses Microsoft's neural German voices (the ones behind Edge's Read Aloud), needs no API key, and writes the same files. The Slow button plays clips at 70% speed. The browser's own voice is only a fallback for text without a clip.

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
build.js                inlines the data → dist/
```

## Build and run

```sh
python3 tools/make_data.py   # after editing sentences
python3 tools/make_audio.py --engine edge   # after editing sentences; pip install edge-tts
node build.js
open dist/index.html   # or any static host
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
