// Shared local viewer for built explainers. One HTTP listener per explainers folder serves every page in it:
//  - starts on demand (when a page is built or opened), on 127.0.0.1 only;
//  - the owner writes a private record (<folder>/.viewer.json, readable only by this user): its port, a signing
//    key that never leaves disk, and a separate link token. Other sessions reuse only that recorded port, and only
//    after the viewer there signs a one-time challenge bound to that port, so a squatter or a relay on another port
//    is never trusted and a leaked link can't forge the proof;
//  - serves pages only to requests carrying the link token (?k=...), so other local users can't read them;
//  - stops after an idle period, and with the process that owns it (the listener never keeps it alive), deleting
//    its record, so every new viewer gets fresh secrets and old links stop working;
//  - serves only .html files inside the folder, never cached.
import http from "node:http";
import { randomBytes, createHmac, timingSafeEqual } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, statSync, readdirSync, mkdirSync, rmSync } from "node:fs";
import { join, resolve, relative, isAbsolute } from "node:path";

const sign = (key, nonce, port) => createHmac("sha256", key).update(`${nonce}:${port}`).digest("hex");
const equal = (a, b) => typeof a === "string" && typeof b === "string" && a.length === b.length && timingSafeEqual(Buffer.from(a), Buffer.from(b));
const hex = () => randomBytes(16).toString("hex");

export function createViewer({ folder, basePort = 4823, tries = 10, idleMs = 30 * 60 * 1000, version = "" }) {
  folder = resolve(folder);
  const recordFile = join(folder, ".viewer.json");
  let srv = null, port = 0, timer = null, token = null, key = null;
  const base = () => `http://127.0.0.1:${port}`;
  const record = () => { try { const r = JSON.parse(readFileSync(recordFile, "utf8")); return Number.isInteger(r.port) && /^[0-9a-f]{32}$/.test(r.key) && /^[0-9a-f]{32}$/.test(r.token) ? r : null; } catch { return null; } };
  const stop = () => {
    if (!srv) return;
    srv.close(); srv.closeAllConnections?.(); srv = null; port = 0;
    if (record()?.token === token) rmSync(recordFile, { force: true }); // only our own record: a newer owner's stays
  };
  const touch = () => { clearTimeout(timer); timer = setTimeout(stop, idleMs); timer.unref(); };
  const inside = (p) => { const r = relative(folder, p); return !!r && !r.startsWith("..") && !isAbsolute(r); };

  function index() {
    const pages = existsSync(folder) ? readdirSync(folder).filter((f) => f.endsWith(".html")).map((f) => {
      const html = readFileSync(join(folder, f), "utf8"), t = (html.match(/<title>([^<]*)<\/title>/) || [])[1] || f;
      return { f, t, m: statSync(join(folder, f)).mtimeMs };
    }).sort((a, b) => b.m - a.m) : [];
    const rows = pages.map((p) => `<li><a href="/${encodeURIComponent(p.f)}?k=${token}">${p.t}</a><span>${new Date(p.m).toISOString().slice(0, 16).replace("T", " ")}</span></li>`).join("");
    return `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Explainers</title>
<style>:root{color-scheme:light dark;--bg:#f5f3ef;--fg:#191615;--mute:#19161599;--line:#19161526}@media(prefers-color-scheme:dark){:root{--bg:#191615;--fg:#f5f3ef;--mute:#f5f3ef99;--line:#f5f3ef26}}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}main{max-width:720px;margin:0 auto;padding:40px 20px}h1{font-weight:400;font-size:28px;margin:0 0 20px}
ul{list-style:none;margin:0;padding:0}li{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-top:1px solid var(--line)}a{color:inherit}span{color:var(--mute);font-size:13px;white-space:nowrap}</style>
<main><h1>Explainers</h1>${rows ? `<ul>${rows}</ul>` : "<p>No explainers yet.</p>"}</main>`;
  }

  function handler(req, res) {
    touch();
    const head = { "cache-control": "no-store", "x-content-type-options": "nosniff", "referrer-policy": "no-referrer" };
    const send = (status, body = "", type = "text/plain; charset=utf-8") => { res.writeHead(status, { ...head, "content-type": type }); res.end(req.method === "HEAD" ? undefined : body); };
    const host = String(req.headers.host || "").toLowerCase();
    if (host !== `127.0.0.1:${port}` && host !== `localhost:${port}`) return send(403, "forbidden"); // blocks DNS rebinding
    if (req.method !== "GET" && req.method !== "HEAD") return send(405, "method not allowed");
    let url, path;
    try { url = new URL(req.url || "/", "http://x"); path = decodeURIComponent((req.url || "/").split("?")[0]); } catch { return send(400, "bad request"); }
    if (path === "/__explainer") { // identity check: sign the caller's one-time challenge, reveal nothing else
      const n = url.searchParams.get("n");
      return send(200, JSON.stringify({ app: "explainer", version, ...(n && /^[0-9a-f]{32}$/.test(n) ? { proof: sign(key, n, port) } : {}) }), "application/json");
    }
    if (!equal(url.searchParams.get("k"), token)) return send(403, "forbidden");
    if (path === "/") return send(200, index(), "text/html; charset=utf-8");
    if (path.includes("..") || path.includes("\\")) return send(404, "not found");
    const file = resolve(folder, "." + path);
    if (!file.toLowerCase().endsWith(".html") || !inside(file) || !existsSync(file) || !statSync(file).isFile()) return send(404, "not found");
    send(200, readFileSync(file), "text/html; charset=utf-8");
  }

  // does the viewer on the recorded port prove it holds the recorded key, for that port?
  const verify = (rec) => new Promise((ok) => {
    const n = hex();
    const req = http.get({ host: "127.0.0.1", port: rec.port, path: `/__explainer?n=${n}`, timeout: 500 }, (res) => {
      let b = ""; res.on("data", (d) => (b += d));
      res.on("end", () => { try { ok(equal(JSON.parse(b).proof, sign(rec.key, n, rec.port))); } catch { ok(false); } });
    });
    req.on("timeout", () => { req.destroy(); ok(false); });
    req.on("error", () => ok(false));
  });
  const listen = (p) => new Promise((ok) => { // fails on any busy port, so squatters are simply skipped
    const s = http.createServer(handler);
    s.once("error", () => ok(false));
    s.listen(p, "127.0.0.1", () => { s.unref(); srv = s; port = s.address().port; ok(true); });
  });
  const own = () => { // this process now owns the folder's viewer: fresh secrets, recorded for other sessions
    key = hex(); token = hex();
    mkdirSync(folder, { recursive: true });
    writeFileSync(recordFile, JSON.stringify({ port, key, token, pid: process.pid }), { mode: 0o600 });
    touch();
    return base();
  };

  // the viewer's base URL, reusing the recorded one or starting our own; null if no port could be used
  async function ensure() {
    if (srv) { touch(); return base(); }
    const rec = record();
    if (rec && (await verify(rec))) { token = rec.token; return `http://127.0.0.1:${rec.port}`; } // another session's viewer
    for (let p = basePort; p < basePort + tries; p++) if (await listen(p)) return own();
    if (await listen(0)) return own(); // every preferred port busy: any free one
    return null;
  }
  // a page's link: base URL, path inside the folder, and the token
  const link = (b, rel) => `${b}/${rel}?k=${token}`;
  return { ensure, stop, link };
}
