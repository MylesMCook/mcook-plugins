# Decoupled Render Tools

Use this pattern when the widget is getting too stateful or when you want a cleaner separation between data and presentation.

## Pattern

- data tool: fetches authoritative data
- render tool: owns the widget resource and display flow
- app-only helper tools: optional, used by the widget for refresh or details

## Why it helps

- the model can still reason over the data tool directly
- the render tool can stay focused on UI
- the widget has a clear owner
- host fallbacks are easier because the data tool remains useful without UI

## Example split

```text
search_orders
render_order_picker
get_order_detail
```

The model can call `search_orders` when it needs discovery and `render_order_picker` when the user would benefit from an inline chooser.

## When to use it

- the UI is mostly a view over existing data
- the widget needs refresh or drilldown behavior
- you want to keep the tool catalog understandable

## When not to use it

- the widget is trivial and tightly bound to one tool
- splitting the tools would only add confusion
