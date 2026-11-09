# Diagnose Codex annotation CSP failures

Use this diagnostic only when the application works normally but Codex annotation mode hides the pointer, shows a small black box, or cannot select an element in the in-app browser. Playwright can confirm the application's behavior, but a separate in-app-browser check must verify the annotation path.

## Confirm the failure boundary

1. Before entering annotation mode, confirm that the page renders correctly and ordinary pointer interaction works.
2. Enter annotation mode and reproduce the failure. Record the Codex desktop build and the exact route when practical.
3. Inspect the in-app browser console and network response. Browser developer mode can expose console output, response headers, and page state through CDP. Capture the exact CSP violation and the effective `Content-Security-Policy`, especially `style-src` and `style-src-elem` when present. A response header takes precedence over assumptions based on application source.
4. Inspect `#codex-browser-sidebar-comments-root`. If its shadow root is accessible, inspect `.interaction-layer` and `.interaction-blocker`, including their computed styles and bounding rectangles. A blocked stylesheet plus missing or very small interaction geometry supports the CSP diagnosis. Any one symptom alone does not prove it.
5. If the application styles render before annotation mode, do not change React, StyleX, or component CSS without separate evidence that those styles are faulty.

If the page has no strict style CSP, the console has no relevant violation, or the failure also occurs outside annotation mode, return to the normal testing workflow and diagnose the application or browser state on its own evidence.

## Choose a safe response

Do not add `style-src 'unsafe-inline'` as the default remedy. Do not weaken every application's CSP or edit a product policy merely to complete a test.

For a controlled application, an exact SHA-256 source expression for the annotation stylesheet can be an opt-in compatibility workaround when the user wants annotation support. Compute it from the exact stylesheet bytes injected by the active Codex build. Do not copy a hash from another report or build. Keep the strict policy, add only the exact hash, and prefer a development-only policy when annotation is needed only for local review. Do not ship the allowance to a deployed environment without explicit approval.

Treat the hash as build-specific and provisional. Recompute and reverify it whenever the injected stylesheet changes. Prefer a documented first-party Codex compatibility mechanism if OpenAI provides one later.

## Verify the actual workflow

After any approved remediation:

1. Reload the page and confirm the intended strict CSP is still present.
2. Confirm ordinary pointer interaction and application styling still work.
3. Enter annotation mode in the Codex in-app browser.
4. Confirm the interaction layer covers the viewport, the annotation pointer and hover target render, and an element can be selected.
5. Confirm the console no longer reports the relevant stylesheet violation.

A screenshot, a passing Playwright test, or visible overlay nodes does not complete this check. Successful element selection in annotation mode does.
