import test from "node:test";
import assert from "node:assert/strict";
import { chmodSync, copyFileSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { delimiter, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import {
  buildClaudeArgs,
  findOnPath,
  parseArgs,
  parseAuthStatus,
  truncateContext,
} from "../scripts/claude-code.mjs";

test("parseArgs", () => {
  const got = parseArgs(["review", "--cwd", "/x", "--timeout-ms", "5", "--max-context-chars", "9", "--no-git-context", "--dry-run", "--", "hi"]);
  assert.equal(got.command, "review");
  assert.equal(got.options.cwd, "/x");
  assert.equal(got.options.timeoutMs, 5);
  assert.equal(got.options.maxContextChars, 9);
  assert.equal(got.options.includeGitContext, false);
  assert.equal(got.options.dryRun, true);
  assert.equal(got.options.prompt, "hi");
});

test("buildClaudeArgs safety", () => {
  const args = buildClaudeArgs("check this");
  assert.deepEqual(args.slice(0, 2), ["-p", "check this"]);
  assert(args.includes("--permission-mode"));
  assert(args.includes("plan"));
  assert(args.includes("--tools"));
  assert(args.includes(""));
  assert(args.includes("--disallowedTools"));
  assert(!args.includes("--dangerously-skip-permissions"));
  assert(!args.includes("--allow-dangerously-skip-permissions"));
  assert(!args.includes("bypassPermissions"));
});

test("helpers", () => {
  assert.equal(parseAuthStatus('{"loggedIn":true}').loggedIn, true);
  assert.equal(parseAuthStatus("bad").parseError, true);
  assert.equal(truncateContext("abcdef", 3), "abc\n\n[context truncated at 3 characters]\n");
  const nodePath = findOnPath("node", process.env.PATH);
  assert(nodePath === null || /[\\/]node(?:\.exe)?$/.test(nodePath));
});

function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), "cici launch space "));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  return root;
}

test("Windows npm layout resolves the native executable, skipping shell shims", (t) => {
  const root = fixture(t);
  writeFileSync(join(root, "claude"), "#!/bin/sh\nexit 1\n");
  writeFileSync(join(root, "claude.cmd"), "@echo off\n");
  const native = join(root, "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe");
  mkdirSync(join(native, ".."), { recursive: true });
  writeFileSync(native, "fixture");
  chmodSync(native, 0o755);
  assert.equal(findOnPath("claude", root, "win32"), native);
  const direct = join(root, "claude.exe");
  writeFileSync(direct, "fixture");
  chmodSync(direct, 0o755);
  assert.equal(findOnPath("claude", root, "win32"), direct);
});

test("Windows skips unsupported shims and keeps PATH precedence", (t) => {
  const root = fixture(t);
  writeFileSync(join(root, "claude"), "shell shim");
  writeFileSync(join(root, "claude.cmd"), "batch shim");
  assert.equal(findOnPath("claude", root, "win32"), null);
  const next = join(root, "next");
  mkdirSync(next);
  writeFileSync(join(next, "claude.exe"), "fixture");
  chmodSync(join(next, "claude.exe"), 0o755);
  assert.equal(findOnPath("claude", [root, next].join(delimiter), "win32"), join(next, "claude.exe"));
});

test("Unix retains extensionless executable lookup", (t) => {
  const root = fixture(t);
  const launcher = join(root, "claude");
  writeFileSync(launcher, "#!/bin/sh\nprintf CICI_UNIX_OK\n");
  chmodSync(launcher, 0o755);
  assert.equal(findOnPath("claude", root, "linux"), launcher);
  if (process.platform !== "win32") {
    assert.equal(spawnSync(launcher, [], { encoding: "utf8" }).stdout, "CICI_UNIX_OK");
  }
});

test("native invocation preserves prompt boundaries and every read-only restriction", async (t) => {
  const { run } = await import("../scripts/claude-code.mjs");
  const root = fixture(t);
  const native = join(root, process.platform === "win32" ? "claude.exe" : "claude");
  // Keep Unix Node's shared libraries beside its real executable.
  if (process.platform === "win32") copyFileSync(process.execPath, native);
  else symlinkSync(process.execPath, native);
  const prompt = 'quotes "hello" \'world\'\n& | < > ^ %PATH% !VAR! $(echo unsafe) `echo unsafe`';
  const args = buildClaudeArgs(prompt);
  const result = await run(native, ["-e", "process.stdout.write(JSON.stringify(process.argv.slice(1)))", "--", ...args]);
  assert.equal(result.ok, true, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), ["-p", prompt, "--permission-mode", "plan", "--tools", "", "--disallowedTools", "Edit MultiEdit Write NotebookEdit Bash", "--output-format", "text", "--no-session-persistence"]);
});

test("missing executable and launch errors are separate from authentication", async (t) => {
  const { run } = await import("../scripts/claude-code.mjs");
  const root = fixture(t);
  const result = await run(join(root, "missing.exe"), ["auth", "status"]);
  assert.equal(result.ok, false);
  assert.equal(result.launchError, "ENOENT");
  const helper = new URL("../scripts/claude-code.mjs", import.meta.url);
  const missing = spawnSync(process.execPath, [fileURLToPath(helper), "setup"], {
    encoding: "utf8", env: { ...process.env, PATH: root },
  });
  assert.equal(missing.status, 1, missing.stderr);
  const report = JSON.parse(missing.stdout);
  assert.match(report.problem, /not found on PATH/);
  assert.equal(report.currentProcess.auth, undefined);
});

test("setup reports a discovered executable that cannot launch without claiming logged out", (t) => {
  const root = fixture(t);
  writeFileSync(join(root, process.platform === "win32" ? "claude.exe" : "claude"), "#!/cici-missing-interpreter\n");
  chmodSync(join(root, process.platform === "win32" ? "claude.exe" : "claude"), 0o755);
  const helper = fileURLToPath(new URL("../scripts/claude-code.mjs", import.meta.url));
  for (const args of [["setup"], ["ask", "--", "synthetic prompt"]]) {
    const result = spawnSync(process.execPath, [helper, ...args], {
      encoding: "utf8", env: { ...process.env, PATH: root }, timeout: 10000,
    });
    assert.equal(result.status, 1, result.stderr);
    assert.doesNotMatch(result.stderr, /ERR_INVALID_ARG_TYPE/);
    if (args[0] === "setup") {
      const report = JSON.parse(result.stdout);
      assert.equal(report.ok, false);
      assert.match(report.problem, /could not be launched/);
      assert(report.launchError);
      assert.equal(report.currentProcess.auth, undefined);
    }
  }
});
