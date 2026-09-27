// Inlines data/sentences.json into src/app.html.
//   dist/index.html    – standalone page (open directly in a browser, or host anywhere)
//   dist/fragment.html – body-only version for hosts that supply their own <html> shell
const fs = require("fs");
const path = require("path");

const root = __dirname;
const sentences = JSON.parse(fs.readFileSync(path.join(root, "data/sentences.json"), "utf8"));
const app = fs.readFileSync(path.join(root, "src/app.html"), "utf8");
const fragment = app.replace("/*__SENTENCES__*/[]", JSON.stringify(sentences));
if (fragment === app) throw new Error("Data placeholder not found in src/app.html");

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
console.log(`Built ${sentences.length} sentences → dist/index.html, dist/fragment.html`);
