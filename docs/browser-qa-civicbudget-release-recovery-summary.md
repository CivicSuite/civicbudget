# CivicBudget Release-Recovery Browser QA

Date: 2026-05-07
Surface: `docs/index.html`
Tooling: Playwright Chromium, local file URL

## Viewports

| Viewport | Screenshot | Result |
|---|---|---|
| Desktop 1440 x 1000 | `browser-qa-civicbudget-release-recovery-desktop.png` | Passed |
| Mobile 390 x 844 | `browser-qa-civicbudget-release-recovery-mobile.png` | Passed |

## Checks

- Recovery copy visible: `published foundation label under suite-wide release-recovery review`.
- Recovery badge visible: `v0.1.2 foundation under recovery review`.
- Stale `Shipping v0.1.2` and `Ships Today` copy absent.
- Mojibake markers absent.
- No horizontal overflow at either viewport.
- Browser console errors: none.
- Page errors: none.
- Keyboard focus: first Tab lands on `read the release-recovery status`.

## Sign-Off Limit

This browser QA verifies the static recovery documentation surface only. It does not certify CivicBudget as product-ready or complete a future v1.0.0 module definition of done.
