// Inlines data/sentences.json, data/topics.json and the audio clips into src/app.html.
//   dist/index.html    – standalone page and installable app (host dist/ anywhere, e.g. GitHub Pages)
//   dist/fragment.html – body-only version for hosts that supply their own <html> shell
const fs = require("fs");
const path = require("path");

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), "utf8");
const data = JSON.parse(read("data/sentences.json"));
const topics = JSON.parse(read("data/topics.json"));
const scenes = JSON.parse(read("data/scenes.json"));
delete scenes._about;
const noScene = data.sentences.filter(x => !scenes[x.key]).map(x => x.key);
if (noScene.length) console.warn(`No picture yet for: ${noScene.join(" ")}`);
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
  ["/*__SCENES__*/{}", scenes],
  ["/*__AUDIO__*/{ sentences: {}, words: {} }", audio],
]) {
  if (!fragment.includes(placeholder)) throw new Error(`Placeholder ${placeholder} not found in src/app.html`);
  fragment = fragment.replace(placeholder, () => JSON.stringify(value));
}

// dist/index.html is also an installable app (PWA): manifest, icons and an offline cache.
// The fragment stays plain, since hosts like Claude artifacts don't allow service workers.
const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1B2F5E">
<meta name="description" content="Learn German through golden sentences: flash cards, word order and grammar notes.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Goldene Sätze">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  body { margin: 0 }
  [hidden] { display: none !important }
</style>
</head>
<body>
${fragment}
<script>
if ("serviceWorker" in navigator && window.isSecureContext && location.protocol !== "file:") navigator.serviceWorker.register("sw.js");
</script>
</body>
</html>
`;

const dist = path.join(root, "dist");
fs.mkdirSync(path.join(dist, "icons"), { recursive: true });
fs.writeFileSync(path.join(dist, "index.html"), page);
fs.writeFileSync(path.join(dist, "fragment.html"), fragment);
const version = require("crypto").createHash("sha256").update(page).digest("hex").slice(0, 12);
fs.writeFileSync(path.join(dist, "sw.js"), read("web/sw.js").replace("__VERSION__", version));
fs.copyFileSync(path.join(root, "web/manifest.webmanifest"), path.join(dist, "manifest.webmanifest"));
for (const f of fs.readdirSync(path.join(root, "web/icons"))) {
  fs.copyFileSync(path.join(root, "web/icons", f), path.join(dist, "icons", f));
}
fs.writeFileSync(path.join(dist, ".nojekyll"), "");
console.log(`Built ${data.sentences.length} sentences, ${Object.keys(topics).length} topics, ${Object.keys(audio.sentences).length + Object.keys(audio.words).length} clips → dist/ (app ${version})`);
