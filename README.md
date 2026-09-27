# Goldene Sätze

A small study app for English speakers learning German through the **41 Golden Sentences**, an expanded version of Tim Ferriss's sentence-deconstruction method. Every sentence reuses the same apple and a handful of people, so each new one isolates a single grammar point: cases, verb position, modal verbs, tenses, adjective endings.

## Modes

- **Learn**: step through the 41 sentences with English, German, a grammar tag and a short note. Audio uses the browser's German text-to-speech voice.
- **Practice**: see the English and produce the German, typed or said aloud, then grade yourself. Scheduling follows a Leitner card box (*Karteikasten*): box 1 comes back in 10 minutes, box 5 in 3 weeks.
- **Build**: put shuffled German words back in order to drill word order (verb-second, verb-final, pronoun order).

Progress is stored in the browser's `localStorage`.

## Layout

```
data/sentences.json   the 41 sentences: en, de, grammar tag, note
src/app.html          the app (HTML/CSS/JS, no framework)
build.js              inlines the data → dist/
```

## Build and run

```sh
node build.js
open dist/index.html   # or any static host
```

No dependencies. `dist/` is generated output and isn't committed.
