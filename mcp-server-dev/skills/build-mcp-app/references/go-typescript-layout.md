# Go Server Plus TypeScript MCP App Layout

Use this layout when a Go MCP server needs optional inline UI.

## Repository shape

```text
.
|-- cmd/server/main.go
|-- internal/domain/
|-- internal/service/
|-- internal/adapters/mcp/
|-- internal/widgetassets/
|   |-- embed.go
|   `-- catalog-results-v1.html
|-- web/
|   |-- package.json
|   |-- tsconfig.json
|   |-- vite.config.ts
|   |-- catalog-results.html
|   `-- src/catalog-results.ts
|-- go.mod
`-- README.md
```

Configure the frontend build to emit one bundled HTML file into `internal/widgetassets/`. Keep frontend dependencies out of the Go runtime.

## Embed the built resource

```go
package widgetassets

import _ "embed"

//go:embed catalog-results-v1.html
var CatalogResultsHTML string
```

## Register metadata and resource in Go

The official Go SDK exposes protocol metadata through `mcp.Meta`.

```go
const (
	catalogWidgetURI  = "ui://catalog/results-v1.html"
	mcpAppHTMLMIMEType = "text/html;profile=mcp-app"
)

func addCatalogWidget(server *mcp.Server) {
	widgetMeta := mcp.Meta{
		"ui": map[string]any{
			"resourceUri": catalogWidgetURI,
		},
		// Optional ChatGPT compatibility alias.
		"openai/outputTemplate": catalogWidgetURI,
	}

	mcp.AddTool(server, &mcp.Tool{
		Name:        "render_catalog_results",
		Title:       "Show catalog results",
		Description: "Use this after search_items when an interactive result list would help the user compare or select items.",
		Meta:        widgetMeta,
	}, renderCatalogResults)

	resourceMeta := mcp.Meta{
		"ui": map[string]any{
			"prefersBorder": true,
			"csp": map[string]any{
				"connectDomains":  []string{},
				"resourceDomains": []string{},
			},
		},
	}

	server.AddResource(&mcp.Resource{
		URI:      catalogWidgetURI,
		Name:     "catalog-results",
		Title:    "Catalog results",
		MIMEType: mcpAppHTMLMIMEType,
		Meta:     resourceMeta,
	}, func(context.Context, *mcp.ReadResourceRequest) (*mcp.ReadResourceResult, error) {
		return &mcp.ReadResourceResult{
			Contents: []*mcp.ResourceContents{
				{
					URI:      catalogWidgetURI,
					MIMEType: mcpAppHTMLMIMEType,
					Text:     widgetassets.CatalogResultsHTML,
					Meta:     resourceMeta,
				},
			},
		}, nil
	})
}
```

The handler should return a useful `content` summary and typed output for `structuredContent`. Do not return HTML from the tool handler.

Pin the Go SDK and recheck the exact API when upgrading. Keep the metadata assembly in the MCP adapter so domain and service packages do not import MCP types.

## Minimal component entry

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

type CatalogResult = {
  items: Array<{ id: string; name: string; notes?: string }>;
};

const app = new App({ name: "Catalog Results", version: "1.0.0" });
const root = document.querySelector<HTMLElement>("#root");

app.addEventListener("toolresult", (result) => {
  const data = result.structuredContent as CatalogResult | undefined;
  if (!root) return;

  if (!data?.items.length) {
    root.textContent = "No catalog items found.";
    return;
  }

  root.replaceChildren(
    ...data.items.map((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = item.name;
      button.addEventListener("click", () => {
        void app.sendMessage({
          role: "user",
          content: [{ type: "text", text: `Use catalog item ${item.id}.` }],
        });
      });
      return button;
    }),
  );
});

await app.connect();
```

## Build contract

A release build must:

1. install frontend dependencies from a lockfile
2. type-check the component
3. bundle the component into a deterministic HTML file
4. verify the expected output path exists
5. compile and test the Go server with the embedded asset
6. fail CI when the frontend source changed but the embedded artifact is stale

Prefer one release artifact containing the Go server and embedded UI. Separate asset hosting is valid when cache policy, CSP, and deployment ownership are explicit.
