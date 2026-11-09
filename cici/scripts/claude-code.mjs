#!/usr/bin/env node
import { spawn } from "node:child_process";
import { accessSync, constants } from "node:fs";
import { delimiter, join } from "node:path";
import { pathToFileURL } from "node:url";
import process from "node:process";

const DEFAULT_TIMEOUT_MS = 120000;
const MAX_CONTEXT_CHARS = 120000;
const DISALLOWED_TOOLS = "Edit MultiEdit Write NotebookEdit Bash";

function usage() {
  return `Usage:
  claude-code.mjs setup
  claude-code.mjs ask [--cwd <path>] [--dry-run] -- <prompt>
  claude-code.mjs review [--cwd <path>] [--dry-run] [--no-git-context] -- <focus>
  claude-code.mjs rescue [--cwd <path>] [--dry-run] [--no-git-context] -- <problem>
`;
}

export function parseArgs(argv) {
  const options = {
    cwd: process.cwd(),
    timeoutMs: DEFAULT_TIMEOUT_MS,
    maxContextChars: MAX_CONTEXT_CHARS,
    includeGitContext: true,
    dryRun: false,
    prompt: "",
  };
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--") {
      options.prompt = argv.slice(i + 1).join(" ").trim();
      break;
    }
    if (arg === "--cwd") {
      options.cwd = argv[++i];
      continue;
    }
    if (arg === "--timeout-ms") {
      options.timeoutMs = Number(argv[++i]);
      continue;
    }
    if (arg === "--max-context-chars") {
      options.maxContextChars = Number(argv[++i]);
      continue;
    }
    if (arg === "--no-git-context") {
      options.includeGitContext = false;
      continue;
    }
    if (arg === "--dry-run") {
      options.dryRun = true;
      continue;
    }
    positionals.push(arg);
  }

  if (!options.prompt && positionals.length > 1) {
    options.prompt = positionals.slice(1).join(" ").trim();
  }

  return {
    command: positionals[0] || "help",
    options,
  };
}

export function findOnPath(binary, envPath = process.env.PATH || "", platform = process.platform) {
  for (const dir of envPath.split(delimiter)) {
    if (!dir) continue;
    // npm's Windows shell shims cannot be spawned safely without a shell.
    const candidates = [join(dir, platform === "win32" ? `${binary}.exe` : binary)];
    if (platform === "win32" && binary === "claude") {
      candidates.push(join(dir, "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe"));
    }
    for (const candidate of candidates) {
      try {
        accessSync(candidate, constants.X_OK);
        return candidate;
      } catch {
        // Keep looking.
      }
    }
  }
  return null;
}

export function run(command, args, options = {}) {
  return new Promise((resolve) => {
    const stdout = [];
    const stderr = [];
    let settled = false;
    let timer;
    const onError = (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({
        ok: false,
        code: error.code || 1,
        signal: null,
        stdout: "",
        stderr: error.message,
        launchError: error.code || "UNKNOWN",
      });
    };
    let child;
    try {
      child = spawn(command, args, {
        cwd: options.cwd || process.cwd(),
        stdio: ["pipe", "pipe", "pipe"],
      });
    } catch (error) {
      onError(error);
      return;
    }
    timer = setTimeout(() => {
      child.kill("SIGTERM");
    }, options.timeoutMs || DEFAULT_TIMEOUT_MS);

    child.stdin.end();
    child.stdout.on("data", (chunk) => stdout.push(chunk));
    child.stderr.on("data", (chunk) => stderr.push(chunk));
    child.on("error", onError);
    child.on("close", (code, signal) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({
        ok: code === 0,
        code: code ?? 1,
        signal,
        stdout: Buffer.concat(stdout).toString(),
        stderr: Buffer.concat(stderr).toString(),
      });
    });
  });
}

export function parseAuthStatus(output) {
  try {
    return JSON.parse(output);
  } catch {
    return {
      loggedIn: false,
      parseError: true,
      raw: output.trim(),
    };
  }
}

export function buildClaudeArgs(prompt) {
  return [
    "-p", prompt,
    "--permission-mode", "plan",
    "--tools", "",
    "--disallowedTools", DISALLOWED_TOOLS,
    "--output-format", "text",
    "--no-session-persistence",
  ];
}

export function truncateContext(text, maxChars = MAX_CONTEXT_CHARS) {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars)}\n\n[context truncated at ${maxChars} characters]\n`;
}

async function gitContext(cwd, timeoutMs, maxContextChars) {
  const commands = [
    ["status", "--short", "--branch"],
    ["diff", "--no-ext-diff", "--stat"],
    ["diff", "--no-ext-diff", "--cached", "--stat"],
    ["diff", "--no-ext-diff"],
    ["diff", "--no-ext-diff", "--cached"],
  ];
  const sections = [];

  for (const args of commands) {
    const result = await run("git", args, { cwd, timeoutMs });
    const title = `$ git ${args.join(" ")}`;
    const body = (result.stdout || result.stderr || "").trim();
    sections.push(`## ${title}\n${body || "[no output]"}`);
  }

  return truncateContext(sections.join("\n\n"), maxContextChars);
}

async function setup(options) {
  const claudePath = findOnPath("claude");
  const report = {
    claudePath,
    currentProcess: {
      note: "Auth visible from this shell context.",
    },
    sandboxNote: "Only investigate OAuth/keychain access after Claude starts and reports logged out.",
  };

  if (!claudePath) {
    report.ok = false;
    report.problem = "A supported Claude executable was not found on PATH";
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = 1;
    return;
  }

  const version = await run(claudePath, ["--version"], options);
  if (version.launchError) {
    report.ok = false;
    report.problem = "Claude could not be launched";
    report.launchError = version.launchError;
    report.version = version.stderr.trim();
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = 1;
    return;
  }
  const auth = await run(claudePath, ["auth", "status"], options);

  report.ok = version.ok && auth.ok;
  report.version = (version.stdout || version.stderr).trim();
  if (auth.launchError) {
    report.problem = "Claude authentication command could not be launched";
    report.launchError = auth.launchError;
    report.currentProcess.auth = null;
  } else {
    report.currentProcess.auth = parseAuthStatus(auth.stdout || auth.stderr);
  }
  report.currentProcess.authCommandExitCode = auth.code;

  console.log(JSON.stringify(report, null, 2));
  if (!report.ok) process.exitCode = 1;
}

async function callClaude(kind, options) {
  if (!options.prompt) {
    throw new Error(`Missing prompt.\n${usage()}`);
  }

  let prompt = options.prompt;
  if (kind === "review") {
    const context = options.includeGitContext
      ? await gitContext(options.cwd, options.timeoutMs, options.maxContextChars)
      : "[git context disabled by --no-git-context]";
    prompt = `You are Claude Code giving a read-only second-pass code review.
Prioritize correctness, security, regressions, and missing tests. Do not emit patches.

Review focus:
${options.prompt}

Local git context:
${context}`;
  }

  if (kind === "rescue") {
    const context = options.includeGitContext
      ? await gitContext(options.cwd, options.timeoutMs, options.maxContextChars)
      : "[git context disabled by --no-git-context]";
    prompt = `You are Claude Code helping Codex investigate a stuck task.
Do not edit files. Propose the smallest safe fix plan and checks.

Problem:
${options.prompt}

Local git context:
${context}`;
  }

  if (options.dryRun) {
    process.stdout.write(prompt);
    process.stdout.write("\n");
    return;
  }

  const claudePath = findOnPath("claude");
  if (!claudePath) {
    throw new Error("A supported Claude executable was not found on PATH");
  }

  const result = await run(claudePath, buildClaudeArgs(prompt), options);
  process.stdout.write(result.stdout);
  process.stderr.write(result.stderr);
  if (!result.ok) process.exitCode = Number.isInteger(result.code) && result.code !== 0 ? result.code : 1;
}

async function main(argv) {
  const { command, options } = parseArgs(argv);
  if (!Number.isFinite(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive number");
  }
  if (!Number.isFinite(options.maxContextChars) || options.maxContextChars <= 0) {
    throw new Error("--max-context-chars must be a positive number");
  }

  if (command === "setup") return setup(options);
  if (command === "ask") return callClaude("ask", options);
  if (command === "review") return callClaude("review", options);
  if (command === "rescue") return callClaude("rescue", options);
  console.log(usage());
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
