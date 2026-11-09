import test from "node:test";
import assert from "node:assert/strict";
import { spawn, execFileSync } from "node:child_process";
import { once } from "node:events";
import { mkdtemp, mkdir, writeFile, access, rm, realpath } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { withNativeFeedback } from "../frontend/feature.mjs";
import { endpointFrom, trustedWindow } from "../frontend/connection.mjs";
import { feedbackEnvironment, frontendCommand, stopOwnedProcess, runFeedback } from "../runtime/run.mjs";
import { quoteWindowsArgument, windowsProcess } from "../runtime/windows-process.mjs";

test("original Vite configuration and plugin ordering survive both toggles", async () => {
  const plugins = [{ name: "stylex" }, { name: "react" }, { name: "existing-dev-workflow" }];
  const config = { plugins, define: { __APP_VERSION__: '"test"' }, server: { port: 1420 }, worker: { format: "es" }, build: { rolldownOptions: { retained: true } } };
  const wrap = withNativeFeedback(async env => { assert.equal(env.mode, "feedback"); return config; });
  const previous = process.env.WAILS_FEEDBACK;
  try {
    process.env.WAILS_FEEDBACK = "1";
    const output = await wrap({ mode: "feedback", command: "serve" });
    assert.deepEqual(output.plugins.slice(0, 3), plugins);
    assert.equal(output.server.port, config.server.port); assert.deepEqual(output.server.hmr, { protocol: "ws", host: "127.0.0.1" }); assert.equal(config.server.hmr, undefined); assert.equal(output.worker, config.worker); assert.equal(output.build, config.build);
    assert.deepEqual(output.define, { __APP_VERSION__: '"test"', __WAILS_FEEDBACK__: "true" });
    assert.equal(config.plugins.length, 3); assert.equal(Object.hasOwn(config.define, "__WAILS_FEEDBACK__"), false);
    assert.equal(output.plugins.at(-1).transformIndexHtml()[0].attrs.name, "wails-native-feedback");
  } finally { if (previous === undefined) delete process.env.WAILS_FEEDBACK; else process.env.WAILS_FEEDBACK = previous; }
});

test("all builds, including feedback mode, are off even with inherited opt-in", async () => {
  const previous = process.env.WAILS_FEEDBACK;
  try {
    process.env.WAILS_FEEDBACK = "1";
    for (const mode of ["production", "demo", "development", "feedback"]) {
      const result = await withNativeFeedback({ plugins: [] })({ mode, command: "build" });
      assert.equal(result.define.__WAILS_FEEDBACK__, "false"); assert.deepEqual(result.plugins, []);
    }
    delete process.env.WAILS_FEEDBACK;
    assert.equal((await withNativeFeedback({})({ mode: "feedback", command: "serve" })).define.__WAILS_FEEDBACK__, "false");
  } finally { if (previous === undefined) delete process.env.WAILS_FEEDBACK; else process.env.WAILS_FEEDBACK = previous; }
});

test("browser, iframe and unmarked Wails window cannot load the feedback gate", () => {
  const scope = { location: { origin: "http://wails.localhost", protocol: "http:", host: "wails.localhost" }, __BURF_WAILS__: true };
  scope.top = scope.self = scope;
  assert.equal(trustedWindow(scope, "__BURF_WAILS__"), true);
  assert.equal(trustedWindow({ ...scope, top: {} }, "__BURF_WAILS__"), false);
  assert.equal(trustedWindow({ ...scope, __BURF_WAILS__: false, _wails: {} }, "__BURF_WAILS__"), false);
  assert.equal(trustedWindow({ ...scope, location: { origin: "http://127.0.0.1:1431", protocol: "http:", host: "127.0.0.1:1431" } }, "__BURF_WAILS__"), false);
  assert.equal(trustedWindow({ ...scope, location: { origin: "null", protocol: "wails:", host: "localhost" } }, "__BURF_WAILS__"), true);
  for (const location of [
    { protocol: "wails:", host: "localhost:1431" },
    { protocol: "http:", host: "wails.localhost:1431" },
  ]) assert.equal(trustedWindow({ ...scope, location }, "__BURF_WAILS__"), true);
  for (const location of [
    { protocol: "https:", host: "wails.localhost:1431" },
    { protocol: "http:", host: "wails.localhost.example:1431" },
    { protocol: "wails:", host: "localhost:80" },
  ]) assert.equal(trustedWindow({ ...scope, location }, "__BURF_WAILS__"), false);
});

test("feedback endpoint requires loopback plus exact capability", () => {
  const capability = "a".repeat(32);
  assert.equal(endpointFrom({ endpoint: `http://127.0.0.1:54321/${capability}` }), `http://127.0.0.1:54321/${capability}`);
  for (const endpoint of [`http://localhost:54321/${capability}`, `https://127.0.0.1:54321/${capability}`, `http://127.0.0.1:80/${capability}`, `http://127.0.0.1:54321/${capability}?x=1`, `http://a@127.0.0.1:54321/${capability}`, "http://127.0.0.1:54321/mcp"]) assert.throws(() => endpointFrom({ endpoint }));
});

test("runner drops inherited remote integrations and build-tag overrides", () => {
  const output = feedbackEnvironment({ PATH: "retained", AGENTATION_API_KEY: "private", AGENTATION_WEBHOOK_URL: "private", WAILS_MCP_TOKEN: "private", WAILS_FEEDBACK: "1", BURF_DEV_HOST: "remote", BERTH_E2E_LIVE: "1" }, { WAILS_FEEDBACK: "1" });
  assert.deepEqual(output, { PATH: "retained", WAILS_FEEDBACK: "1" });
  assert.throws(() => feedbackEnvironment({ GOFLAGS: "-tags=production" }));
  assert.deepEqual(feedbackEnvironment({ GOFLAGS: "-trimpath" }), { GOFLAGS: "-trimpath" });
});

test("runner retains package script and validates its private Vite port", () => {
  assert.deepEqual(frontendCommand("pnpm", "dev", 1431, "darwin"), { command: "pnpm", args: ["run", "dev", "--mode", "feedback", "--host", "127.0.0.1", "--port", "1431", "--strictPort"] });
  assert.equal(frontendCommand("npm", "dev", 1431, "darwin").args[2], "--");
  assert.equal(frontendCommand("pnpm", "dev", 1431, "win32").args[3], "pnpm.cmd run dev --mode feedback --host 127.0.0.1 --port 1431 --strictPort");
  for (const port of [1420, 1377, 1440, NaN]) assert.throws(() => frontendCommand("pnpm", "dev", port));
  assert.throws(() => frontendCommand("pnpm", "dev&evil", 1431));
});

test("Windows process wrapper contains argument boundaries without invoking a shell", () => {
  assert.equal(quoteWindowsArgument('a"b'), '"a\\"b"');
  assert.equal(quoteWindowsArgument('C:\\folder\\'), '"C:\\folder\\\\"');
  assert.throws(() => quoteWindowsArgument("a\nb"));
  const child = windowsProcess("C:\\Program Files\\node.exe", ["file.mjs", "$literal"], "C:\\private", { PATH: "retained", WAILS_FEEDBACK_PARENT_PID: "untrusted" });
  assert.equal(child.command, "powershell.exe");
  assert.equal(child.env.WAILS_FEEDBACK_CHILD_COMMAND, '"C:\\Program Files\\node.exe" "file.mjs" "$literal"');
  assert.equal(child.env.PATH, "retained");
  assert.equal(child.env.WAILS_FEEDBACK_PARENT_PID, String(process.pid));
  const wrapper = Buffer.from(child.args.at(-1), "base64").toString("utf16le");
  assert.ok(wrapper.indexOf("AssignProcessToJobObject(job,process.Process)") < wrapper.indexOf("ResumeThread(process.Thread)"));
  assert.ok(wrapper.indexOf("OpenProcess(") < wrapper.indexOf("if(!CreateProcess("));
  assert.match(wrapper, /WaitForMultipleObjects/);
});

test("Unix cleanup kills a resistant descendant after its leader exits", { skip: process.platform === "win32", timeout: 8000 }, async () => {
  const descendantCode = 'process.on("SIGTERM",()=>{}); console.log(process.pid); setInterval(()=>{},1000)';
  const leaderCode = `const {spawn}=require("node:child_process"); const child=spawn(process.execPath,["-e",${JSON.stringify(descendantCode)}],{stdio:["ignore","pipe","ignore"]}); child.stdout.on("data",data=>process.stdout.write(data)); process.on("SIGTERM",()=>process.exit(0)); setInterval(()=>{},1000);`;
  const leader = spawn(process.execPath, ["-e", leaderCode], { detached: true, stdio: ["ignore", "pipe", "ignore"] });
  leader.feedbackTree = true;
  try {
    const [output] = await once(leader.stdout, "data");
    const descendant = Number(output.toString().trim());
    assert.ok(descendant > 0);
    await stopOwnedProcess(leader);
    const deadline = Date.now() + 2000;
    while (true) {
      try { process.kill(descendant, 0); }
      catch (error) { assert.equal(error.code, "ESRCH"); break; }
      assert.ok(Date.now() < deadline, "owned descendant remained after cleanup");
      await new Promise(yes => setTimeout(yes, 25));
    }
  } finally {
    try { process.kill(-leader.pid, "SIGKILL"); } catch {}
  }
});


test("Windows private state has only owner and SYSTEM access and failed startup releases the lock", { skip: process.platform !== "win32" }, async (t) => {
  // Windows CI can spell TEMP with an 8.3 alias; exercise the canonical app path.
  const directory = await realpath(await mkdtemp(join(tmpdir(), "wails-feedback-acl-")));
  t.after(() => rm(directory, { recursive: true, force: true }));
  await mkdir(join(directory, "frontend")); await mkdir(join(directory, "native"));
  await writeFile(join(directory, "frontend/package.json"), '{"private":true}');
  const plan = join(directory, "plan.json");
  await writeFile(plan, JSON.stringify({ root: ".", frontend: "frontend", native: "native" }));
  await assert.rejects(runFeedback(plan), /Cannot find module 'agentation-mcp'/);
  const state = join(directory, "state");
  await assert.rejects(access(join(state, "run.lock")), { code: "ENOENT" });
  const script = 'Import-Module (Join-Path $PSHOME "Modules/Microsoft.PowerShell.Security/Microsoft.PowerShell.Security.psd1"); $a=Get-Acl -LiteralPath $env:WAILS_FEEDBACK_ACL_TEST; $s=[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value; $ids=@($a.Access | ForEach-Object {$_.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value}); @{protected=$a.AreAccessRulesProtected;owner=$a.GetOwner([System.Security.Principal.SecurityIdentifier]).Value;current=$s;rules=$ids;rights=@($a.Access | ForEach-Object {[string]$_.FileSystemRights});types=@($a.Access | ForEach-Object {[string]$_.AccessControlType})} | ConvertTo-Json';
  const acl = JSON.parse(execFileSync("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", script], { env: { ...process.env, WAILS_FEEDBACK_ACL_TEST: state }, encoding: "utf8", windowsHide: true }));
  assert.equal(acl.protected, true); assert.equal(acl.owner, acl.current);
  assert.deepEqual(acl.rules.sort(), [acl.current, "S-1-5-18"].sort());
  assert.deepEqual(acl.rights, ["FullControl", "FullControl"]);
  assert.deepEqual(acl.types, ["Allow", "Allow"]);
});


test("Windows owner restricts private state without changing ownership or loading caller modules", { skip: process.platform !== "win32" }, async (t) => {
  const directory = await realpath(await mkdtemp(join(tmpdir(), "wails-feedback-owner-")));
  t.after(() => rm(directory, { recursive: true, force: true }));
  await mkdir(join(directory, "frontend")); await mkdir(join(directory, "native"));
  await writeFile(join(directory, "frontend/package.json"), '{"private":true}');
  const state = join(directory, "state");
  await mkdir(state);
  // A normal desktop owner may edit its DACL but cannot rewrite ownership.
  const script = '$p=$env:WAILS_FEEDBACK_ACL_TEST; $s=[System.Security.Principal.WindowsIdentity]::GetCurrent().User; $a=New-Object System.Security.AccessControl.DirectorySecurity; $a.SetOwner($s); $a.SetAccessRuleProtection($true,$false); $a.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule($s,"Modify,ChangePermissions","ContainerInherit,ObjectInherit","None","Allow"))); $a.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(([System.Security.Principal.SecurityIdentifier]"S-1-5-18"),"FullControl","ContainerInherit,ObjectInherit","None","Allow"))); (Get-Item -LiteralPath $p).SetAccessControl($a)';
  execFileSync("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", script], { env: { ...process.env, WAILS_FEEDBACK_ACL_TEST: state }, windowsHide: true });
  const plan = join(directory, "plan.json");
  await writeFile(plan, JSON.stringify({ root: ".", frontend: "frontend", native: "native" }));
  const modules = join(directory, "caller-modules");
  const security = join(modules, "Microsoft.PowerShell.Security");
  await mkdir(security, { recursive: true });
  await writeFile(join(security, "Microsoft.PowerShell.Security.psd1"), "@{RootModule='incompatible.psm1';ModuleVersion='99.0.0';FunctionsToExport=@('Get-Acl')}\n");
  await writeFile(join(security, "incompatible.psm1"), 'throw "Caller security module must not be loaded by the Windows helper"\n');
  const before = process.env.PSModulePath;
  try {
    process.env.PSModulePath = modules;
    await assert.rejects(runFeedback(plan), /Cannot find module 'agentation-mcp'/);
  } finally {
    if (before === undefined) delete process.env.PSModulePath;
    else process.env.PSModulePath = before;
  }
  await assert.rejects(access(join(state, "run.lock")), { code: "ENOENT" });
});

test("Windows job launches the bounded cmd development workflow", { skip: process.platform !== "win32" }, async () => {
  const task = windowsProcess(process.env.ComSpec, ["/d", "/s", "/c", "echo feedback-launch-ok"], process.cwd(), process.env);
  const child = spawn(task.command, task.args, { env: task.env, stdio: ["ignore", "pipe", "pipe"], windowsHide: true });
  let output = ""; child.stdout.on("data", bytes => { output += bytes; });
  const [code] = await once(child, "exit");
  assert.equal(code, 0); assert.equal(output.trim(), "feedback-launch-ok");
  assert.throws(() => windowsProcess(process.env.ComSpec, ["/d", "/s", "/c", "echo ok & echo forbidden"], process.cwd(), process.env));
});


test("feedback keeps explicit HMR configuration and ordinary server settings", async () => {
  const before = process.env.WAILS_FEEDBACK;
  try {
    process.env.WAILS_FEEDBACK = "1";
    for (const hmr of [false, { host: "existing-host", clientPort: 12345 }]) {
      const server = { hmr, strictPort: true, watch: { ignored: ["**/native/**"] } };
      const result = await withNativeFeedback({ server })({ mode: "feedback", command: "serve" });
      assert.equal(result.server, server);
    }
    const server = { port: 1420 };
    const result = await withNativeFeedback({ server })({ mode: "development", command: "serve" });
    assert.equal(result.server, server);
  } finally { if (before === undefined) delete process.env.WAILS_FEEDBACK; else process.env.WAILS_FEEDBACK = before; }
});
