#!/usr/bin/env node
// Explainer MCP server (stdio, no dependencies). Lets any MCP-capable agent turn a topic into an interactive explainer page.
// Run: node mcp.mjs. Speaks both MCP eras: the 2026-07-28 stateless protocol (server/discover, per-request _meta)
// and the older initialize handshake (2024-11-05 … 2025-11-25).
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync, realpathSync } from "node:fs";
import { join, dirname, resolve, relative, isAbsolute, sep } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createInterface } from "node:readline";
import { validate, render, stats, keepPrevious, KIT_VERSION } from "./kit.mjs";
import { createViewer } from "./viewer.mjs";

const root = dirname(fileURLToPath(import.meta.url));
const MODERN = ["2026-07-28"];
const LEGACY = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"];
const SERVER_INFO = { name: "explainer", version: KIT_VERSION };
const OUT_DIR = process.env.EXPLAINER_OUT || join(homedir(), "Explainers");
const IDLE_MIN = Number(process.env.EXPLAINER_IDLE_MINUTES) || 30;
// one shared local viewer per explainers folder; it stops after IDLE_MIN idle minutes or with this process
const viewer = createViewer({ folder: OUT_DIR, basePort: Number(process.env.EXPLAINER_PORT) || 4823, idleMs: IDLE_MIN * 60000, version: KIT_VERSION });
const viewUrlOf = async (page) => {
  const base = await viewer.ensure();
  return base ? viewer.link(base, relative(OUT_DIR, page).split(sep).map(encodeURIComponent).join("/")) : null;
};
const VIEW_NOTE = `Open it for the user now (in Claude Code desktop: the browser pane). The shared viewer is already running, so don't start a server. It stops by itself after ${IDLE_MIN} idle minutes or when this session ends; explainer_open starts it again.`;
const INSTRUCTIONS = "Turns 'how does X work?' into an interactive, step-by-step explainer page. New explainer: call explainer_guide once, gather the facts first (the user's files, sessions, docs or code), write the topic, do an editing pass (direct text, short sentences, bullet summaries; use the writer skill if available), call explainer_check until it reports ok, then explainer_build. Changing an existing one: explainer_list, then explainer_get, edit, check, build. Showing one: explainer_open. Build and open return viewUrl: open it for the user right away. The shared viewer manages itself, so never start a server for explainers. Never invent specifics: mark guesses as guesses and say when example values are illustrative.";

// Results carry a short model-readable text plus structuredContent matching each tool's outputSchema.
const done = (s, data) => ({ content: [{ type: "text", text: s }], structuredContent: data, isError: false });
const fail = (s) => ({ content: [{ type: "text", text: s }], isError: true });
const inOut = (p) => { const r = relative(resolve(OUT_DIR), p); return r && !r.startsWith("..") && !isAbsolute(r); };
const EXAMPLES = ["dns", "incident", "mcp"];

const TOPIC_INPUT = {
  topic: { type: "object", description: "The whole topic as a JSON object, in the format explainer_guide describes. Give this or topicPath." },
  topicPath: { type: "string", pattern: "\\.json$", description: "A topic file in the explainers folder instead of topic, relative to that folder (for example \"oauth.json\", as explainer_list names it). Cheaper than resending a large topic when revising." },
};
// Exactly one of topic / topicPath; returns { t, src } or { error }.
function loadTopic({ topic, topicPath }) {
  if ((topic === undefined) === (topicPath === undefined)) return { error: "Give exactly one of topic (the JSON object) or topicPath (a .json file)." };
  if (topic !== undefined) {
    if (typeof topic === "string") try { topic = JSON.parse(topic); } catch (e) { return { error: `topic is not valid JSON (${e.message}). Pass it as a JSON object.` }; }
    if (!topic || typeof topic !== "object" || Array.isArray(topic)) return { error: "topic must be a JSON object." };
    return { t: topic, src: null };
  }
  // only topics inside the explainers folder, so this tool can't be used to read other files
  const src = resolve(OUT_DIR, String(topicPath));
  if (!src.toLowerCase().endsWith(".json")) return { error: "topicPath must be a .json file." };
  if (!inOut(src)) return { error: "topicPath must be a file inside the explainers folder, for example \"oauth.json\"." };
  if (!existsSync(src)) return { error: `No topic file named ${relative(OUT_DIR, src)}. Use explainer_list to see saved explainers.` };
  const real = relative(realpathSync(OUT_DIR), realpathSync(src)); // a symlink must not lead out of the folder
  if (!real || real.startsWith("..") || isAbsolute(real)) return { error: "topicPath must not link outside the explainers folder." };
  try { return { t: JSON.parse(readFileSync(src, "utf8")), src }; } catch (e) { return { error: `${src} is not valid JSON (${e.message}).` }; }
}
const problemsText = (errs) => `${errs.length} problem(s):\n- ` + errs.join("\n- ");
// Saved explainers: every <name>.json in the folder that has a built <name>.html beside it.
function saved() {
  if (!existsSync(OUT_DIR)) return [];
  return readdirSync(OUT_DIR).filter((f) => f.endsWith(".json") && existsSync(join(OUT_DIR, f.replace(/\.json$/, ".html")))).map((f) => {
    const topicPath = join(OUT_DIR, f), page = topicPath.replace(/\.json$/, ".html");
    let t = {}; try { t = JSON.parse(readFileSync(topicPath, "utf8")); } catch {}
    return { name: f.replace(/\.json$/, ""), id: t.id || null, title: t.title || null, updated: statSync(page).mtime.toISOString(), page, topicPath };
  }).sort((a, b) => b.updated.localeCompare(a.updated));
}

const TOOLS = [
  {
    name: "explainer_guide",
    title: "How to write an explainer topic",
    description: "Use this before writing a new explainer topic. Returns the topic format, the writing, accuracy and template rules, the presets, and one complete example to copy. Read-only. Next: write the topic, then explainer_check.",
    inputSchema: { type: "object", additionalProperties: false, properties: { example: { enum: EXAMPLES, default: "dns", description: "Example to include: dns (a system or protocol, small), incident (something that broke and was fixed, incident preset), mcp (large, with versions)." } } },
    annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
    run: ({ example = "dns" }) => {
      if (!EXAMPLES.includes(example)) return fail(`example must be one of ${EXAMPLES.join(", ")}.`);
      return { content: [{ type: "text", text: readFileSync(join(root, "TOPIC-GUIDE.md"), "utf8") + `\n\n## Complete example (topics/${example}.json)\n\n\`\`\`json\n` + readFileSync(join(root, "topics", `${example}.json`), "utf8") + "\n```" }], isError: false };
    },
  },
  {
    name: "explainer_list",
    title: "List saved explainers",
    description: "Use this when the user mentions an explainer they already have (\"update my OAuth explainer\") and you need its name. Lists explainers in the explainers folder, newest first. Read-only. Next: explainer_get.",
    inputSchema: { type: "object", additionalProperties: false, properties: {} },
    outputSchema: { type: "object", required: ["folder", "explainers"], properties: { folder: { type: "string" }, explainers: { type: "array", items: { type: "object", properties: { name: { type: "string" }, id: { type: ["string", "null"] }, title: { type: ["string", "null"] }, updated: { type: "string" }, page: { type: "string" }, topicPath: { type: "string" } } } } } },
    annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
    run: () => {
      const list = saved().slice(0, 50);
      const lines = list.map((e) => `- ${e.name}: ${e.title || "(no title)"} · updated ${e.updated.slice(0, 10)}`);
      return done(list.length ? `${list.length} explainer(s) in ${OUT_DIR}:\n${lines.join("\n")}` : `No explainers yet in ${OUT_DIR}.`, { folder: OUT_DIR, explainers: list });
    },
  },
  {
    name: "explainer_get",
    title: "Get a saved explainer's topic",
    description: "Use this to revise an existing explainer: returns its saved topic JSON and file paths. Edit the topic, then explainer_check and explainer_build (with topicPath if you edited the file on disk). Read-only.",
    inputSchema: { type: "object", additionalProperties: false, required: ["name"], properties: { name: { type: "string", pattern: "^[A-Za-z0-9._-]+$", description: "The explainer's name from explainer_list (its file name without .json)." } } },
    outputSchema: { type: "object", required: ["name", "page", "topicPath", "topic"], properties: { name: { type: "string" }, page: { type: "string" }, topicPath: { type: "string" }, topic: { type: "object" } } },
    annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
    run: ({ name }) => {
      if (typeof name !== "string" || !/^[A-Za-z0-9._-]+$/.test(name)) return fail("name must be a file name from explainer_list, without a folder or .json.");
      const e = saved().find((x) => x.name === name);
      if (!e) return fail(`No saved explainer named "${name}". Use explainer_list to see the names.`);
      const topic = JSON.parse(readFileSync(e.topicPath, "utf8"));
      return done(`Topic file: ${e.topicPath}\nPage: ${e.page}\n\n${JSON.stringify(topic, null, 2)}`, { name, page: e.page, topicPath: e.topicPath, topic });
    },
  },
  {
    name: "explainer_check",
    title: "Check an explainer topic",
    description: "Use this after writing or editing a topic, before building. Lists every problem with its exact location (fields, references, lengths, spacing, wording). Fix them and check again until it reports ok. Read-only; writes nothing.",
    inputSchema: { type: "object", additionalProperties: false, properties: TOPIC_INPUT },
    outputSchema: { type: "object", required: ["ok", "problems"], properties: { ok: { type: "boolean" }, problems: { type: "array", items: { type: "string" } }, lessons: { type: "integer" }, messages: { type: "integer" } } },
    annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
    run: (args) => {
      const { t, error } = loadTopic(args);
      if (error) return fail(error);
      const errs = validate(t, "topic");
      if (errs.length) return { ...fail(problemsText(errs)), structuredContent: { ok: false, problems: errs } };
      const s = stats(t);
      return done(`ok: ${s.lessons} lessons, ${s.messages} messages. Next: explainer_build.`, { ok: true, problems: [], ...s });
    },
  },
  {
    name: "explainer_build",
    title: "Build an explainer page",
    description: "Use this once explainer_check reports ok. Writes one self-contained HTML page (opens from disk, no server) to the explainers folder as <id>.html, with the topic saved beside it as <id>.json for later revision. Rebuilding replaces the page, and the previous page and topic are kept in a .history folder first. Returns viewUrl, a local link that works right away. Next: open viewUrl for the user.",
    inputSchema: { type: "object", additionalProperties: false, properties: { ...TOPIC_INPUT, path: { type: "string", pattern: "\\.html$", description: "Optional file name (or sub-path) inside the explainers folder, ending in .html. Defaults to <id>.html." } } },
    outputSchema: { type: "object", required: ["page", "url", "topicPath"], properties: { page: { type: "string" }, url: { type: "string", description: "file:// address of the page" }, viewUrl: { type: ["string", "null"], description: "Local viewer link to open; null if no viewer could start" }, topicPath: { type: "string" }, previous: { type: ["string", "null"], description: "Where the replaced page was kept, if any." }, unchanged: { type: "boolean" }, lessons: { type: "integer" }, messages: { type: "integer" }, kitVersion: { type: "string" } } },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    run: async (args) => {
      const { path, ...topicArgs } = args;
      const { t, src, error } = loadTopic(topicArgs);
      if (error) return fail(error);
      const errs = validate(t, "topic");
      if (errs.length) return fail("Not built. " + problemsText(errs));
      const out = resolve(OUT_DIR, path || `${t.id}.html`);
      if (!inOut(out)) return fail(`path must stay inside the explainers folder (${OUT_DIR}).`);
      if (!out.toLowerCase().endsWith(".html")) return fail("path must end in .html.");
      const topicPath = out.replace(/\.html$/i, ".json"), html = render(t), json = JSON.stringify(t, null, 2);
      const unchanged = existsSync(out) && readFileSync(out, "utf8") === html;
      const previous = existsSync(out) && !unchanged ? keepPrevious(out, topicPath) : null; // keep what is about to be replaced
      mkdirSync(dirname(out), { recursive: true });
      if (!unchanged) writeFileSync(out, html);
      if (!src || resolve(src) !== resolve(topicPath)) writeFileSync(topicPath, json); // a topic edited in place is already saved
      const s = stats(t), url = pathToFileURL(out).href, viewUrl = await viewUrlOf(out);
      return done(
        `${unchanged ? "Unchanged" : "Built"} ${out}\n${viewUrl ? `View: ${viewUrl}\n${VIEW_NOTE}` : `Open: ${url} (no local viewer could start; open the file directly)`}\nTopic: ${topicPath}${previous ? `\nPrevious version kept: ${previous}` : ""}`,
        { page: out, url, viewUrl, topicPath, previous, unchanged, ...s, kitVersion: KIT_VERSION },
      );
    },
  },
  {
    name: "explainer_open",
    title: "Open a saved explainer",
    description: "Use this when the user wants to see an explainer that is already built (\"show me the OAuth explainer\"). Returns viewUrl, a local link that works right away, starting the shared viewer if needed. Get the name from explainer_list. Next: open viewUrl for the user.",
    inputSchema: { type: "object", additionalProperties: false, required: ["name"], properties: { name: { type: "string", pattern: "^[A-Za-z0-9._-]+$", description: "The explainer's name from explainer_list." } } },
    outputSchema: { type: "object", required: ["name", "viewUrl", "page"], properties: { name: { type: "string" }, viewUrl: { type: ["string", "null"] }, page: { type: "string" } } },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    run: async ({ name }) => {
      const e = saved().find((x) => x.name === name);
      if (!e) return fail(`No saved explainer named "${name}". Use explainer_list to see the names.`);
      const viewUrl = await viewUrlOf(e.page);
      return done(viewUrl ? `View: ${viewUrl}\n${VIEW_NOTE}` : `No local viewer could start. Open the file directly: ${pathToFileURL(e.page).href}`, { name, viewUrl, page: e.page });
    },
  },
];

const cacheable = { resultType: "complete", ttlMs: 3600000, cacheScope: "public" };
async function handle(msg) {
  const { method, params = {} } = msg;
  const asked = params._meta && params._meta["io.modelcontextprotocol/protocolVersion"];
  if (asked && method !== "initialize" && ![...MODERN, ...LEGACY].includes(asked))
    throw Object.assign(new Error("Unsupported protocol version"), { code: -32022, data: { supported: [...MODERN, ...LEGACY], requested: asked } });
  switch (method) {
    case "initialize": {
      const v = params.protocolVersion;
      return { protocolVersion: LEGACY.includes(v) ? v : LEGACY[0], capabilities: { tools: {} }, serverInfo: SERVER_INFO, instructions: INSTRUCTIONS };
    }
    case "server/discover":
      return { ...cacheable, supportedVersions: [...MODERN, ...LEGACY], capabilities: { tools: {} }, instructions: INSTRUCTIONS };
    case "ping":
      return { resultType: "complete" };
    case "tools/list":
      return { ...cacheable, tools: TOOLS.map(({ run, ...t }) => t) };
    case "tools/call": {
      const tool = TOOLS.find((t) => t.name === params.name);
      if (!tool) throw Object.assign(new Error(`Unknown tool: ${params.name}`), { code: -32602 });
      const args = params.arguments || {}, allowed = Object.keys(tool.inputSchema.properties);
      const extra = Object.keys(args).filter((k) => !allowed.includes(k));
      if (extra.length) return { resultType: "complete", ...fail(`Unknown argument(s): ${extra.join(", ")}. ${tool.name} takes: ${allowed.join(", ") || "nothing"}.`) };
      try { return { resultType: "complete", ...(await tool.run(args)) }; } catch (e) { return { resultType: "complete", ...fail(`Failed: ${e.message}`) }; }
    }
    default:
      throw Object.assign(new Error(`Method not found: ${method}`), { code: -32601 });
  }
}

const send = (o) => process.stdout.write(JSON.stringify(o) + "\n");
// when the client closes our stdin the session is over: exit, taking the viewer with us
createInterface({ input: process.stdin }).on("close", () => { viewer.stop(); process.exit(0); }).on("line", async (line) => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }); }
  if (msg.id === undefined) return; // notifications need no reply
  try {
    const result = await handle(msg);
    result._meta = { ...result._meta, "io.modelcontextprotocol/serverInfo": SERVER_INFO };
    send({ jsonrpc: "2.0", id: msg.id, result });
  } catch (e) {
    send({ jsonrpc: "2.0", id: msg.id, error: { code: e.code || -32603, message: e.message, ...(e.data ? { data: e.data } : {}) } });
  }
});
