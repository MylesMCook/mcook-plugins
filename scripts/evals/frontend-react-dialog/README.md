# Base UI + StyleX dialog evaluation

A bounded integration test, not a starter or a component catalog. Dependencies are pinned in package-lock.json. This fixture lives outside the plugin bundle so dependency installs do not become package contents.

Run `npm ci`, `npm run lint`, `npm run build`, then `npm test` in this directory. Tests use an already installed Google Chrome, one worker, and a task-local production preview on loopback port 4183. They fail if that port is occupied. No browser installation or global package changes are required.

The two viewport cases verify Enter/Space opening, accessible name/description, modal accessibility isolation, initial focus, forward/backward focus containment, visible keyboard focus, Escape/Close/backdrop dismissal, focus return, preserved consumer handlers, static and dynamic state styling, emitted and loaded CSS, live portal theme changes, and narrow-screen containment. Screenshots go to ignored test-results directories.

The implementation follows the [Dialog part APIs](https://base-ui.com/react/components/dialog), [render composition](https://base-ui.com/react/handbook/composition), and [mergeProps contract](https://base-ui.com/react/utils/merge-props). The callback applies the full StyleX result before Base UI props so internal inline values survive. Ref composition is unnecessary because it introduces no additional callback ref. A documented initialFocus ref verifies the existing focus path.

[StyleX's Vite integration](https://stylexjs.com/docs/learn/installation/vite/vite-react) supplies compiler ordering and CSS extraction. [Theme application](https://stylexjs.com/docs/learn/theming/creating-themes/) affects DOM descendants: the open portal is outside main, so the fixture applies the active theme at both boundaries. This is an integration choice verified by computed colors in the browser, not a claim that React context carries CSS variables.

Reviewed 2026-09-08 with Base UI 1.8.0 and StyleX 0.19.0. This single dialog does not validate forms, anchored positioning, animations, SSR/hydration, screen-reader speech, or all Base UI components. The linked official pages must still be consulted for future version-sensitive work.
