# CivicBudget Audit-Full Packet

Date: 2026-05-07
Repo: `CivicSuite/civicbudget`
Mode: release-recovery gate
Local commit audited before fixes: `68b25e5`

## 1. Executive Audit

Static audit confidence: High for release-script, docs, dependency, and tests inspected locally.
Runtime sign-off confidence: High for this release-recovery scope after WSL release verification and browser QA passed.

CivicBudget had material release-truth drift: current docs still referenced v0.1.1 and CivicCore v0.3.0, package metadata depended on unresolved `civiccore==0.4.0` while CI preinstalled the wheel, and public copy used "Shipping" language during suite-wide recovery.

## 2. Audit Coverage Ledger

| Area | Status | Evidence |
|---|---|---|
| Engineering | Checked | pyproject, workflow, release script, runtime tests |
| Security and authorization | Checked | bearer-token retrieval protection tests inspected |
| UI/UX | Checked | docs and public UI updated; Playwright desktop/mobile browser QA passed |
| Product/PM | Checked | provisional foundation label added |
| Documentation | Checked | README/manual/text docs/changelog/docs index/recovery status |
| Install/bootstrap/seeding | Checked | dependency changed to published CivicCore v0.4.0 wheel |
| Version/release consistency | Checked | stale v0.1.1/v0.3.0 current docs corrected |
| Test engineering | Checked | regression tests added for verifier/docs/dependency/status |
| Runtime QA | Checked | WSL release gate passed; browser QA passed |
| Cross-cutting synthesis | Checked | main issue class is release evidence and source-of-truth drift |

## 3. Claim Verification Matrix

| Claim | Result | Evidence |
|---|---|---|
| CivicBudget is not product-ready | Verified static | README/manual/recovery status |
| Version remains `0.1.2` | Verified static | package, pyproject, release script |
| Fresh install can resolve CivicCore | Verified | WSL temp venv installed `civiccore-0.4.0` and `civicbudget-0.1.2` |
| Current docs no longer claim v0.1.1/v0.3.0 | Verified static | user manual and text manual updated |
| Browser docs are readable | Verified | Playwright desktop/mobile QA passed with no console/page errors |

## 4. What The Dev Team Needs To Do Now

1. Push the recovery branch.
2. Open a PR.
3. Confirm GitHub CI runs the release gate without a hidden CivicCore preinstall.
4. Merge only after CI is green.

## 5. Next-Sprint Watchlist

- Full CivicBudget v1.0.0 scope remains future active-module work.
- Production claims require real user-flow Playwright tests, runtime install proof, consistency gates, docs-source enforcement, and security scans.

## 6. Engineering Deep Dive

Finding ENG-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: CI should not hide unresolved package metadata.
Evidence: `pyproject.toml` used `civiccore==0.4.0`; workflow separately installed the CivicCore wheel.
Blast radius: fresh installs, CI evidence, WSL release proof.
Fix: use the published CivicCore v0.4.0 release wheel directly and allow Hatch direct references.

## 7. Security And Authorization Deep Dive

Existing persisted retrieval auth tests cover missing auth configuration and bearer-token requirements. This recovery patch does not expand access surfaces.

## 8. UI/UX Deep Dive

Finding UX-001
Severity: Major
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: First-viewport "Shipping" language overstates release confidence during recovery.
Evidence: docs index and public UI used "Shipping v0.1.2" / "Ships Today".
Blast radius: public trust and status interpretation.
Fix: use "foundation under recovery review" and add browser QA proof.

## 9. Product/PM Deep Dive

CivicBudget is useful as a deterministic budget workpaper foundation but is not production budget software. Finance staff remain responsible for all numbers and public statements.

## 10. Documentation Deep Dive

Finding DOC-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: Current docs contradicted package metadata and release history.
Evidence: user manual and text manual referenced v0.1.1 and CivicCore v0.3.0 while package version is v0.1.2.
Blast radius: install instructions, public trust, release consistency.
Fix: update current docs to v0.1.2 and CivicCore v0.4.0 release wheel.

## 11. Install / Bootstrap / Seeding Deep Dive

The package now resolves CivicCore from the published v0.4.0 release wheel without a hidden workflow preinstall.

## 12. Version And Release Consistency Deep Dive

Version remains `0.1.2`. This patch does not promote CivicBudget to v1.0.0.

## 13. Test Engineering Deep Dive

Regression tests cover Python launcher order, WindowsApps fallback removal, direct CivicCore wheel dependency, docs gate markers, current-doc version/pin currency, recovery copy, and public UI wording.

## 14. Runtime QA Deep Dive

WSL fresh install resolved CivicCore from the published v0.4.0 wheel and imported `civicbudget==0.1.2` on Linux. WSL `scripts/verify-release.sh` passed with `22 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums created. Playwright Chromium verified the recovery docs at desktop and mobile widths with no console errors, page errors, mojibake, stale shipping language, or horizontal overflow; keyboard focus reached the recovery evidence link.

## 15. Cross-Cutting Synthesis

CivicBudget's core recovery issue is source-of-truth drift plus release-evidence trust. The patch makes current docs and install proof match package reality.

## 16. Verification Gaps And Sign-Off Limits

This packet does not certify CivicBudget as product-ready. It certifies only that the current published foundation label is truthfully represented and locally verifiable for the release-recovery scope.
