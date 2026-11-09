# Local MCP Security

An MCPB bundle is a package, not a sandbox. The server normally runs with the user's operating-system privileges.

Treat every tool input as untrusted, including input selected by a model after reading external content.

## Filesystem scope

Use an explicit install-time or launch-time root. Do not default to the entire home directory when a narrower directory works.

For Go 1.25, prefer rooted filesystem APIs:

```go
root, err := os.OpenRoot(configuredRoot)
if err != nil {
	return fmt.Errorf("open configured root: %w", err)
}
defer root.Close()

f, err := root.Open(userRelativePath)
if err != nil {
	return fmt.Errorf("open requested file: %w", err)
}
defer f.Close()
```

Keep user paths relative. Reject absolute paths, volume changes, device paths, and escape attempts. Use rooted APIs for writes and deletes too.

The legacy MCP roots feature is deprecated in protocol `2026-07-28`. Do not make `roots/list` the only security boundary. A configured root enforced by the server remains required.

## Process execution

Never concatenate user text into a shell command.

```go
cmd := exec.CommandContext(ctx, "git", "log", "--end-of-options", validatedRevision, "--")
cmd.Dir = allowedRepository
cmd.Env = minimalEnvironment()
```

The final `--` separates revisions from pathspecs. `--end-of-options` prevents a
validated revision beginning with `-` from being parsed as another Git option.

Rules:

- use executable plus argv
- leave shell execution disabled
- allowlist executables and flags
- validate working directories
- set timeouts
- cap output
- remove unnecessary inherited environment variables
- refuse arbitrary command tools unless arbitrary execution is the explicit product

## Read and write separation

Prefer distinct tools:

```text
list_files
read_file
write_file
delete_file
```

Mark read tools read-only. Mark overwrite and delete tools destructive. Re-authorize each consequential action and include the exact target in the user-visible confirmation path.

Consider omitting delete entirely.

## Resource limits

Cap:

- bytes read or written
- directory entries
- recursion depth
- search matches
- subprocess runtime
- subprocess output
- concurrent operations
- archive expansion ratio

Reject oversized work before loading it into memory.

## Secrets

- mark install-time secrets sensitive in the manifest
- receive them through the host-supported environment path
- never print them to stdout or stderr
- never return them in tool results
- redact derived credentials and authorization headers
- avoid writing secrets to the bundle or working directory

Remember that tool results may enter chat history and logs.

## Local network access

A local server can reach localhost and the wider network unless the OS blocks it.

- allowlist outbound destinations when possible
- defend against SSRF
- do not treat `localhost` as trusted input
- validate URL scheme, host, port, redirects, and resolved addresses
- avoid exposing an unauthenticated local HTTP control plane

## Adversarial tests

Test at least:

- `../` and absolute path escapes
- symlink or junction escapes
- Windows device and UNC paths
- shell metacharacters and option injection
- very large files and directories
- hung child processes
- malicious archive contents
- secret-bearing errors
- repeated destructive requests

## Release rule

Test the package on a clean machine using a low-privilege account. A passing developer-machine test is not sufficient evidence for local security or portability.
