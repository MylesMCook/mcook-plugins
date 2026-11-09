# Go Remote MCP Server Scaffold

Use this as the default greenfield baseline for an ordinary remote integration server.

## Requirements

- Go `1.25` or newer
- official Go MCP SDK pinned to `v1.7.0`

This scaffold was last compiled and vetted with Go `1.27.0`.

```bash
go mod init example.com/acme-catalog-mcp
go get github.com/modelcontextprotocol/go-sdk@v1.7.0
```

Pin the SDK version in `go.mod` and commit `go.sum`.

## Minimal complete server

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sort"
	"strings"
	"syscall"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type Item struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Notes string `json:"notes"`
}

type SearchInput struct {
	Query string `json:"query"`
	Limit int    `json:"limit"`
}

type SearchOutput struct {
	Items []Item `json:"items"`
}

var catalog = []Item{
	{ID: "itm_001", Name: "Alpha", Notes: "First catalog item"},
	{ID: "itm_002", Name: "Bravo", Notes: "Second catalog item"},
	{ID: "itm_003", Name: "Charlie", Notes: "Third catalog item"},
}

func searchItems(
	_ context.Context,
	_ *mcp.CallToolRequest,
	input SearchInput,
) (*mcp.CallToolResult, SearchOutput, error) {
	query := strings.TrimSpace(input.Query)
	if query == "" {
		return nil, SearchOutput{}, errors.New("query must not be blank")
	}

	limit := input.Limit
	if limit == 0 {
		limit = 10
	}

	query = strings.ToLower(query)
	items := make([]Item, 0, limit)
	for _, item := range catalog {
		haystack := strings.ToLower(item.Name + " " + item.Notes)
		if strings.Contains(haystack, query) {
			items = append(items, item)
		}
	}
	sort.Slice(items, func(i, j int) bool {
		return items[i].ID < items[j].ID
	})
	if len(items) > limit {
		items = items[:limit]
	}

	output := SearchOutput{Items: items}
	result := &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{
				Text: fmt.Sprintf("Found %d catalog items matching %q.", len(items), input.Query),
			},
		},
	}
	return result, output, nil
}

func newMCPServer() *mcp.Server {
	server := mcp.NewServer(
		&mcp.Implementation{
			Name:    "acme-catalog",
			Version: "0.1.0",
		},
		&mcp.ServerOptions{
			Instructions: "Use search_items to discover catalog item IDs before referring to an item.",
		},
	)

	destructive := false
	openWorld := false
	mcp.AddTool(
		server,
		&mcp.Tool{
			Name:        "search_items",
			Title:       "Search catalog items",
			Description: "Use this when the user needs to find catalog items by keyword.",
			InputSchema: map[string]any{
				"$schema": "https://json-schema.org/draft/2020-12/schema",
				"type":    "object",
				"properties": map[string]any{
					"query": map[string]any{
						"type":        "string",
						"minLength":   1,
						"description": "Keywords matched against item names and notes.",
					},
					"limit": map[string]any{
						"type":        "integer",
						"minimum":     1,
						"maximum":     50,
						"default":     10,
						"description": "Maximum number of matches to return.",
					},
				},
				"required":             []string{"query"},
				"additionalProperties": false,
			},
			Annotations: &mcp.ToolAnnotations{
				ReadOnlyHint:    true,
				IdempotentHint:  true,
				DestructiveHint: &destructive,
				OpenWorldHint:   &openWorld,
			},
		},
		searchItems,
	)

	return server
}

func main() {
	mcpServer := newMCPServer()
	mcpHandler := mcp.NewStreamableHTTPHandler(
		func(*http.Request) *mcp.Server {
			return mcpServer
		},
		&mcp.StreamableHTTPOptions{
			Stateless: true,
		},
	)

	mux := http.NewServeMux()
	mux.Handle("/mcp", mcpHandler)
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok\n"))
	})

	addr := os.Getenv("HTTP_ADDR")
	if addr == "" {
		addr = ":3000"
	}

	httpServer := &http.Server{
		Addr:              addr,
		Handler:           mux,
		ReadHeaderTimeout: 10 * time.Second,
		IdleTimeout:       90 * time.Second,
	}

	ctx, stop := signal.NotifyContext(
		context.Background(),
		os.Interrupt,
		syscall.SIGTERM,
	)
	defer stop()

	errCh := make(chan error, 1)
	go func() {
		log.Printf("MCP server listening on %s", addr)
		errCh <- httpServer.ListenAndServe()
	}()

	select {
	case <-ctx.Done():
		log.Print("shutdown requested")
	case err := <-errCh:
		if !errors.Is(err, http.ErrServerClosed) {
			log.Fatalf("HTTP server failed: %v", err)
		}
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := httpServer.Shutdown(shutdownCtx); err != nil {
		log.Fatalf("graceful shutdown failed: %v", err)
	}
}
```

The typed `SearchOutput` becomes `structuredContent`. The explicit `Content` remains useful to the model and to clients that do not render structured results specially.

## Production shape

Once the server grows, move toward:

```text
cmd/server/main.go
internal/domain
internal/service
internal/adapters/mcp
internal/adapters/upstream
internal/config
```

Keep the `mcp` import inside the MCP adapter and process entrypoint.

## Authentication

Wrap `/mcp` before the MCP handler:

```go
mux.Handle("/mcp", authenticate(mcpHandler))
```

The middleware should validate bearer token signature, issuer, audience, expiry, and required scopes, then place a small principal object in `context.Context`.

Do not forward that token upstream. Use token exchange or service-owned credentials.

## UI handoff

Do not change backend language to add an MCP App. Keep the Go server and follow `build-mcp-app`.

## Transport notes

- `Stateless: true` is required for the Go SDK's modern `2026-07-28` path.
- Leave the SDK's supported legacy negotiation available when broad client support matters.
- Avoid an HTTP `WriteTimeout` that can terminate long-lived streaming responses.
- Put request-size limits, rate limits, authentication, and structured access logs around the handler in production.
- Keep health, metrics, and administrative endpoints outside the MCP handler.
- Run multiple replicas without sticky sessions only after request state is externalized.

## Validation

```bash
gofmt -w .
go vet ./...
go test ./...
go build ./...
npx @modelcontextprotocol/inspector@latest
```

Then prove:

- modern `2026-07-28` requests
- every legacy version claimed
- invalid schema inputs
- deterministic list output
- auth failures
- retries and duplicate calls
- ChatGPT behavior
- secondary-client behavior when portability is claimed
