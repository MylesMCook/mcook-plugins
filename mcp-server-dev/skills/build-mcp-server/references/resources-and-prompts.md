# Resources And Prompts

MCP defines three primary server-side primitives:

- tools
- resources
- prompts

Tools are model-driven. Resources are host-driven. Prompts are user-driven.

Most servers only need tools. Reach for the others when the integration shape does not fit "the model calls a function."

## Resources

A resource is data identified by a URI. The host reads it; it is not called like a tool.

Use a resource when:

- the host should browse or fetch content
- the content is better identified by URI than by tool input
- you are serving UI bundles or other structured assets

Use a tool instead when:

- the action has side effects
- the result depends on parameters the model should choose
- you want the model, not the host, to decide when to invoke it

## Prompts

A prompt is a parameterized message template surfaced as a slash command or menu action by the host.

Use a prompt when:

- users repeat the same workflow often
- the output should land directly in the conversation
- the server does not need to perform side effects

## Quick table

| You want to... | Use |
|---|---|
| Let the model fetch something on demand with arguments | Tool |
| Expose browsable context or UI bundles | Resource |
| Expose a family of URIs | Resource template |
| Give users a one-click workflow | Prompt |
| Ask the user a simple question mid-tool | Elicitation |
