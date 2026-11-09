# Stack routing

Use `stylex` alone for compiler integration, CSS extraction, syntax, tokens, themes, typed style contracts, styling migration, and general debugging. It does not require Base UI.

When a component combines Base UI and StyleX, `base-ui-stylex` leads its behavior and integration. Its references cover state callbacks, render composition, prop/ref preservation, portal theme inheritance, positioning, forms, and interaction checks. Use its current official Base UI documentation route before making component-specific decisions. If that skill is unavailable, start at https://base-ui.com/llms.txt and select the actual component-part and relevant handbook/utility pages.

Route existing shadcn component edits and explicit shadcn requests to `shadcn`. A `components.json` file does not make every component a shadcn component. Check the target's implementation and styling contract: a Base UI + StyleX component in that repository still uses `base-ui-stylex`; an existing shadcn component built on Base UI keeps its shadcn styling conventions.

Preserve project choices unless migration is explicitly requested. New work using Base UI + StyleX takes behavior and accessibility mechanics from Base UI and styling from StyleX. Tailwind, `cn()`, and shadcn conventions do not govern that combination. Plain React performance work does not activate this integration workflow.
