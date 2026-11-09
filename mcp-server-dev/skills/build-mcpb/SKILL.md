---
name: build-mcpb
description: Use when a local stdio MCP server must be distributed as a one-click MCP Bundle for desktop hosts. Default new Go servers to self-contained binary bundles, use the current stable MCPB manifest, and keep the ordinary executable usable outside MCPB.
---

# Build an MCP Bundle

MCPB packages a local stdio MCP server with metadata and install-time configuration.

Use it only when the server must run on the user's machine, for example:

- local files
- desktop applications
- localhost services
- hardware or OS APIs
- local command-line tools

For cloud APIs and shared services, use a remote HTTPS MCP server instead.

## Portability model

MCPB is an optional distribution format, not the MCP server architecture.

Build in this order:

1. normal local stdio MCP server
2. standalone executable and documentation
3. MCP protocol validation
4. MCPB package for hosts that support it

Keep the underlying executable independently runnable so users and other clients are not locked to one bundle host.

## Source of truth

Use:

- `https://github.com/modelcontextprotocol/mcpb`
- `https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md`
- `https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md`

Use the stable manifest version stated in `MANIFEST.md`. At the current verified baseline, that is `0.3`.

Do not use draft fields from a later manifest version unless the target host explicitly supports them and the package is labeled accordingly.

## Default language and package shape

For a new local server, prefer a compiled Go binary:

- no Node or Python runtime dependency
- simple stdio process model
- small operational surface
- straightforward platform-specific release artifacts

Preserve an existing healthy Node, Python, or Rust implementation instead of rewriting it solely for packaging.

## Workflow

### 1. Confirm MCPB is necessary

Before packaging, answer:

- what local capability requires local execution
- which desktop hosts are targeted
- which operating systems and CPU architectures are supported
- what user configuration is required
- whether the same executable should also be documented for manual MCP configuration

If the server only calls remote APIs, stop and use remote HTTPS.

### 2. Build a normal stdio server

For Go:

```go
if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
	log.Fatal(err)
}
```

Rules:

- write MCP messages only to stdout
- write diagnostics to stderr
- exit non-zero on startup or fatal runtime failure
- handle cancellation and process shutdown
- keep all paths, process arguments, and environment input untrusted
- avoid relying on the current working directory

### 3. Build per target

Go binaries are platform and architecture specific. Produce one bundle per supported target by default.

Example:

```bash
GOOS=darwin GOARCH=arm64 go build -trimpath -ldflags="-s -w" \
  -o dist/darwin-arm64/server/local-files ./cmd/server

GOOS=windows GOARCH=amd64 go build -trimpath -ldflags="-s -w" \
  -o dist/windows-amd64/server/local-files.exe ./cmd/server

GOOS=linux GOARCH=amd64 go build -trimpath -ldflags="-s -w" \
  -o dist/linux-amd64/server/local-files ./cmd/server
```

Use a macOS universal binary only when the build and signing process explicitly creates and tests one.

### 4. Create the stable manifest

Minimal Go binary example:

```json
{
  "manifest_version": "0.3",
  "name": "local-files",
  "display_name": "Local Files",
  "version": "0.1.0",
  "description": "Read and search files inside a user-configured local directory.",
  "author": {
    "name": "Your Name"
  },
  "server": {
    "type": "binary",
    "entry_point": "server/local-files",
    "mcp_config": {
      "command": "${__dirname}/server/local-files",
      "args": [],
      "env": {}
    }
  },
  "compatibility": {
    "platforms": ["darwin"]
  }
}
```

For Windows, keep the logical entry point without `.exe` when following the official binary convention. The host can append the extension.

Add `user_config` only for real install-time settings. Mark secrets sensitive and deliver them through environment variables when supported by the target host.

Use `references/manifest-schema.md`.

### 5. Enforce local security

MCPB does not make local code safe.

- scope filesystem access to explicit configured roots
- use OS-rooted file APIs where available
- reject path escape and symlink escape
- never build shell commands from user text
- use executable plus argv arrays
- allowlist commands and flags
- cap file sizes, result counts, recursion, and runtime
- split reads from writes
- re-authorize destructive actions
- never log secrets or return them in tool output

Use `references/local-security.md`.

### 6. Validate and pack

Run the verified current CLI package without adding a global dependency:

```bash
npx --yes @anthropic-ai/mcpb@2.1.2 --version
```

Then, for each target staging directory:

```bash
npx --yes @anthropic-ai/mcpb@2.1.2 validate dist/darwin-arm64/manifest.json
npx --yes @anthropic-ai/mcpb@2.1.2 pack dist/darwin-arm64/ releases/local-files-darwin-arm64.mcpb
npx --yes @anthropic-ai/mcpb@2.1.2 info releases/local-files-darwin-arm64.mcpb
```

Signing is optional and host-dependent. When distributing signed bundles,
verify the final artifact with the same pinned runner:

```bash
npx --yes @anthropic-ai/mcpb@2.1.2 verify releases/local-files-darwin-arm64.mcpb
```

Publish certificate or trust details clearly.

### 7. Test on clean machines

For each artifact:

- inspect the archive contents
- verify executable permissions on Unix
- launch the executable as stdio outside MCPB
- run MCP Inspector against the executable
- install it in each target host
- test install-time configuration
- test without a development toolchain
- test restricted and adversarial inputs
- verify uninstall and update behavior

Do not claim cross-platform support from cross-compilation alone.

### 8. Release both paths

Prefer release assets such as:

```text
local-files-darwin-arm64
local-files-windows-amd64.exe
local-files-linux-amd64
local-files-darwin-arm64.mcpb
local-files-windows-amd64.mcpb
local-files-linux-amd64.mcpb
SHA256SUMS
```

Document:

- manual stdio configuration
- MCPB installation for supported hosts
- OS and architecture matrix
- required local permissions
- configuration and secret handling
- checksums and signatures
- known host limitations

## MCP Apps with MCPB

A local server can still serve MCP App resources. The UI contract is unchanged.

Use `build-mcp-app` for the component and keep the package difference limited to local stdio execution and distribution.

## Hard rules

- Do not use MCPB as the default for remote services.
- Do not call MCPB universally supported.
- Do not ship one Go binary as though it works on every OS and architecture.
- Do not use manifest `0.4` fields under a `0.3` declaration.
- Do not assume the bundle creates a sandbox.
- Do not require MCPB to run the underlying executable.
- Do not claim a host is supported until the actual bundle installs and runs there.

## Output order

When implementing or reviewing, report:

1. why local execution is required
2. target hosts, operating systems, and architectures
3. server runtime and stdio validation
4. manifest and package layout
5. security controls
6. build and bundle commands
7. validation performed
8. release artifacts
9. unverified host behavior or platform gaps

## References

- `../../SOURCE-OF-TRUTH.md`
- `references/manifest-schema.md`
- `references/local-security.md`
