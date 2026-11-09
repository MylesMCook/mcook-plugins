# Local Firecrawl CLI

Use the CLI only on a machine that can reach the self-hosted API. Check the installed command help;
CLI availability does not prove this self-hosted API implements newer endpoints.

## Verify before changing anything

```bash
command -v firecrawl
firecrawl --version
firecrawl --help
```

If the CLI is missing or an upgrade is needed, ask before installing or updating
the machine-wide package. After approval, follow the host's existing package
management convention and verify the version. Do not perform an incidental npm,
Node, Homebrew, or Firecrawl upgrade.

## Self-hosted configuration

Prefer current-shell configuration:

```bash
export FIRECRAWL_API_URL=http://127.0.0.1:3002
```

Pass `--api-url "$FIRECRAWL_API_URL"` explicitly. Use `FIRECRAWL_API_KEY` only
when the self-hosted API itself requires that key. Do not reuse or forward a
hosted provider key.

Persistent `firecrawl config` changes require a direct request. Changing only
the URL can retain an existing stored key.

## Small verification

When live web access is in scope:

```bash
mkdir -p .firecrawl
firecrawl scrape "https://example.com" \
  --api-url "$FIRECRAWL_API_URL" \
  --only-main-content \
  -o .firecrawl/self-host-check.md
head -20 .firecrawl/self-host-check.md
```

This verifies one CLI path. It does not prove map, crawl, download, screenshots,
AI formats, or the portable MCP connection.
