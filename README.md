# Goldene Sätze

A small study app for English speakers learning German through "golden sentences": short sentences that reuse the same apple and a handful of people, so each one isolates a single grammar point.

50 sentences in three sets, each chosen to add something the others don't:

- **Ferriss core (13):** Tim Ferriss's original deconstruction sentences, verbatim.
- **Golden expansion (23):** from the 41 Golden Sentences, dropping the 18 that repeat Ferriss's originals or reuse another sentence's frame with one word swapped. Their small points live on in the notes.
- **Gap fillers (14):** grammar neither list covers, including Anna (*Ich gebe Anna ihren Apfel*, the possessive *ihr*): feminine and neuter nouns, kein, commands, formal Sie, two-way prepositions, Perfekt with sein, separable and reflexive verbs, relative clauses, time-before-place.

## Install on your phone

The app is published to GitHub Pages at **https://nomoregas.github.io/golden-sentences/** and installs as an app (PWA) that works offline, audio included.

- **iPhone:** open the link in Safari → Share → **Add to Home Screen**.
- **Android:** open the link in Chrome → ⋮ menu → **Install app** (or **Add to Home screen**).

Progress is stored on the device, separately for the installed app and for any other copy of the page.

## One story, three genders

The whole story is about one object, and you can switch it: **der Apfel**, **die Birne** or **das Bonbon**. Every sentence, note, hint, common mistake, picture and recording follows the choice, so the same structures appear with masculine, feminine and neuter forms: *Ich muss ihn / sie / es ihm geben*, *keinen Apfel / keine Birne / kein Bonbon*, *Er ist nicht meiner / Sie ist nicht meine / Es ist nicht meins*. In Learn, **Compare** shows all three versions with the changed words highlighted.

Sentences are templates (`tools/sentences_src.py`) with placeholders such as `{den} {Apfel}` or `{ihn}`; `tools/make_data.py` fills them in for each gender and checks every version. Run `python3 tools/make_data.py --review` to print all versions for proofreading.

## Modes

**Learn**: a picture of the sentence, German words underlined by case (tap one for its meaning), a word-for-word gloss, a short note, a common mistake, and expandable grammar topics with tables.

**Table**: all 50 sentences at once, switchable between English, Deutsch and Both without losing your place. Tick the sentences you want to practise (or **All** / **None**); every drill uses only the ticked ones. Tap a sentence to peek at its translation, ▶ to hear it, or its number to open it in Learn.

Every sentence is tagged with the CEFR level of the grammar it centres on: **A1** (16), **A2** (22) or **B1** (12). They stop at B1 because B2 and C levels are about nuance and idiom rather than core sentence structure. The Table can group **By story** or **By level**, and each group has a *practise only these* link.

**Practice** opens a menu of drills. Each one is entered on its own, with its own progress, and shows what's due, new and solid:

| Drill | What you do |
|---|---|
| EN → DE (flash cards) | See the English, say the German, flip to check |
| DE → EN (flash cards) | Read the German, say what it means |
| Listen (flash cards) | Hear the sentence with no text, say what it means |
| Type it | Type the German and see it compared word by word |
| Build | Put shuffled German words back in order, then see the sentence frame (Vorfeld · verb · Mittelfeld · verb end), the model behind German word order |

The card drills work in rounds: each round goes through every selected sentence once (shuffled, or **In order**). **Again** puts the card back a few cards later in the same round, and **Got it** finishes it for the round. The progress grid (*Karteikasten*, "card box") shows how each sentence went the last time: green for got it, red for missed. Build tracks which sentences you've built correctly. Inside a drill, **Clear** resets that drill; the footer's **Reset all progress** resets everything.

Pictures: every sentence has a small scene (`data/scenes.json`, drawn as SVG by the app) with a fixed cast, each person in one colour: **ich** blue, **du** green, **er** teal, **sie** purple, **John** orange, **Anna** mustard, a child, and a formal **Sie**. The same marks recur: a dashed arrow for giving, ✗ for not, ? for questions, ! for must, ♥ for want, and a clock with an arrow back (past) or ahead (future). Pictures show in Learn and Build, on the front of EN → DE cards, and only on the back of DE → EN and Listen cards so they don't give the meaning away.

Audio: every sentence and every word has a clip in `audio/`, embedded in the page so it plays anywhere, including in-app browsers with no speech voice. The committed clips use Microsoft's neural German voice Katja (`de-DE-KatjaNeural`, the voices behind Edge's Read Aloud; no API key). To regenerate them, for example after editing sentences or to switch voice, run the **Generate audio** workflow from the repo's Actions tab, or `python3 tools/make_audio.py --engine edge` on any machine with internet access. `--engine mbrola` is an offline fallback that sounds robotic. The Slow button plays clips at 70% speed. The browser's own voice is only a fallback for text without a clip.

Progress is stored in the browser's `localStorage`.

## Layout

```
tools/sentences_src.py  sentence source: text, per-word gloss/case/slot, topics, note, hint, mistake
tools/make_data.py      validates the source and writes data/sentences.json
tools/make_audio.py     generates audio/ clips and audio/manifest.json
data/sentences.json     generated sentence data
data/topics.json        grammar topics: title, summary, explanation, optional table
data/scenes.json        one picture per sentence, as a list of cast members and props
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
