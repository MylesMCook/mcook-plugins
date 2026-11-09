// Explainer player: renders one topic (the JSON in #topic) as an intro, a lesson list,
// an animated network/sequence diagram, a message log and a message inspector.
// The topic format is documented in TOPIC-GUIDE.md.
(() => {
"use strict";
const T = JSON.parse(document.getElementById("topic").textContent);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
// web links open in a new tab; "#lesson" and relative links (other topics) stay in this one; other schemes are dropped
const safeUrl = (u) => { u = String(u ?? ""); try { return ["http:", "https:", location.protocol].includes(new URL(u, location.href).protocol) ? u : "#"; } catch { return "#"; } };
const external = (u) => /^https?:\/\//i.test(u);
const link = (t, u) => { u = safeUrl(u); return `<a href="${esc(u)}"${external(u) ? ' target="_blank" rel="noopener"' : ""}>${esc(t)}${external(u) ? " ↗" : ""}</a>`; };
const NS = "http://www.w3.org/2000/svg";
const svgEl = (tag, attrs = {}, html) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; };
const narrow = matchMedia("(max-width:640px)");
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

const KIND = Object.assign({ req: "Request", res: "Response", err: "Error", note: "Notice", http: "Network", host: "Internal" }, T.kinds);
const LESSONS = T.lessons;
const INTRO_ID = (T.intro && T.intro.lesson) || LESSONS[0].id;
const VERS = T.versions || null; // { label, current, list: [{ id, short }] }
const vIdx = (v) => (VERS ? VERS.list.findIndex((x) => x.id === v) : 0);

// ── isometric illustrations ────────────────────────────────────────────────
// Each model is drawn around (0,0) on the ground plane and reports its screen bounds.
const COS = Math.cos(Math.PI / 6), SIN = 0.5;
const iso = (x, y, z) => [(x - y) * COS, (x + y) * SIN - z];
const fmt = (p) => p.map((v) => v.toFixed(1)).join(",");
class Model {
  constructor() { this.svg = ""; this.t = 0; this.b = 0; this.w = 0; }
  grow(p) { this.t = Math.min(this.t, p[1]); this.b = Math.max(this.b, p[1]); this.w = Math.max(this.w, Math.abs(p[0])); }
  shadow(r) { this.svg += `<ellipse cx="0" cy="${(r * 0.08).toFixed(1)}" rx="${r}" ry="${(r * 0.56).toFixed(1)}" class="shd"/>`; this.grow([r, r * 0.64]); return this; }
  // a box from (x,y,z) with size w×d×h; faces: left (front-left), right (front-right), top
  box(x, y, z, w, d, h, opt = {}) {
    const top = [iso(x, y, z + h), iso(x + w, y, z + h), iso(x + w, y + d, z + h), iso(x, y + d, z + h)];
    const right = [iso(x + w, y, z), iso(x + w, y + d, z), iso(x + w, y + d, z + h), iso(x + w, y, z + h)];
    const left = [iso(x, y + d, z), iso(x + w, y + d, z), iso(x + w, y + d, z + h), iso(x, y + d, z + h)];
    [...top, ...right, ...left].forEach((p) => this.grow(p));
    const poly = (pts, c) => `<polygon points="${pts.map(fmt).join(" ")}" class="${c}"/>`;
    let s = `<g class="bx ${opt.cls || ""}">${poly(left, "fl")}${poly(right, "fr")}${poly(top, "ft")}</g>`;
    // face decorations use a local 2D frame: u to the right, v downwards from the face's top-left corner
    const frame = (a, b, c, d, o) => `matrix(${a},${b},${c},${d},${o[0].toFixed(1)},${o[1].toFixed(1)})`;
    if (opt.left) s += `<g transform="${frame(COS, SIN, 0, 1, iso(x, y + d, z + h))}">${opt.left}</g>`;
    if (opt.right) s += `<g transform="${frame(COS, -SIN, 0, 1, iso(x + w, y + d, z + h))}">${opt.right}</g>`;
    if (opt.top) s += `<g transform="${frame(COS, SIN, -COS, SIN, iso(x, y, z + h))}">${opt.top}</g>`;
    this.svg += s;
    return this;
  }
  raw(s, t, b, w) { this.svg += s; this.grow([w, t]); this.grow([w, b]); return this; }
}
const MODELS = {
  server() {
    const m = new Model().shadow(46), w = 46, h = 13, gap = 4;
    for (let i = 0; i < 3; i++) m.box(-w / 2, -w / 2, i * (h + gap), w, w, h, {
      left: `<circle cx="6" cy="${h / 2}" r="2" class="led"/><circle cx="12" cy="${h / 2}" r="2" class="led2"/><path d="M19 ${h / 2}h${w - 25}" class="ln"/>`,
      right: `<path d="M6 4.5h${w - 12}M6 8.5h${w - 12}" class="ln"/>` });
    return m;
  },
  tile(a) {
    const m = new Model().shadow(46), w = 48, h = 12, gap = 4;
    for (let i = 0; i < 2; i++) m.box(-w / 2, -w / 2, i * (h + gap), w, w, h, {
      left: `<circle cx="6" cy="${h / 2}" r="2" class="led"/><path d="M13 ${h / 2}h${w - 19}" class="ln"/>`,
      top: i ? `<text x="${w / 2}" y="${w / 2 + 5}" text-anchor="middle" class="mono3">${esc(a.mono || "")}</text>` : "" });
    return m;
  },
  laptop() {
    // base: a key grid near the hinge, a centred trackpad in front
    let keys = "";
    for (let r = 0; r < 3; r++) for (let c = 0; c < 8; c++) keys += `<rect x="${(4 + c * 6.2).toFixed(1)}" y="${6 + r * 5}" width="5" height="3.8" rx=".8" class="kbd"/>`;
    keys += `<rect x="16" y="21" width="24" height="3.8" rx=".8" class="kbd"/><rect x="19" y="29" width="18" height="10" rx="1.5" class="kbd"/>`;
    const m = new Model().shadow(52).box(-28, -22, 0, 56, 44, 5, { top: keys });
    // lid: hinged on the long back edge, tilted back, screen facing the viewer
    const x0 = -28, x1 = 28, z0 = 5, H = 36, tilt = 9, yf = -19, yb = -22;
    const P = { a: iso(x0, yf, z0), b: iso(x1, yf, z0), c: iso(x1, yf - tilt, z0 + H), d: iso(x0, yf - tilt, z0 + H),
      e: iso(x1, yb - tilt, z0 + H), f: iso(x0, yb - tilt, z0 + H), g: iso(x1, yb, z0) };
    Object.values(P).forEach((p) => m.grow(p));
    const poly = (pts, c) => `<polygon points="${pts.map(fmt).join(" ")}" class="${c}"/>`;
    const L = Math.hypot(H, tilt), v = iso(0, tilt, -H).map((n) => n / L); // unit step down the screen face
    m.svg += `<g class="bx">${poly([P.b, P.g, P.e, P.c], "fr")}${poly([P.d, P.c, P.e, P.f], "ft")}${poly([P.a, P.b, P.c, P.d], "fl")}</g>` +
      `<g transform="matrix(${COS},${SIN},${v[0].toFixed(3)},${v[1].toFixed(3)},${P.d[0].toFixed(1)},${P.d[1].toFixed(1)})">` +
      `<rect x="3" y="3" width="50" height="${(L - 7).toFixed(1)}" rx="2" class="scr"/><path d="M9 11h18M9 17h28M9 23h14" class="code"/></g>`;
    return m;
  },
  chip() {
    const m = new Model().shadow(50), back = [], front = [];
    for (let i = -20; i <= 16; i += 9) {
      back.push([-30, i, 4, 4], [i, -30, 4, 4]);
      front.push([i, 26, 4, 6], [26, i, 6, 4]);
    }
    back.forEach(([x, y, w, d]) => m.box(x, y, 1, w, d, 3, { cls: "pin" }));
    m.box(-26, -26, 0, 52, 52, 8);
    front.forEach(([x, y, w, d]) => m.box(x, y, 1, w, d, 3, { cls: "pin" }));
    return m.box(-15, -15, 8, 30, 30, 6, { top: `<path d="M15 4Q16.5 13.5 26 15Q16.5 16.5 15 26Q13.5 16.5 4 15Q13.5 13.5 15 4Z" class="spark"/>` });
  },
  person() {
    const m = new Model().shadow(24);
    return m.raw(`<path d="M-15 0L-13-30A13 7.5 0 0 1 13-30L15 0A15 8.6 0 0 1-15 0Z" class="fr"/>` +
      `<path d="M0 8.6A15 8.6 0 0 1-15 0L-13-30A13 7.5 0 0 0 0-22.5Z" class="fl"/>` +
      `<ellipse cx="0" cy="-30" rx="13" ry="7.5" class="ft"/>` +
      `<circle cx="0" cy="-49" r="11" class="ft" stroke="var(--f55)" stroke-width=".85"/>`, -60, 8.6, 15);
  },
  browser() {
    return new Model().shadow(42).box(-32, -3, 10, 64, 4, 46, {
      left: `<path d="M0 9h64" class="ln"/><circle cx="5" cy="4.5" r="1.6" class="led"/><circle cx="10" cy="4.5" r="1.6" class="led2"/><circle cx="15" cy="4.5" r="1.6" class="led2"/><rect x="18" y="20" width="28" height="7" rx="2" class="ln2"/><rect x="24" y="32" width="16" height="6" rx="3" class="scr"/>` })
      .box(-6, -2, 0, 12, 6, 10);
  },
  vault() {
    return new Model().shadow(42).box(-24, -24, 0, 48, 48, 46, {
      left: `<circle cx="24" cy="18" r="5" class="scr"/><path d="M21.5 21L20 31H28L26.5 21Z" class="scr"/>`,
      right: `<path d="M6 8h36M6 13h36M6 18h24" class="ln"/>` });
  },
  database() {
    const m = new Model().shadow(34);
    let s = "";
    for (let i = 0; i < 3; i++) {
      const y = -i * 17;
      s += `<path d="M-26 ${y}V${y - 13}A26 15 0 0 0 26 ${y - 13}V${y}A26 15 0 0 1-26 ${y}Z" class="fr"/>` +
        `<path d="M-26 ${y - 13}A26 15 0 0 0 0 ${y + 2}V${y + 15}A26 15 0 0 1-26 ${y}Z" class="fl"/>` +
        `<circle cx="-14" cy="${y + 1}" r="2" class="led"/>`;
    }
    s += `<ellipse cx="0" cy="-47" rx="26" ry="15" class="ft"/>`;
    return m.raw(s, -62, 15, 26);
  },
  gateway() {
    const m = new Model().shadow(60), w = 66;
    for (let i = 0; i < 3; i++) {
      if (i) m.box(-w / 2 + 4, -w / 2 + 4, i * 15 - 9, 4, 4, 9, { cls: "pin" }).box(w / 2 - 8, w / 2 - 8, i * 15 - 9, 4, 4, 9, { cls: "pin" });
      m.box(-w / 2, -w / 2, i * 15, w, w, 6, i === 2 ? { cls: "lit", top: `<rect x="17" y="17" width="32" height="32" rx="3" class="core"/><rect x="26" y="26" width="14" height="14" rx="2" class="spark"/>` } : {});
    }
    return m;
  },
  code() {
    return new Model().shadow(52).box(-29, -29, 0, 58, 58, 32, {
      top: `<rect x="5" y="5" width="48" height="48" rx="2" class="pit"/>`,
      left: `<text x="29" y="21" text-anchor="middle" class="mono3">{ }</text>`,
      right: `<path d="M8 10h22M8 16h30M8 22h16" class="code"/>` });
  },
  phone() {
    return new Model().shadow(30).box(-14, -3, 0, 28, 5, 52, {
      left: `<rect x="3" y="5" width="22" height="38" rx="2" class="scr"/><path d="M7 13h12M7 19h14M7 25h8" class="code"/><circle cx="14" cy="47.5" r="1.8" class="led"/>` });
  },
};
const SCALE = 1.4;
const textW = (s, px, mono) => String(s || "").length * px * (mono ? 0.6 : 0.52);
function layoutActor(a) {
  const m = (MODELS[a.icon] || MODELS.server)(a);
  const mh = (m.b - m.t) * SCALE, total = mh + 46;
  const gy = a.y - total / 2 - m.t * SCALE; // where the model's ground plane sits
  const ly = gy + m.b * SCALE + 22, sy = ly + 19;
  const lw = Math.max(m.w * SCALE * 2, textW(a.label, 19), textW(a.sub, 13.5, true));
  return Object.assign(a, { _svg: m.svg, _gy: gy, _ly: ly, _sy: sy, ex: a.x, ey: gy + (m.t + m.b) / 2 * SCALE, hw: m.w * SCALE + 4, hh: mh / 2 + 4,
    bx0: a.x - lw / 2, bx1: a.x + lw / 2, by0: a.y - total / 2, by1: sy + 6 });
}

// ── lessons: versions, variants, phone layout ──────────────────────────────
const st = { version: VERS ? VERS.current : null, lesson: null, idx: -1, sel: null, playing: false, view: "network", timer: 0 };
const variantOf = {};
function atVersion(l, ver = st.version) {
  if (!VERS || ver === VERS.current) return l;
  if (l.since && vIdx(ver) < vIdx(l.since))
    return Object.assign({}, l, { absent: l.since, variants: undefined, steps: [{ title: "Not in this version", desc: `${l.code} arrived in ${l.since}. Move the timeline forward to see it.`, msgs: [] }] });
  const o = (l.atVersion || {})[ver];
  return o ? Object.assign({}, l, o, { id: l.id, verDiff: o.diff }) : Object.assign({}, l, { verSame: true });
}
function resolve(l) {
  l = atVersion(l);
  const vs = l.variants || [], v = vs.find((x) => x.id === variantOf[l.id]) || vs[0];
  return v ? Object.assign({}, l, v, { id: l.id, code: l.code, name: l.name, vid: v.id, variants: vs }) : l;
}
// Every version and variant of a lesson, for sizing things that must not change when switching between them.
function allForms(l) {
  const forms = [];
  for (const ver of VERS ? VERS.list.map((v) => v.id) : [null]) {
    const lv = VERS ? atVersion(l, ver) : l;
    for (const v of lv.variants && lv.variants.length ? lv.variants : [null]) forms.push(v ? Object.assign({}, lv, v) : lv);
  }
  return forms;
}
const maxSteps = (l) => Math.max(...allForms(l).map((f) => (f.steps || []).length));
// On phones the diagram turns 90°: columns of actors become rows, read top to bottom.
function portrait(l) {
  if (!narrow.matches) return l;
  // rows come from the columns used by any variant or version of this lesson, so a shared actor
  // keeps its row when the reader toggles between them
  const base = LESSONS.find((x) => x.id === l.id), xs = (base ? allForms(base) : [l]).flatMap((f) => f.actors || []).map((a) => a.x);
  const cols = [];
  xs.sort((a, b) => a - b).forEach((x) => { if (!cols.some((c) => Math.abs(c - x) < 90)) cols.push(x); });
  const row = (x) => cols.findIndex((c) => Math.abs(c - x) < 90);
  return Object.assign({}, l, { portrait: true, actors: l.actors.map((a) => Object.assign({}, a, { x: 130 + (a.y - 100) * 1.25, y: 140 + row(a.x) * 285 })) });
}
const withActors = (l) => Object.assign({}, l, { actors: l.actors.map((a) => Object.assign({}, T.actors[a.id], a)) });
const flat = (l) => l.steps.flatMap((s, si) => s.msgs.map((m) => Object.assign({ step: si }, m)));
let MSGS = [];
const actor = (id) => st.lesson.actors.find((a) => a.id === id) || { label: id };

function methodOf(m) {
  if (m.method) return m.method;
  const j = m.json && typeof m.json === "object" ? m.json : {};
  if (j.method) return j.method === "tools/call" && j.params && j.params.name ? "tools/call " + j.params.name : j.method;
  if (m.kind === "res") return "result";
  if (m.kind === "err") return j.error && j.error.code != null ? "error " + j.error.code : "error";
  if (m.kind === "http") return String(j.request || j.status || "http").split(" ")[0];
  return j.type || j.host || "message";
}
const size = (m) => { const b = new TextEncoder().encode(JSON.stringify(m.json ?? null)).length; return b > 1024 ? (b / 1024).toFixed(1) + " KB" : b + " B"; };

// ── rendering ──────────────────────────────────────────────────────────────
const RISKS = T.risks || {};
const riskBtn = (k) => RISKS[k] ? `<button type="button" class="risk" data-risk="${esc(k)}" aria-label="${esc(T.riskLabel || "Watch out")}: ${esc(RISKS[k].title)}" aria-haspopup="dialog"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.2 14.3 13.3H1.7z"/><path d="M8 6.6v3.1M8 11.6v.1"/></svg></button>` : "";

function renderList() {
  const cur = MSGS[st.idx];
  let html = "", last;
  for (const l of LESSONS) {
    if (l.id === INTRO_ID) continue;
    if (l.group !== last) { last = l.group; const g = (T.groups || []).find((x) => x.id === l.group) || { title: l.group || "" }; html += `<div class="gh${g.separate ? " sep" : ""}">${esc(g.title)}</div>`; }
    const open = l.id === st.lesson.id, gone = VERS && l.since && vIdx(st.version) < vIdx(l.since);
    // Every lesson always lists its steps, with room for its longest variant or version, so opening a
    // lesson, toggling a variant or moving the timeline never shifts the list (spatial stability).
    const shown = open ? st.lesson.steps : resolve(l).steps, spare = Math.max(0, maxSteps(l) - shown.length);
    const rows = shown.map((s, i) => `<li><button type="button" class="stp ${open && cur && cur.step === i ? "cur" : open && cur && cur.step > i ? "past" : ""}" data-l="${esc(l.id)}" data-step="${i}"><span class="num">${i + 1}</span><span><b>${esc(s.title)}</b></span></button></li>`).join("")
      + `<li class="ph" aria-hidden="true"><span class="stp"><span class="num">0</span><span><b>&nbsp;</b></span></span></li>`.repeat(spare);
    html += `<div class="li${open ? " open" : ""}${gone ? " gone" : ""}"><button type="button" class="lh" data-l="${esc(l.id)}"${open ? ' aria-current="true"' : ""}><span class="lt"><b>${esc(l.code)}</b><em>${esc(l.name)}</em></span></button><ol class="steps">${rows}</ol></div>`;
  }
  if (T.whatsNext && T.whatsNext.length) html += `<div class="gh sep">${esc(T.whatsNextTitle || "What's next")}</div>` + T.whatsNext.map(([t, d, u]) => { u = safeUrl(u); return `<a class="wnl" href="${esc(u)}"${external(u) ? ' target="_blank" rel="noopener"' : ""}><b>${esc(t)}${external(u) ? " ↗" : " →"}</b><em>${esc(d)}</em></a>`; }).join("");
  $("#list").innerHTML = html;
  if (!$("#left").classList.contains("expanded")) $("#bl-name").textContent = st.lesson.code;
  $("#btn-lessons").setAttribute("aria-label", "Lessons. Current: " + st.lesson.code);
}

function renderOverview() {
  const L = st.lesson;
  $("#ov-title").textContent = L.code;
  $("#ov-name").textContent = L.name;
  // a summary is a short sentence or two, or 2 to 4 bullet points
  $("#ov-sum").innerHTML = Array.isArray(L.summary) ? `<ul>${L.summary.map((s) => `<li>${esc(s)}</li>`).join("")}</ul>` : L.summary ? `<p>${esc(L.summary)}</p>` : "";
  $("#ov-facts tbody").innerHTML = (L.facts || []).map(([k, v]) => `<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`).join("");
  $("#ov-ns").hidden = !L.aside;
  if (L.aside) { $("#ov-ns-tag").textContent = L.aside.tag || ""; $("#ov-ns-text").textContent = L.aside.text || ""; }
  let more = "";
  if (L.links && L.links.length) more += `<div class="srcs"><span class="lbl">${esc(L.linksLabel || "Read more")}</span><span class="lnk">${L.links.map(([t, u]) => link(t, u)).join("")}</span></div>`;
  if (VERS && st.version !== VERS.current) {
    const items = L.absent ? [`${L.code} arrived in ${L.absent}.`] : L.verDiff ? L.verDiff : [`No changes worth showing; the flow matches ${VERS.current}.`];
    more += `<div class="nextbox"><span class="nexttag">${L.absent ? "Not in" : "In"} ${esc(st.version)}</span><ul>${items.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
  }
  for (const b of L.boxes || []) more += `<div class="nextbox"><span class="nexttag">${esc(b.title)}</span><ul>${(b.items || []).map((x) => `<li>${esc(x)}</li>`).join("")}</ul>${b.link ? link(b.link[0], b.link[1]) : ""}</div>`;
  $("#ov-more").innerHTML = more;
}

function highlight(json) {
  return esc(JSON.stringify(json, null, 2)).replace(/(&quot;(?:[^&]|&(?!quot;))*?&quot;)(\s*:)?|\b(true|false|null)\b|(-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b)/gi,
    (m, str, colon, lit, num) => str ? (colon ? `<span class="k">${str}</span>${colon}` : `<span class="s">${str}</span>`) : lit ? `<span class="l">${lit}</span>` : `<span class="n">${num}</span>`);
}
function renderInspector() {
  const i = st.sel != null ? st.sel : st.idx, m = MSGS[i], box = $("#insp");
  if (!m) { box.innerHTML = `<p class="empty">Press <b>Play</b> or <b>Step</b> to send the first message.</p>`; return; }
  const r = m.risk && RISKS[m.risk];
  box.innerHTML = `<div class="ih"><span class="dot k-${esc(m.kind)}"></span><span class="im">${esc(methodOf(m))}</span><span class="isz">${size(m)}</span></div>` +
    `<div class="ir">${esc(actor(m.from).label)} → ${esc(actor(m.to).label)} · ${esc(KIND[m.kind] || m.kind)} · #${i + 1}</div>` +
    (m.json !== undefined ? `<pre class="json">${highlight(m.json)}</pre>` : "") +
    (m.notes ? `<dl class="notes">${m.notes.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl>` : "") +
    (r ? `<div class="riskline">${riskBtn(m.risk)}<p><b>${esc(T.riskLabel || "Watch out")}: ${esc(r.title)}.</b> ${esc(r.text)}${r.lesson ? ` <a href="#${esc(r.lesson)}">See it →</a>` : ""}</p></div>` : "");
}

function renderTable() {
  $("#tbody").innerHTML = MSGS.map((m, i) => {
    const cls = [i === st.idx ? "cur" : "", i > st.idx ? "fut" : "", i === st.sel ? "sel" : ""].join(" ").trim();
    return `<tr class="${cls}" data-i="${i}" tabindex="0"><td><span class="dot k-${esc(m.kind)}">${i + 1}</span></td><td>${esc(actor(m.from).label)}</td><td>${esc(actor(m.to).label)}</td><td class="mono">${esc(methodOf(m))}</td><td>${esc(m.info)}${m.risk ? " " + riskBtn(m.risk) : ""}</td></tr>`;
  }).join("");
  const cur = $("#tbody tr.cur"), wrap = $("#tablewrap");
  if (cur && wrap.clientHeight) { const head = wrap.querySelector("thead").offsetHeight; wrap.scrollTo({ top: Math.max(0, cur.offsetTop - head - (wrap.clientHeight - head) / 2 + cur.offsetHeight / 2), behavior: "smooth" }); }
}

// Two lanes per pair so each direction has its own line; ends stop at the node's box.
function edgePts(a, b) {
  const dx = b.ex - a.ex, dy = b.ey - a.ey, len = Math.hypot(dx, dy) || 1, ux = dx / len, uy = dy / len;
  const clip = (n, sx, sy) => { const k = Math.min(n.hw / Math.abs(sx || 1e-6), n.hh / Math.abs(sy || 1e-6)); return [n.ex + sx * k, n.ey + sy * k]; };
  const p1 = clip(a, ux, uy), p2 = clip(b, -ux, -uy), ox = -uy * 5, oy = ux * 5;
  return [p1[0] + ox, p1[1] + oy, p2[0] + ox, p2[1] + oy];
}
const pairKey = (a, b) => [a, b].sort().join("|");
// A zone's box around its laid-out actors (null when none of them is in this lesson).
function zoneRect(z, find) {
  const ms = z.ids.map(find).filter((m) => m && m.bx0 != null);
  if (!ms.length) return null;
  let x0 = Math.min(...ms.map((m) => m.bx0)) - 22, x1 = Math.max(...ms.map((m) => m.bx1)) + 22;
  const need = 48 + z.label.length * 8.9 + (z.sub ? z.sub.length * 7.6 + 10 : 0);
  if (x1 - x0 < need) { const c = (x0 + x1) / 2; x0 = c - need / 2; x1 = c + need / 2; }
  return { x0, x1, y0: Math.min(...ms.map((m) => m.by0)) - 40, y1: Math.max(...ms.map((m) => m.by1)) + 14 };
}
// The phone diagram's frame is computed from layout geometry over every variant and version of the
// lesson, so toggling or stepping never resizes it (measuring the live drawing changed with highlights).
const frames = {};
function portraitFrame(id) {
  if (frames[id]) return frames[id];
  const f = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity }, grow = (r) => { f.x0 = Math.min(f.x0, r.x0); f.y0 = Math.min(f.y0, r.y0); f.x1 = Math.max(f.x1, r.x1); f.y1 = Math.max(f.y1, r.y1); };
  for (const form of allForms(LESSONS.find((l) => l.id === id))) {
    const P = portrait(withActors(form)), by = Object.fromEntries(P.actors.map((a) => [a.id, layoutActor(a)]));
    P.actors.forEach((a) => grow({ x0: a.bx0, y0: a.by0, x1: a.bx1, y1: a.by1 }));
    (P.zones || []).forEach((z) => { const r = zoneRect(z, (k) => by[k]); if (r) grow(r); });
  }
  return (frames[id] = f);
}
function renderNetwork() {
  const svg = $("#net"), L = st.lesson, cur = MSGS[st.idx];
  L.actors.forEach(layoutActor);
  if (L.portrait) L.actors.forEach((a) => Object.assign(a, { ey: (a.by0 + a.by1) / 2, hw: (a.bx1 - a.bx0) / 2 + 8, hh: (a.by1 - a.by0) / 2 + 8 }));
  let h = `<defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" class="gdot"/></pattern><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahp"/></marker></defs><rect x="-400" y="-100" width="1800" height="${L.portrait ? 2400 : 800}" fill="url(#dots)"/>`;
  h += `<g class="zones">`;
  for (const z of L.zones || []) {
    const r = zoneRect(z, actor);
    if (!r) continue;
    const { x0, y0, x1, y1 } = r, style = z.style || "solid";
    h += `<g class="zone ${style === "dashed" ? "dashed" : style === "accent" ? "accent" : ""}"><rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" rx="16" class="zb"/><text x="${x0 + 18}" y="${y0 + 24}" class="zl">${esc(z.label.toUpperCase())}</text>${z.sub ? `<text x="${x0 + 30 + z.label.length * 8.9}" y="${y0 + 24}" class="zsub">${esc(z.sub)}</text>` : ""}</g>`;
  }
  h += `</g><g>`;
  const pairs = new Map();
  MSGS.forEach((m, i) => {
    const k = pairKey(m.from, m.to);
    if (!pairs.has(k)) pairs.set(k, { a: m.from, b: m.to, used: false, host: true });
    const p = pairs.get(k); if (i <= st.idx) p.used = true; if (m.kind !== "host") p.host = false;
  });
  for (const [k, p] of pairs) {
    const a = actor(p.a), b = actor(p.b);
    if (a.ex == null || b.ex == null) continue;
    const on = cur && pairKey(cur.from, cur.to) === k;
    let pts = [a.ex, a.ey, b.ex, b.ey];
    if (L.portrait) { const q = edgePts(a, b), r = edgePts(b, a); pts = [(q[0] + r[2]) / 2, (q[1] + r[3]) / 2, (q[2] + r[0]) / 2, (q[3] + r[1]) / 2]; }
    h += `<line x1="${pts[0]}" y1="${pts[1]}" x2="${pts[2]}" y2="${pts[3]}" class="edge${on ? " on" : p.used ? " used" : ""}${p.host ? " hostedge" : ""}"/>`;
  }
  h += `</g>`;
  for (const k in L.wires || {}) {
    const [i, j] = k.split("|"), a = actor(i), b = actor(j);
    if (a.ex == null || b.ex == null) continue;
    const w = textW(L.wires[k], 13, true) + 18;
    h += `<g class="wire" transform="translate(${(a.ex + b.ex) / 2},${(a.ey + b.ey) / 2})"><rect x="${-w / 2}" y="-12" width="${w}" height="24" rx="12"/><text y="4.5" text-anchor="middle">${esc(L.wires[k])}</text></g>`;
  }
  for (const a of L.actors) {
    const on = cur && (cur.from === a.id || cur.to === a.id);
    h += `<g class="node iso${on ? " on" : ""}"><g class="mdl" transform="translate(${a.x},${a._gy}) scale(${SCALE})">${a._svg}</g><text x="${a.x}" y="${a._ly}" text-anchor="middle" class="nl halo">${esc(a.label)}</text><text x="${a.x}" y="${a._sy}" text-anchor="middle" class="ns halo">${esc(a.sub || "")}</text></g>`;
  }
  svg.innerHTML = h;
  if (L.portrait) {
    let { x0, y0, x1, y1 } = portraitFrame(L.id);
    if (x1 - x0 < 640) { const c = (x0 + x1) / 2; x0 = c - 320; x1 = c + 320; }
    const p = 18, w = x1 - x0 + 2 * p, hh = y1 - y0 + 2 * p;
    svg.setAttribute("viewBox", `${x0 - p} ${y0 - p} ${w} ${hh}`); svg.style.aspectRatio = `${w} / ${hh}`;
  } else { svg.setAttribute("viewBox", "0 0 1000 560"); svg.style.aspectRatio = ""; }
  renderCaption();
}

const capHTML = (L, i) => {
  const s = L.steps[i] || { title: "", desc: "" };
  const rk = (MSGS.find((m) => m.step === i && m.risk) || {}).risk;
  return `<div class="ov">Step ${i + 1} of ${L.steps.length}${rk ? " " + riskBtn(rk) : ""}</div><div class="ct">${esc(s.title)}</div><p>${esc(s.desc)}</p>`;
};
let capKey = "";
// Reserve the tallest caption of the lesson, across all its steps, variants and versions, so the diagram
// and toggles never move while stepping or switching. Measured in fractional pixels, then rounded up.
function fitCaption() {
  const cap = $("#caption"), L = st.lesson, w = cap.clientWidth, key = L.id + ":" + w;
  if (!w || key === capKey) return;
  capKey = key;
  const keep = cap.innerHTML;
  cap.style.minHeight = "0";
  let h = 0;
  for (const f of allForms(LESSONS.find((l) => l.id === L.id) || L)) (f.steps || []).forEach((s, i) => { cap.innerHTML = capHTML(f, i); h = Math.max(h, cap.getBoundingClientRect().height); });
  cap.innerHTML = keep;
  cap.style.minHeight = Math.max(70, Math.ceil(h)) + "px";
}
function renderCaption() { fitCaption(); const cur = MSGS[st.idx]; $("#caption").innerHTML = capHTML(st.lesson, cur ? cur.step : 0); }
const refit = () => { capKey = ""; if (st.lesson) fitCaption(); };
addEventListener("resize", refit);
if (document.fonts) document.fonts.ready.then(refit);

let anim = null;
function animatePacket(m) {
  const svg = $("#net");
  if (anim) { cancelAnimationFrame(anim.raf); anim.g.remove(); anim.trail.remove(); anim = null; }
  const a = actor(m.from), b = actor(m.to);
  if (a.ex == null || b.ex == null) return;
  const [x1, y1, x2, y2] = edgePts(a, b), label = methodOf(m), w = Math.max(60, label.length * 8.1 + 30);
  const trail = svgEl("line", { x1, y1, x2: x1, y2: y1, class: "trail k-" + m.kind, "marker-end": "url(#ah)" });
  const g = svgEl("g", { class: "pkt k-" + m.kind }, `<rect x="${-w / 2}" y="-14" width="${w}" height="28" rx="14" class="pb"/><circle cx="${-w / 2 + 14}" cy="0" r="4.5" class="pd"/><text x="${-w / 2 + 25}" y="4.5" class="pt">${esc(label)}</text>`);
  svg.append(trail, g);
  const t0 = performance.now(), dur = 900, ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  const tick = (now) => {
    const t = reduceMotion.matches ? 1 : Math.min(1, (now - t0) / dur), e = ease(t), x = x1 + (x2 - x1) * e, y = y1 + (y2 - y1) * e;
    g.setAttribute("transform", `translate(${x},${y})`); trail.setAttribute("x2", x); trail.setAttribute("y2", y);
    if (t < 1) anim.raf = requestAnimationFrame(tick); else g.classList.add("arrived");
  };
  anim = { g, trail, raf: requestAnimationFrame(tick) };
}

function renderSequence() {
  const svg = $("#seq"), L = st.lesson, colW = 1000 / L.actors.length, top = 92, rowH = 38;
  const H = Math.max(520, top + MSGS.length * rowH + 30), cx = {};
  let h = `<defs><marker id="sah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahp"/></marker></defs>`;
  L.actors.forEach((a, i) => {
    const x = colW * i + colW / 2, z = (L.zones || []).find((z) => z.ids.includes(a.id));
    cx[a.id] = x;
    h += `<line x1="${x}" y1="${top - 14}" x2="${x}" y2="${H - 10}" class="life"/><g transform="translate(${x - 70},14)"><rect width="140" height="38" rx="6" class="nb"/><text x="70" y="24" text-anchor="middle" class="nl">${esc(a.label)}</text>${z ? `<text x="70" y="54" text-anchor="middle" class="zl">${esc(z.label.toUpperCase())}</text>` : ""}</g>`;
  });
  let last = -1;
  MSGS.forEach((m, i) => {
    const y = top + 14 + i * rowH, x1 = cx[m.from], x2 = cx[m.to], dir = x2 > x1 ? 1 : -1;
    if (x1 == null || x2 == null) return;
    if (m.step !== last) { h += `<text x="8" y="${y + 4}" class="sstep">${m.step + 1}</text>`; last = m.step; }
    const label = m.kind === "req" || m.kind === "note" ? methodOf(m) : m.info;
    h += `<g class="sm k-${esc(m.kind)}${i > st.idx ? " fut" : ""}${i === st.idx ? " cur" : ""}" data-i="${i}"><line x1="${x1 + dir * 4}" y1="${y}" x2="${x2 - dir * 4}" y2="${y}" marker-end="url(#sah)"/><text x="${(x1 + x2) / 2}" y="${y - 7}" text-anchor="middle">${esc(label)}</text></g>`;
  });
  svg.setAttribute("viewBox", `0 0 1000 ${H}`);
  svg.style.height = H + "px";
  svg.innerHTML = h;
  const wrap = $("#seqwrap"), y = top + st.idx * rowH;
  if (st.idx >= 0 && (y > wrap.scrollTop + wrap.clientHeight - 60 || y < wrap.scrollTop)) wrap.scrollTo({ top: y - 120, behavior: "smooth" });
}

function renderTimeline() {
  if (!VERS) return;
  $("#tm").hidden = false; $("#btn-ver").hidden = false;
  $("#tm").setAttribute("aria-label", VERS.label || "Version");
  $("#tm-label").textContent = VERS.label || "Version";
  $("#bv-name").textContent = (VERS.prefix || "") + st.version;
  const cur = VERS.list.find((v) => v.id === st.version) || {};
  $("#tm-cur").textContent = st.version + (st.version === VERS.current ? " · default" : cur.tag ? " · " + cur.tag : "");
  $("#tm-line").innerHTML = VERS.list.map((v) => `<button type="button" data-ver="${esc(v.id)}" aria-pressed="${v.id === st.version}" title="${esc(v.id)}"><i></i><span>${esc(v.short || v.id)}</span></button>`).join("");
}
function renderVariants() {
  const box = $("#variants"), vs = st.lesson.variants || [];
  box.hidden = vs.length < 2;
  box.innerHTML = vs.map((v) => `<button type="button" data-variant="${esc(v.id)}" aria-pressed="${v.id === st.lesson.vid}" title="${esc(v.hint || "")}">${esc(v.label || v.id)}</button>`).join("");
}

const ICON_PLAY = `<svg viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z"/></svg>`, ICON_PAUSE = `<svg viewBox="0 0 24 24"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg>`;
const nextLesson = () => { const list = LESSONS.filter((l) => l.id !== INTRO_ID), i = list.findIndex((l) => l.id === st.lesson.id); return list[(i + 1) % list.length]; };
function renderAll(animate) {
  const atEnd = st.idx >= MSGS.length - 1;
  $(".stage").classList.toggle("absent", !!st.lesson.absent);
  renderTimeline(); renderVariants(); renderList(); renderOverview(); renderInspector(); renderTable();
  $("#viewnet").hidden = st.view !== "network"; $("#seqwrap").hidden = st.view !== "sequence";
  $$("[data-view]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.view === st.view));
  if (st.view === "network") { renderNetwork(); if (animate && MSGS[st.idx]) animatePacket(MSGS[st.idx]); } else { renderSequence(); renderCaption(); }
  $("#btn-step").disabled = atEnd;
  $("#flowcount").textContent = `${MSGS.length} messages · ${st.lesson.steps.length} steps`;
  $("#btn-play").innerHTML = st.playing ? ICON_PAUSE + "Pause" : ICON_PLAY + (atEnd && st.idx >= 0 ? "Replay" : "Play");
  $("#mb-play").innerHTML = st.playing ? ICON_PAUSE : ICON_PLAY;
  $("#mb-play").setAttribute("aria-label", st.playing ? "Pause" : atEnd ? "Replay" : "Play");
  $("#mb-prev").disabled = st.idx <= 0; $("#mb-next").disabled = atEnd;
  $("#mb-count").textContent = `${st.idx + 1}/${MSGS.length}`;
  const nx = nextLesson(); $("#mb-lname").textContent = nx.code; $("#mb-lesson").setAttribute("aria-label", "Next lesson: " + nx.code);
}

// ── playback ───────────────────────────────────────────────────────────────
const inIntro = () => document.body.classList.contains("intro");
function go(i, animate = true) {
  st.idx = Math.max(-1, Math.min(MSGS.length - 1, i));
  st.sel = null;
  renderAll(animate);
}
function stop() { st.playing = false; clearTimeout(st.timer); }
function loop() {
  if (!st.playing) return;
  if (st.idx >= MSGS.length - 1) {
    stop(); renderAll(false);
    // the intro diagram replays on its own
    if (inIntro()) st.timer = setTimeout(() => { if (inIntro()) { st.idx = -1; st.playing = true; loop(); } }, 2600);
    return;
  }
  go(st.idx + 1);
  const m = MSGS[st.idx], nx = MSGS[st.idx + 1];
  st.timer = setTimeout(loop, nx && nx.step !== m.step ? 2200 : 1300);
}
function play() {
  if (st.playing) { stop(); renderAll(false); return; }
  if (st.idx >= MSGS.length - 1) st.idx = -1;
  st.playing = true; loop();
}
function setLesson(id, vid) {
  stop();
  const base = LESSONS.find((l) => l.id === id) || LESSONS[0];
  if (vid) variantOf[base.id] = vid;
  st.lesson = portrait(withActors(resolve(base)));
  MSGS = flat(st.lesson);
  if (anim) { cancelAnimationFrame(anim.raf); anim = null; }
  capKey = "";
  $("#seqwrap").scrollTop = 0;
  go(0, false);
  const open = $(".li.open"), list = $("#list");
  if (open && list.clientHeight) { const t = open.offsetTop - list.offsetTop - 8; if (t < list.scrollTop || t > list.scrollTop + list.clientHeight - 40) list.scrollTo({ top: t, behavior: "smooth" }); } // only when the lesson is out of view, never under the pointer
}
function writeHash() {
  const L = st.lesson, v = L.vid && L.variants && L.vid !== L.variants[0].id ? ":" + L.vid : "", ver = VERS && st.version !== VERS.current ? "@" + st.version : "";
  history.replaceState(null, "", "#" + L.id + v + ver);
}
function readHash() {
  const [a, ver] = decodeURIComponent(location.hash.slice(1)).split("@"), [id, v] = a.split(":");
  return { id, v, ver: VERS && VERS.list.some((x) => x.id === ver) ? ver : VERS ? VERS.current : null };
}
function enterIntro() {
  document.body.classList.add("intro");
  setLesson(INTRO_ID);
  history.replaceState(null, "", location.pathname + location.search);
  // with reduced motion the intro shows the whole loop at once instead of replaying itself
  if (reduceMotion.matches) { go(MSGS.length - 1, false); return; }
  st.idx = -1; st.playing = true; st.timer = setTimeout(loop, 700);
}
function exitIntro(id) { document.body.classList.remove("intro"); setLesson(id); writeHash(); }

// ── risk pop-over ──────────────────────────────────────────────────────────
let pinned = null;
function showRisk(btn, pin) {
  const r = RISKS[btn.dataset.risk], pop = $("#riskpop");
  if (!r) return;
  if (pin && pinned === btn) { hideRisk(); return; }
  pop.innerHTML = `<b>${esc(r.title)}</b><p>${esc(r.text)}</p>${r.lesson ? `<a href="#${esc(r.lesson)}">See it →</a>` : ""}`;
  pop.hidden = false;
  const b = btn.getBoundingClientRect(), w = Math.min(300, innerWidth - 24);
  pop.style.width = w + "px";
  pop.style.left = Math.max(12, Math.min(innerWidth - w - 12, b.left + b.width / 2 - w / 2)) + "px";
  pop.style.top = (b.bottom + 8 + pop.offsetHeight < innerHeight - 80 ? b.bottom + 8 : b.top - pop.offsetHeight - 8) + "px";
  pinned = pin ? btn : null;
  btn.setAttribute("aria-expanded", "true");
}
function hideRisk() { $("#riskpop").hidden = true; $$(".risk[aria-expanded]").forEach((b) => b.removeAttribute("aria-expanded")); pinned = null; }
document.addEventListener("pointerover", (e) => { const b = e.target.closest && e.target.closest(".risk"); if (b && e.pointerType === "mouse" && !pinned) showRisk(b, false); });
document.addEventListener("pointerout", (e) => { const b = e.target.closest && e.target.closest(".risk"); if (b && e.pointerType === "mouse" && !pinned && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest("#riskpop"))) hideRisk(); });
document.addEventListener("pointerdown", (e) => { if (!e.target.closest("#riskpop, .risk")) hideRisk(); });
addEventListener("scroll", () => { if (!$("#riskpop").hidden) hideRisk(); }, true);

// ── events ─────────────────────────────────────────────────────────────────
function toggleMenu(which) {
  const left = $("#left"), lessons = which === "lessons";
  const on = left.classList.toggle(lessons ? "expanded" : "ver-open");
  left.classList.remove(lessons ? "ver-open" : "expanded");
  $("#btn-lessons").setAttribute("aria-expanded", lessons && on);
  $("#btn-ver").setAttribute("aria-expanded", !lessons && on);
  $("#bl-name").textContent = lessons && on ? "All lessons" : st.lesson.code;
}
function closeMenus() { $("#left").classList.remove("expanded", "ver-open"); $("#btn-lessons").setAttribute("aria-expanded", "false"); $("#btn-ver").setAttribute("aria-expanded", "false"); }
document.addEventListener("click", (e) => {
  const t = e.target.closest("button, tr[data-i], .sm");
  if (!t) return;
  const d = t.dataset;
  if (d.risk) { e.stopPropagation(); showRisk(t, true); return; }
  if (d.step != null) { // a step in any lesson: open that lesson at that step
    stop();
    if (d.l && d.l !== st.lesson.id) { closeMenus(); setLesson(d.l); writeHash(); }
    go(MSGS.findIndex((m) => m.step === +d.step)); return;
  }
  if (d.l) { closeMenus(); setLesson(d.l); writeHash(); return; }
  if (d.ver) { closeMenus(); st.version = d.ver; setLesson(st.lesson.id); writeHash(); return; }
  if (d.variant) { setLesson(st.lesson.id, d.variant); writeHash(); return; }
  if (d.view) { st.view = d.view; renderAll(false); return; }
  if (d.i != null) { stop(); const i = +d.i; if (i <= st.idx) { st.sel = i; renderAll(false); } else go(i); return; }
  switch (t.id) {
    case "btn-play": case "mb-play": play(); break;
    case "btn-step": case "mb-next": stop(); go(st.idx + 1); break;
    case "mb-prev": stop(); go(st.idx - 1, false); break;
    case "btn-reset": stop(); go(-1, false); break;
    case "intro-start": exitIntro(T.intro.start); break;
    case "btn-intro": enterIntro(); break;
    case "mb-log": { const on = document.body.classList.toggle("log-open"); t.setAttribute("aria-expanded", on); if (on) renderTable(); break; }
    case "mb-lesson": setLesson(nextLesson().id); writeHash(); scrollTo({ top: $("#center").offsetTop - 64, behavior: "smooth" }); break;
    case "btn-lessons": toggleMenu("lessons"); break;
    case "btn-ver": toggleMenu("ver"); break;
    case "btn-light": case "btn-dark": document.documentElement.dataset.theme = t.id === "btn-dark" ? "dark" : "light"; syncTheme(); break;
  }
});
document.addEventListener("keydown", (e) => {
  if (e.target.closest("input, textarea, select")) return;
  if (e.key === "Escape") { if (!$("#riskpop").hidden) return hideRisk(); if (document.body.classList.contains("log-open")) { document.body.classList.remove("log-open"); $("#mb-log").setAttribute("aria-expanded", "false"); } return; }
  if (e.key === " " && !e.target.closest("button, a")) { e.preventDefault(); play(); }
  else if (e.key === "ArrowRight") { stop(); go(st.idx + 1); }
  else if (e.key === "ArrowLeft") { stop(); go(st.idx - 1, false); }
  else if (e.key === "Enter" && e.target.matches("tr[data-i]")) e.target.click();
});
addEventListener("hashchange", () => {
  const h = readHash();
  if (!LESSONS.some((l) => l.id === h.id)) return;
  document.body.classList.remove("intro");
  if (location.hash.includes("@")) st.version = h.ver;
  setLesson(h.id, h.v); writeHash();
});
narrow.addEventListener("change", () => { const i = st.idx; setLesson(st.lesson.id); if (i >= 0) go(i, false); });
function syncTheme() { const dark = document.documentElement.dataset.theme === "dark"; $("#btn-light").setAttribute("aria-pressed", !dark); $("#btn-dark").setAttribute("aria-pressed", dark); }

// ── boot: static text from the topic ───────────────────────────────────────
const I = T.intro || {};
$("#site-title").textContent = T.title;
$("#btn-intro").textContent = (LESSONS.find((l) => l.id === INTRO_ID) || {}).code || "Intro";
if (T.byline) { $("#byline").hidden = false; $("#byname").textContent = T.byline; }
$("#subject").textContent = T.subject || T.title;
$("#intro").setAttribute("aria-label", I.heading || T.title);
$("#intro-kicker").textContent = I.kicker || "";
$("#intro-h").textContent = I.heading || T.title;
$("#intro-lead").textContent = I.lead || "";
$("#intro-facts").innerHTML = (I.facts || []).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("");
if (I.startLabel) $("#intro-start-label").textContent = I.startLabel;
for (const k of ["flow", "message", "method", "info"]) if (T.labels && T.labels[k]) $("#lbl-" + k).textContent = T.labels[k];
$("#intro-jump").innerHTML = I.jump && I.jump.length ? "or jump to " + I.jump.map(([t, u]) => `<a href="${esc(safeUrl(u))}">${esc(t)}</a>`).join(" · ") : "";
$("#foot").innerHTML = esc(T.footer || "") + (T.footerLinks ? " " + T.footerLinks.map(([t, u]) => link(t, u)).join(" · ") : "");
syncTheme();
const H0 = readHash();
if (VERS) st.version = H0.ver;
if (LESSONS.some((l) => l.id === H0.id) && H0.id !== INTRO_ID) { document.body.classList.remove("intro"); setLesson(H0.id, H0.v); } else enterIntro();
})();
