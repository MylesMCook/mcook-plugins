import { spawn } from "node:child_process";

const packageName = "chrome-devtools-mcp@1.5.0";
const packageArgs = [packageName, "--no-usage-statistics"];
const isWindows = process.platform === "win32";
const command = isWindows ? process.env.ComSpec || "cmd.exe" : "npx";
const args = isWindows
  ? ["/d", "/s", "/c", `npx -y ${packageArgs.join(" ")}`]
  : ["-y", ...packageArgs];

const child = spawn(command, args, {
  env: process.env,
  stdio: "inherit",
  windowsHide: true,
});

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => {
    if (!child.killed) child.kill(signal);
  });
}

child.on("error", (error) => {
  console.error(`Unable to start ${packageName}: ${error.message}`);
  process.exitCode = 1;
});

child.on("exit", (code, signal) => {
  process.exitCode = code ?? (signal ? 1 : 0);
});
