# MCPB Manifest And Binary Packaging

## Stable baseline

Use the stable manifest version declared by the official MCPB repository.

Verified baseline:

```json
"manifest_version": "0.3"
```

Canonical sources:

- [MCPB overview](https://github.com/modelcontextprotocol/mcpb)
- [Manifest specification](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)
- [CLI reference](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md)

Do not copy schema URLs or version numbers from old Anthropic repository paths when the official repository has moved.

## Required fields

A minimal manifest requires:

- `manifest_version`
- `name`
- `version`
- `description`
- `author.name`
- `server.type`
- `server.entry_point`
- `server.mcp_config.command`

## Go binary example

```json
{
  "manifest_version": "0.3",
  "name": "local-files",
  "display_name": "Local Files",
  "version": "0.1.0",
  "description": "Read and search files inside a configured local directory.",
  "author": {
    "name": "Your Name",
    "url": "https://example.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/example/local-files"
  },
  "license": "Apache-2.0",
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
  },
  "tools_generated": true
}
```

Binary packages do not declare Node or Python runtime requirements.

## Platform values

Use the manifest's platform vocabulary:

- `darwin`
- `win32`
- `linux`

Architecture is not a portable substitute for platform testing. Publish one artifact per OS and architecture unless a tested universal binary is used.

## Windows entry point

For a binary entry point such as:

```json
"entry_point": "server/local-files"
```

the implementing host may append `.exe` on Windows. Follow the current official manifest behavior and test the actual target host.

## User configuration

Use `user_config` for install-time input, not as a general application database.

Example:

```json
{
  "user_config": {
    "root_dir": {
      "type": "directory",
      "title": "Allowed directory",
      "description": "The only directory this server may access.",
      "required": true
    },
    "api_key": {
      "type": "string",
      "title": "API key",
      "sensitive": true,
      "required": false
    }
  },
  "server": {
    "type": "binary",
    "entry_point": "server/local-files",
    "mcp_config": {
      "command": "${__dirname}/server/local-files",
      "args": [],
      "env": {
        "ROOT_DIR": "${user_config.root_dir}",
        "API_KEY": "${user_config.api_key}"
      }
    }
  }
}
```

Recheck the current manifest spec before relying on interpolation, platform overrides, or draft runtime types.

## Package staging layout

```text
dist/darwin-arm64/
|-- manifest.json
|-- server/
|   `-- local-files
|-- icon.png
`-- README.txt
```

The final `.mcpb` is a ZIP-compatible archive produced from the staging directory.

## CLI checks

```bash
npx --yes @anthropic-ai/mcpb@2.1.2 validate dist/darwin-arm64/manifest.json
npx --yes @anthropic-ai/mcpb@2.1.2 pack dist/darwin-arm64/ releases/local-files-darwin-arm64.mcpb
npx --yes @anthropic-ai/mcpb@2.1.2 info releases/local-files-darwin-arm64.mcpb
```

For signed artifacts:

```bash
npx --yes @anthropic-ai/mcpb@2.1.2 sign releases/local-files-darwin-arm64.mcpb --cert cert.pem --key key.pem
npx --yes @anthropic-ai/mcpb@2.1.2 verify releases/local-files-darwin-arm64.mcpb
```

Do not treat a valid manifest as proof that the executable runs, that permissions are safe, or that a client supports the bundle.
