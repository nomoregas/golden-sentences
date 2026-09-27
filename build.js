// Inlines data/sentences.json, data/topics.json and the audio clips into src/app.html.
//   dist/index.html    – standalone page (open directly in a browser, or host anywhere)
//   dist/fragment.html – body-only version for hosts that supply their own <html> shell
const fs = require("fs");
const path = require("path");

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), "utf8");
const data = JSON.parse(read("data/sentences.json"));
const topics = JSON.parse(read("data/topics.json"));
const app = read("src/app.html");

// Audio clips are embedded as data: URIs so the page works as a single file,
// including inside in-app browsers that have no built-in speech voice.
const audio = { sentences: {}, words: {} };
const manifestPath = path.join(root, "audio/manifest.json");
if (fs.existsSync(manifestPath)) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  for (const kind of ["sentences", "words"]) {
    for (const [text, file] of Object.entries(manifest[kind])) {
      audio[kind][text] = "data:audio/mpeg;base64," + fs.readFileSync(path.join(root, file)).toString("base64");
    }
  }
}

let fragment = app;
for (const [placeholder, value] of [
  ["/*__SENTENCES__*/{ sets: {}, sentences: [] }", data],
  ["/*__TOPICS__*/{}", topics],
  ["/*__AUDIO__*/{ sentences: {}, words: {} }", audio],
]) {
  if (!fragment.includes(placeholder)) throw new Error(`Placeholder ${placeholder} not found in src/app.html`);
  fragment = fragment.replace(placeholder, () => JSON.stringify(value));
}

const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>body{margin:0}[hidden]{display:none!important}</style>
</head>
<body>
${fragment}
</body>
</html>
`;

fs.mkdirSync(path.join(root, "dist"), { recursive: true });
fs.writeFileSync(path.join(root, "dist/index.html"), page);
fs.writeFileSync(path.join(root, "dist/fragment.html"), fragment);
console.log(`Built ${data.sentences.length} sentences, ${Object.keys(topics).length} topics, ${Object.keys(audio.sentences).length + Object.keys(audio.words).length} clips → dist/index.html, dist/fragment.html`);
