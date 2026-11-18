---
name: usability-heuristics-audit
description: >-
  Audit UI design, flows, microcopy, forms, and frontend code (HTML/CSS/JS, React, Vue, Flutter)
  against Usability frameworks: Nielsen's 10 Heuristics & 5 Attributes, Jakob's Law, Deniese
  Pierotti's 225 active Xerox rules (+ 22 conditional runtime/docs), Shneiderman's 8 Golden Rules,
  Steve Krug, Janice Redish, Quesenbery's 5 Es, Preece, ISO 9241-11/9126, and the 4 web
  abandonment causes. Delivers a prioritized chat report plus a full item-by-item checklist
  markdown at project root. Trigger whenever asked to audit usability, fix confusing navigation,
  links, error copy, or form friction, or reduce web abandonment—even without naming Nielsen or
  Pierotti ("auditar usabilidad", "heurísticas de Nielsen", "checklist Pierotti", "evaluación
  heurística", "No me hagas pensar", "8 reglas de oro"). Skip for Class 1 UCD/DCU
  (user-centered-design-audit), restyling (impeccable), Vercel lint (web-design-guidelines),
  E2E/scraping, pure theory Q&A, or backend-only logic.
---

# Usability Heuristics & Pierotti 225 Audit

Diagnostic usability audit verifying UI design, microcopy, navigation architecture, error handling, and frontend interaction code. Match the user's language in both the chat report and the generated checklist file, and keep every claim grounded in observed source code (`file:line`) or live browser inspection.

This audit never modifies target source code. The only file written in an audited UI project is the checklist report (`auditoria-usabilidad-checklist.md` or `usability-audit-checklist.md`) so the team gets a complete item-by-item artifact without polluting application code.

Before evaluating any rule, read both references to align scoring states and observable signals:
- [references/frameworks-rubric.md](references/frameworks-rubric.md) (9 filtered Class 2 frameworks, 8 consolidated pillars, severity rules, verifiable technical criteria)
- [references/pierotti-225-checklist.md](references/pierotti-225-checklist.md) (all 225 active Pierotti criteria across 11 areas + 22 conditional Group B items)

## Workflow

### 1. Map the Target First

1. **Check UI applicability:** Confirm the target has a user-facing UI layer (HTML, templates, components, screens, CSS, or client interaction handlers). If the target is backend-only, a non-interactive utility, or pure domain logic with no UI, stop immediately, state that usability UI auditing is out of scope, and do **not** create any `.md` checklist file.
2. **Exclude generated noise:** Skip `node_modules/`, `dist/`, `build/`, `.next/`, `.dart_tool/`, `coverage/`, and minified bundles unless no source exists.
3. **Infer context silently:** Identify user profile (`novato`/`experto`/`general` for `11.3`/`11.4`), usage environment (`desktop`/`mobile`), primary critical flow, and whether an integrated help/documentation portal exists (`10.10–10.18`).
4. **Trace connected flows end-to-end:** Read layouts, routers, state stores, form validators, and async error paths together so you do not flag missing feedback or guards already handled by a parent container.

### 2. Static Pass First, Then Optional Live Browser (`agent-browser` / `playwright-cli`)

1. **Always run static analysis first:** Audit markup semantics, CSS/tokens, visual hierarchy, headings/links (Redish), responsive rules, keyboard/focus handling, form constraints, and error copy against both reference files.
2. **Binary live-browser condition:** Only inspect in a live browser when **both** conditions apply:
   - A running URL or self-contained local `.html` file is available, **and**
   - Runtime signals cannot be confirmed statically (response timing `1.17–1.24`, actual `Tab` order, computed `:focus-visible` contrast, `375px` and `320px` mobile overflow including clipped children inside `overflow: hidden` boxes, or live DOM loading/embed error states).
3. **Browser tool check (ask consent before installing):**
   - Check for `agent-browser` or `playwright-cli` (`Get-Command` / `command -v`), or an active browser session.
   - If neither CLI is installed and live verification is needed for a deeper audit, ask the user for explicit confirmation before running `npm i -g agent-browser && agent-browser install`.
   - When driving `agent-browser`, prefer short synchronous invocations (`eval -b <base64>`, `press`, `set viewport`) over piping multi-line async promises through `--stdin`, and always close the session cleanly.
   - If the user declines or no runtime exists, proceed statically and mark runtime-only checks (`1.17–1.24` and dynamic overlap/overflow) as `No verificable estáticamente` / `Not statically verifiable` rather than guessing.

### 3. Score Every Criterion Strictly

Evaluate every framework pillar and all `225 + 22` Pierotti items using exactly five states (localized to the prompt's language):
- **Cumple / Pass**
- **Parcial / Partial**
- **No cumple / Fail**
- **No aplica / Not applicable** — when the target lacks that component/feature class (e.g., draft persistence on a 1-field search form, docs portal checks `10.10–10.18` when no help site exists)
- **No verificable estáticamente / Not statically verifiable** — when runtime execution, missing business profile, or external style guide is required

Escalate issues matching any of the **4 Web Abandonment Causes** (confusing navigation, incomprehensible jargon/copy, unindicated waits/missing exits, blocking errors/lost form state/gratuitous login walls) to `Critical` (`Crítico`) or `High` (`Alto`).

### 4. Write the Full `225 + 22` Checklist `.md` at Project Root

On every valid UI audit, write a companion Markdown file in the audited project's root directory (or the audited file's directory when targeting a standalone HTML file):
- Spanish prompt -> `auditoria-usabilidad-checklist.md`
- English prompt -> `usability-audit-checklist.md`

**Collision policy:** If that filename already exists and the user did not ask to overwrite or archive by date, ask briefly whether to overwrite it or write with a date suffix (`-YYYY-MM-DD.md`) instead of overwriting prior audits silently.

Include in the generated `.md`:
1. Header metadata (target path, date, audit mode `Static` vs `Static + Live Browser`) and status counts across the **225 Group A** and **22 Group B** items.
2. Summary status across the **8 Consolidated Pillars** and **Nielsen H1–H10**.
3. Complete 1-by-1 tables covering all **225 Group A items** across the 11 areas (`| ID | Area / Categoría | Criterio | Estado | Evidencia / Justificación (`file:line` o razón de `No aplica`) |`) without omitting or collapsing ranges.
4. Conditional **Group B appendix (`22` items)**: `1.17–1.24`, `3.23`, `4.3`, `10.10–10.18`, `11.3`, `11.4`, `11.9` with observed evidence or explicit `No aplica` / `No verificable estáticamente`.

To generate this `.md` fast with guaranteed exact counts (`0` skipped items), write a compact evaluation JSON (`meta`, optional feature-class `bulk_rules`, and `items`) to a temp path and run `python <skill-dir>/scripts/render_checklist.py render --input <eval.json> --output <checklist.md>` (deleting the temp JSON afterward), or verify manually written tables with `render_checklist.py validate <checklist.md>`.

### 5. Deliver the Chat Report & Next-Step Offer

Present the summary cleanly in chat in the user's language:
1. **Inferred Context:** Target user, environment, primary flow, whether a docs portal exists, inspected files, and whether live browser inspection ran.
2. **Generated Checklist Link:** Clickable `file:///` link to `auditoria-usabilidad-checklist.md` / `usability-audit-checklist.md` with its exact Pierotti summary counts (`225` Group A + `22` Group B).
3. **Compliance Table (8 Pillars & Nielsen `H1–H10`):** Status + key Pierotti IDs per row + concise observation.
4. **Prioritized Findings (max 15 in chat):** Ordered `Critical` -> `High` -> `Medium` (note if additional minor findings live in the `.md`). Each finding must state:
   - **Rule violated & Pierotti IDs** (e.g., `Nielsen H5 · Shneiderman #5 · Pierotti 5.15, 6.11`)
   - **Evidence** (`file:line` or live browser selector/observation)
   - **User impact** (note any Web Abandonment Cause triggered)
   - **Suggested fix** (minimal design or code change)
   - **Verifiable technical acceptance criterion** (binary QA/E2E assertion from [references/frameworks-rubric.md](references/frameworks-rubric.md))
5. **Next Step Offer:** Briefly offer to apply minimal fixes for specific findings once confirmed.
