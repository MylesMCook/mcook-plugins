// Explainer builder. Needs only Node 18+, no npm install.
//   node build.mjs                      build every topics/*.json into dist/ (the "home" topic at dist/index.html, others at dist/<id>/)
//   node build.mjs my-topic.json        build one topic into my-topic.html, a single self-contained file
//   node build.mjs my-topic.json --out page.html
//   node build.mjs --check [file.json]  only validate
// Every page embeds its fonts, styles, player and topic, so it works opened straight from disk.
import { writeFileSync, mkdirSync, rmSync, readdirSync, readFileSync, existsSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { validate, render, stats, keepPrevious } from "./kit.mjs";

const root = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const checkOnly = args.includes("--check");
const outIdx = args.indexOf("--out");
const outArg = outIdx >= 0 ? args[outIdx + 1] : null;
const fileArg = args.find((a, i) => a.endsWith(".json") && !(outIdx >= 0 && i === outIdx + 1));

function load(path) {
  try { return JSON.parse(readFileSync(path, "utf8")); } catch (e) { console.error(`${path}: not valid JSON: ${e.message}`); process.exit(1); }
}
function fail(errors) { console.error(`Topic problems (${errors.length}):\n- ` + errors.join("\n- ")); process.exit(1); }
const count = (t) => { const s = stats(t); return `${s.lessons} lessons, ${s.messages} messages`; };

if (fileArg) {
  // one topic → one file
  const t = load(fileArg), errors = validate(t, fileArg);
  if (errors.length) fail(errors);
  console.log(`ok  ${fileArg}  ${count(t)}`);
  if (checkOnly) process.exit(0);
  const out = resolve(outArg || fileArg.replace(/\.json$/, ".html"));
  const html = render(t);
  if (existsSync(out) && readFileSync(out, "utf8") === html) { console.log(`unchanged ${out}`); process.exit(0); }
  if (existsSync(out)) console.log(`previous page kept: ${keepPrevious(out)} (it embeds the previous topic)`);
  writeFileSync(out, html);
  console.log(`built ${out}`);
  process.exit(0);
}

const topicsDir = join(root, "topics");
const topics = readdirSync(topicsDir).filter((f) => f.endsWith(".json")).sort().map((f) => ({ f, t: load(join(topicsDir, f)) }));
const errors = topics.flatMap(({ f, t }) => validate(t, "topics/" + f));
if (topics.length && topics.filter(({ t }) => t.home).length !== 1) errors.push(`exactly one topic needs "home": true`);
if (new Set(topics.map(({ t }) => t.id)).size !== topics.length) errors.push("two topics share an id");
if (errors.length) fail(errors);
for (const { f, t } of topics) console.log(`ok  topics/${f}  ${count(t)}`);
if (checkOnly) process.exit(0);

const out = join(root, "dist");
rmSync(out, { recursive: true, force: true });
for (const { t } of topics) {
  const dir = t.home ? out : join(out, t.id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), render(t));
  console.log(`built ${t.home ? "dist/index.html" : `dist/${t.id}/index.html`}`);
}
