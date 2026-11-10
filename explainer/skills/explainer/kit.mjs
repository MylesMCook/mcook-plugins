// Shared by build.mjs (command line) and mcp.mjs (MCP server): topic validation and page rendering.
import { readFileSync, existsSync, mkdirSync, copyFileSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { unknownFields } from "./schema-keys.mjs";

const root = dirname(fileURLToPath(import.meta.url));
export const KIT_VERSION = JSON.parse(readFileSync(join(root, "package.json"), "utf8")).version;


// Presets fix the words a kind of explainer uses, so every explainer of that kind reads the same.
// A topic's own kinds, labels, riskLabel and groups override the preset's.
export const PRESETS = {
  protocol: {
    kinds: { req: "Request", res: "Response", err: "Error", note: "Notice", http: "Network", host: "Internal" },
    labels: { flow: "Message flow", message: "Message", method: "Method", info: "Info" },
    riskLabel: "Attack surface",
  },
  incident: {
    kinds: { req: "Request", res: "Result", err: "Failure", note: "Notice", http: "Storage", host: "Inside" },
    labels: { flow: "What happened, in order", message: "Detail", method: "Action", info: "Info" },
    riskLabel: "Caveat",
    groups: [{ id: "cause", title: "What happened" }, { id: "fix", title: "Proving and fixing it" }, { id: "after", title: "After the fix", separate: true }],
  },
  process: {
    kinds: { req: "Ask", res: "Reply", err: "Problem", note: "Notice", http: "Hand-off", host: "Inside" },
    labels: { flow: "What happens, in order", message: "Detail", method: "Action", info: "Info" },
    riskLabel: "Watch out",
  },
};
export function applyPreset(t) {
  const p = PRESETS[t && t.preset];
  if (!p) return t;
  return { ...t, kinds: { ...p.kinds, ...t.kinds }, labels: { ...p.labels, ...t.labels }, riskLabel: t.riskLabel || p.riskLabel, groups: t.groups || p.groups };
}

// Words that add length without meaning. Plain-language rule from TOPIC-GUIDE.md "Writing".
const FILLER = /\b(seamless(ly)?|robust|leverag(e|es|ing)|utiliz(e|es|ing)|facilitat(e|es|ing)|cutting-edge|state-of-the-art|best-in-class|delve|in order to|it is important to note|it's worth noting|at this point in time|in conclusion|successfully|essentially|basically)\b/i;

export function validate(topic, file) {
  const errs = [], at = (p, m) => errs.push(`${file} → ${p}: ${m}`);
  for (const e of unknownFields(topic)) errs.push(`${file} → ${e.replace(/^topic\.?/, "")}`); // misspelled fields would otherwise be silently ignored
  const t = applyPreset(topic);
  const isStr = (v) => typeof v === "string" && v.trim() !== "";
  const words = (s) => s.trim().split(/\s+/).length;
  // Direct text, no blobs: short fields, short sentences, no filler. Limits are in TOPIC-GUIDE.md "Writing".
  const prose = (p, s, max) => {
    if (!isStr(s)) return;
    if (s.length > max) at(p, `${s.length} characters; keep it under ${max}. Cut what the reader doesn't need, or use bullet points`);
    const long = s.split(/(?<=[.!?])\s+/).find((x) => words(x) > 20);
    if (long) at(p, `a ${words(long)}-word sentence ("${long.slice(0, 40)}…"); split it or cut it (20 words max)`);
    const f = s.match(FILLER);
    if (f) at(p, `"${f[0]}" is filler; say it plainly or cut it`);
  };
  // a summary is one or two short sentences, or 2 to 4 bullet points
  const summary = (p, s) => {
    if (!Array.isArray(s)) return prose(p, s, 160);
    if (s.length < 2 || s.length > 4) at(p, `${s.length} point${s.length === 1 ? "" : "s"}; use 2 to 4, or one short sentence instead`);
    s.forEach((x, i) => (isStr(x) ? prose(`${p}[${i}]`, x, 90) : at(`${p}[${i}]`, "empty point")));
  };
  const { lead, facts } = t.intro || {};
  prose("intro.lead", lead, 180);
  (Array.isArray(facts) ? facts : []).forEach((f, i) => prose(`intro.facts[${i}]`, f && f[1], 80));
  for (const [k, r] of Object.entries(t.risks || {})) prose(`risks.${k}.text`, r.text, 140);
  if ((facts || []).length > 5) at("intro.facts", "more than 5 key terms; keep the ones a newcomer needs first");
  if (!isStr(t.id) || !/^[a-z0-9-]+$/.test(t.id)) at("id", "needs a lowercase id like \"mcp\" (letters, digits, dashes)");
  if (!isStr(t.title)) at("title", "missing");
  if (!t.actors || typeof t.actors !== "object") at("actors", "missing the actor catalogue");
  if (!Array.isArray(t.lessons) || !t.lessons.length) { at("lessons", "needs at least one lesson"); return errs; }
  const ids = new Set();
  for (const l of t.lessons) { if (ids.has(l.id)) at(`lessons.${l.id}`, "duplicate lesson id"); ids.add(l.id); }
  const intro = t.intro || {};
  if (intro.lesson && !ids.has(intro.lesson)) at("intro.lesson", `no lesson "${intro.lesson}"`);
  if (!intro.start || !ids.has(intro.start)) at("intro.start", `must name a lesson id (got "${intro.start}")`);
  for (const [label, href] of intro.jump || []) if (!String(href).startsWith("#") || !ids.has(String(href).slice(1).split(/[:@]/)[0])) at(`intro.jump "${label}"`, `link "${href}" is not #<lesson id>`);
  const groups = new Set((t.groups || []).map((g) => g.id));
  const vers = t.versions ? t.versions.list.map((v) => v.id) : null;
  if (vers && !vers.includes(t.versions.current)) at("versions.current", "not in versions.list");
  for (const [k, a] of Object.entries(t.actors || {})) if (!isStr(a.label)) at(`actors.${k}.label`, "missing");
  const checkLesson = (l, p) => {
    if (!isStr(l.code) || !isStr(l.name)) at(p, "needs code (short title) and name (one-line subtitle)");
    summary(`${p}.summary`, l.summary);
    (Array.isArray(l.facts) ? l.facts : []).forEach((f, i) => prose(`${p}.facts[${i}]`, f && f[1], 80));
    prose(`${p}.aside`, l.aside && l.aside.text, 140);
    if (l.id !== intro.lesson && t.groups && !groups.has(l.group)) at(`${p}.group`, `"${l.group}" is not in groups`);
    if (!Array.isArray(l.actors) || !l.actors.length) { at(`${p}.actors`, "missing"); return; }
    const act = new Set();
    for (const a of l.actors) {
      if (!t.actors[a.id] && !(a.label && a.icon)) at(`${p}.actors.${a.id}`, "not in the actor catalogue (or give label + icon here)");
      if (typeof a.x !== "number" || typeof a.y !== "number") at(`${p}.actors.${a.id}`, "needs numeric x and y (canvas is 1000 × 560)");
      else if (a.x < 60 || a.x > 940 || a.y < 60 || a.y > 520) at(`${p}.actors.${a.id}`, `x ${a.x}, y ${a.y} is too close to the edge (keep x 60–940, y 60–520)`);
      act.add(a.id);
    }
    for (let i = 0; i < l.actors.length; i++) for (let j = i + 1; j < l.actors.length; j++) {
      const a = l.actors[i], b = l.actors[j], gap = Math.round(Math.hypot(a.x - b.x, a.y - b.y));
      if (gap < 150) at(`${p}.actors`, `"${a.id}" and "${b.id}" are ${gap} px apart and will overlap; keep at least 150 px (about 300 in a row, 260 between rows)`);
    }
    for (const z of l.zones || []) for (const id of z.ids || []) if (!act.has(id)) at(`${p}.zones "${z.label}"`, `"${id}" is not an actor in this lesson`);
    for (const k of Object.keys(l.wires || {})) for (const id of k.split("|")) if (!act.has(id)) at(`${p}.wires "${k}"`, `"${id}" is not an actor in this lesson`);
    if (!Array.isArray(l.steps) || !l.steps.length) { at(`${p}.steps`, "needs at least one step"); return; }
    l.steps.forEach((s, si) => {
      const sp = `${p}.steps[${si}]`;
      if (!isStr(s.title) || !isStr(s.desc)) at(sp, "needs title and desc");
      else if (words(s.title) > 3) at(`${sp}.title`, `"${s.title}" is long; use one or two words`);
      prose(`${sp}.desc`, s.desc, 120);
      (s.msgs || []).forEach((m, mi) => {
        const mp = `${sp}.msgs[${mi}]`;
        if (!act.has(m.from)) at(mp, `from "${m.from}" is not an actor in this lesson`);
        if (!act.has(m.to)) at(mp, `to "${m.to}" is not an actor in this lesson`);
        if (m.from === m.to) at(mp, "from and to are the same actor; for work inside one part, send a \"host\" message to the part it affects, or describe it in the step's desc");
        if (!isStr(m.info)) at(mp, "needs a short info line");
        else if (m.info.length > 40) at(mp, `info is ${m.info.length} characters and gets cut off; keep it under 40 and put detail in json or notes`);
        if (m.risk && !(t.risks || {})[m.risk]) at(mp, `risk "${m.risk}" is not in risks`);
        // every message explains itself in the inspector: what it does, then why it is sent
        if (!isStr(m.what)) at(`${mp}.what`, "missing; say what this message does in one plain sentence that starts with a verb (\"Asks the server to…\")");
        else if (isStr(m.info) && m.what.trim().toLowerCase() === m.info.trim().toLowerCase()) at(`${mp}.what`, "repeats info; say what the message does, not its label");
        if (!isStr(m.why)) at(`${mp}.why`, "missing; say why it is sent: the job it does in the flow, or what breaks without it");
        else if (isStr(m.what) && m.why.trim().toLowerCase() === m.what.trim().toLowerCase()) at(`${mp}.why`, "repeats what; give the reason, not the action again");
        prose(`${mp}.what`, m.what, 120);
        prose(`${mp}.why`, m.why, 160);
        (Array.isArray(m.notes) ? m.notes : []).forEach((n, ni) => prose(`${mp}.notes[${ni}]`, n && n[1], 100));
      });
    });
    if (!l.steps.some((s) => (s.msgs || []).length)) at(`${p}.steps`, "no step has any messages");
  };
  for (const l of t.lessons) {
    const p = `lessons.${l.id}`;
    if (!(l.variants || []).length) checkLesson(l, p); // with variants, each variant supplies the steps
    for (const v of l.variants || []) { if (!isStr(v.id)) at(`${p}.variants`, "each variant needs an id"); checkLesson(Object.assign({}, l, v), `${p}.variants.${v.id}`); }
    if (vers && l.since && !vers.includes(l.since)) at(`${p}.since`, `"${l.since}" is not a version`);
    for (const [ver, o] of Object.entries(l.atVersion || {})) { if (vers && !vers.includes(ver)) at(`${p}.atVersion`, `"${ver}" is not a version`); checkLesson(Object.assign({}, l, o), `${p}.atVersion.${ver}`); }
    // spatial stability: an actor shared by a lesson's variants or versions stays put, so switching
    // between them only changes what actually differs
    // (only layouts a reader can see: lesson-level actors are hidden when every variant has its own)
    const shown = (f) => f.actors || l.actors || [];
    const forms = [...((l.variants || []).length ? l.variants.map((v) => [`variants.${v.id}`, shown(v)]) : [["", shown(l)]]),
      ...Object.entries(l.atVersion || {}).map(([k, o]) => [`atVersion.${k}`, shown(o)])];
    const seen = {};
    for (const [where, actors] of forms) for (const a of actors) {
      const s = seen[a.id];
      if (!s) seen[a.id] = { x: a.x, y: a.y, where };
      else if (s.x !== a.x || s.y !== a.y) at(`${p}${where ? "." + where : ""}.actors.${a.id}`, `at ${a.x}, ${a.y} but at ${s.x}, ${s.y} in ${s.where || "the lesson"}; keep shared actors in the same place so switching only changes what differs`);
    }
  }
  for (const [k, r] of Object.entries(t.risks || {})) if (r.lesson && !ids.has(r.lesson)) at(`risks.${k}.lesson`, `no lesson "${r.lesson}"`);
  return errs;
}

let page = null;
export function render(t) {
  if (!page) {
    const font = (f) => readFileSync(join(root, "src", "fonts", f)).toString("base64");
    const css = readFileSync(join(root, "src", "explainer.css"), "utf8").replace(/url\(fonts\/([\w-]+\.woff2)\)/g, (m, f) => `url(data:font/woff2;base64,${font(f)})`);
    page = readFileSync(join(root, "src", "index.html"), "utf8")
      .replace("{{CSS}}", () => css)
      .replace("{{JS}}", () => readFileSync(join(root, "src", "explainer.js"), "utf8").replace(/<\/script/gi, "<\\/script"))
      .replace("{{GENERATOR}}", `explainer-kit ${KIT_VERSION}`);
  }
  t = applyPreset(t);
  const attr = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
  const vals = {
    PAGE_TITLE: attr(t.pageTitle || t.title),
    DESCRIPTION: attr(t.description || ""),
    TOPIC_JSON: JSON.stringify(t).replace(/</g, "\\u003c"), // keeps "</script>" in topic text from closing the tag
  };
  return page.replace(/\{\{(PAGE_TITLE|DESCRIPTION|TOPIC_JSON)\}\}/g, (m, k) => vals[k]); // one pass: inserted text is never rescanned
}

// Lesson and message counts, including messages inside variants.
export const stats = (t) => ({
  lessons: t.lessons.length,
  messages: t.lessons.reduce((n, l) => n + [l, ...(l.variants || [])].reduce((k, v) => k + (v.steps || []).reduce((j, s) => j + (s.msgs || []).length, 0), 0), 0),
});

// Before a built page is replaced, keep the old one (and the topic file beside it, if given) in a
// .history folder next to it. The old page also embeds its own topic. Returns the kept page path.
export function keepPrevious(out, topicPath) {
  const hist = join(dirname(out), ".history"), stamp = new Date().toISOString().replace(/[:.]/g, "-");
  mkdirSync(hist, { recursive: true });
  const prev = join(hist, `${basename(out, ".html")}.${stamp}.html`);
  copyFileSync(out, prev);
  if (topicPath && existsSync(topicPath)) copyFileSync(topicPath, prev.replace(/.html$/, ".json"));
  return prev;
}
