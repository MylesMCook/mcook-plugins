# Documentation routing

## Route across the full Base UI index

Keep the index live instead of copying a fixed component catalog or release list into this skill. Select pages by the task's question and follow relevant cross-links until the implementation decision is supported. Fetch independent relevant pages together when useful; do not download the entire documentation site by default.

| Task or question | Route from the current index |
| --- | --- |
| Initial setup or global integration | [Quick start](https://base-ui.com/react/overview/quick-start.md), then the actual framework's StyleX setup guide. |
| New interactive UI, keyboard/focus behavior, or accessibility review | [Accessibility](https://base-ui.com/react/overview/accessibility.md), plus the specific component's guidance. |
| Upgrade, regression, deprecated API, or version mismatch | [Releases](https://base-ui.com/react/overview/releases.md), then the installed/target releases and relevant intervening changes. Distinguish stable and prerelease versions. |
| Library fit, project background, or ecosystem/support options | [About](https://base-ui.com/react/overview/about.md) or [Community](https://base-ui.com/react/overview/community.md). Verify third-party compatibility at the linked project's source. |
| Choosing or implementing any component | Search all current Components entries for the required behavior. Read the matching component and relevant alternatives before inventing a substitute; similar names do not imply equivalent semantics. |
| Styling, animation, composition, behavior, forms, or types | Use the handbook routes below alongside the component API. |
| CSP requirements affecting Base UI inline output | [CSP Provider](https://base-ui.com/react/utils/csp-provider.md). Do not change security policy merely to make an example work. |
| RTL or direction-aware interaction | [Direction Provider](https://base-ui.com/react/utils/direction-provider.md), plus relevant component behavior and logical StyleX properties. |
| Combining behavior props | [mergeProps](https://base-ui.com/react/utils/merge-props.md); distinguish prop merging from StyleX style resolution. |
| Adding render composition to a custom component | [useRender](https://base-ui.com/react/utils/use-render.md), together with Composition and TypeScript. Use only when the component needs that contract. |

For example, an RTL animated dialog may need Dialog, Accessibility, Animation, and Direction Provider; a validated select may need Select, Forms, and TypeScript. These illustrate contextual routing, not mandatory bundles for every edit.

## Route to the relevant Base UI handbook

Fetch the applicable pages live rather than loading the entire handbook for every task. Pair handbook guidance with the exact component-part API and the corresponding StyleX API.

| Task or uncertainty | Official page to read | Integration question to resolve |
| --- | --- | --- |
| Styling a part or state | [Styling](https://base-ui.com/react/handbook/styling.md) | Which class/style callbacks, states, and CSS variables can StyleX consume? |
| Enter/exit transitions or animated overlays | [Animation](https://base-ui.com/react/handbook/animation.md) | Which lifecycle states and mounting behavior must the StyleX motion preserve? |
| Custom render targets or reusable wrappers | [Composition](https://base-ui.com/react/handbook/composition.md) | How must render props, refs, and DOM props be forwarded? Also read mergeProps when manually combining props. |
| Controlled state or event behavior changes | [Customization](https://base-ui.com/react/handbook/customization.md) | Which change-event details and cancellation/propagation APIs apply? Do not substitute native-event assumptions. |
| Labels, submission, validation, or form-library integration | [Forms](https://base-ui.com/react/handbook/forms.md) | How are controls named, values submitted, and errors associated? Read the section for the project's existing form library only when relevant. |
| Wrapper props, generics, refs, or event types | [TypeScript](https://base-ui.com/react/handbook/typescript.md) | Which exported types and inference patterns match the installed package? |

If a retrieval tool rejects a Markdown content type, open the same official page without `.md`, or use another supported reader. Do not interpret that tool error as missing documentation. Rediscover changed paths through llms.txt.
