# Component routing

Apply shadcn conventions to existing shadcn components or explicit shadcn requests. Inspect the target component's imports, implementation, and styling contract; components.json does not make every component in a mixed project a shadcn component.

Base UI + StyleX components use base-ui-stylex for behavior and integration, with stylex supporting general styling and compiler work. Tailwind, cn(), shadcn variants, and component conventions in this skill do not govern those components. Existing shadcn components may use Base UI internally; preserve their actual styling contract unless migration is requested.

Plain React performance work uses relevant performance guidance without adding a Base UI workflow.
