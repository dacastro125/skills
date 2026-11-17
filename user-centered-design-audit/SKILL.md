---
name: user-centered-design-audit
description: >-
  Audit frontend/UI codebases and interactive apps against User-Centered Design (UCD / DCU)
  principles: ISO 9241-210, ISO 9241-11, Don Norman (mental models, affordances, signifiers,
  natural mapping, immediate feedback, creeping featurism), Ben Shneiderman (direct manipulation),
  Henry Dreyfuss (ergonomics and error prevention), and verifiable technical acceptance criteria.
  Use when asked to audit or evaluate DCU/UCD, human-centered interaction, Norman/Shneiderman/Dreyfuss
  principles, or ISO 9241 compliance in HTML/CSS/JS, React, Vue, or Flutter ("auditar DCU",
  "principios de Norman", "audit UCD"). Skip for visual/brand restyling (use impeccable),
  Vercel Web Interface Guidelines (use web-design-guidelines), or backend-only/security audits.
---

# User-Centered Design (UCD / DCU) Audit

Read-only diagnostic audit verifying how UI design, interaction flows, and frontend architecture implement foundational User-Centered Design principles. Respond in the user's language and keep every claim grounded in observed code (`file:line`) or observed browser behavior.

Before evaluating any rule, read [references/clase-1-rubric.md](references/clase-1-rubric.md) for the exact observable signals, `Not applicable` conditions, and verifiable acceptance-criterion standard.

## Workflow

### 1. Map the Target First

1. **Check UI applicability:** Verify the target contains a user-facing UI layer (HTML/templates, components, screens, styles, or client-side interaction logic). If the target is backend-only, a non-interactive script, or a pure API with no UI, stop immediately and explain that UCD/UI auditing is out of scope rather than inventing UI findings.
2. **Exclude generated noise:** Skip `node_modules/`, `dist/`, `build/`, `.next/`, `.dart_tool/`, `coverage/`, and minified bundles unless no source exists.
3. **Infer context silently:** Infer the likely user profile, usage environment, and primary critical user flow from `README`, routes, entry points, and copy (or use any context the user provided). Do not stall the audit with pre-audit questionnaires unless the target is completely ambiguous.
4. **Trace the flow end-to-end:** Before scoring any principle, read the connected layout, router, state/persistence layer, and error handlers for the primary flow so you do not falsely flag behavior handled by a parent component.

Completion check: you can name the target user, environment, primary flow, and the exact files read.

### 2. Inspect Static Code First, Then Optional Live Browser

1. **Static pass (always first):** Inspect markup, component tree, CSS/layout, event handlers, async/error paths, state persistence, and schema-to-UI mapping against [references/clase-1-rubric.md](references/clase-1-rubric.md).
2. **Binary browser-audit check:** Only run a live browser check when **both** conditions hold:
   - The user provided a running URL or a self-contained local `.html` file, **and**
   - Focus order, keyboard reachability, responsive overflow, or runtime error/loading states cannot be confirmed from static code alone.
3. **Browser CLI fallback (ask before installing):**
   - Check if `agent-browser` or `playwright-cli` is available (`command -v` / `Get-Command`), or if a browser tool is already active.
   - If neither `agent-browser` nor `playwright-cli` is installed and live verification is needed for a deeper audit, **ask the user for explicit confirmation** before installing `agent-browser` (`npm i -g agent-browser && agent-browser install`).
   - If the user declines or no runtime is available, continue with the static audit and label runtime-dependent checks as `Not statically verifiable` (in the user's language) instead of guessing.

Completion check: every potential finding has verified `file:line` (or observed DOM/runtime) evidence.

### 3. Score Each Principle Strictly

Evaluate every principle in [references/clase-1-rubric.md](references/clase-1-rubric.md) using these five states (localized to the user's language):
- **Pass** (`Cumple`)
- **Partial** (`Parcial`)
- **Fail** (`No cumple`)
- **Not applicable** (`No aplica`) — when the product lacks that feature class (e.g., multi-step form persistence on a static page)
- **Not statically verifiable** (`No verificable estáticamente`) — when runtime/visual inspection is required and unavailable

Every reported failure must point to an observable signal in code or runtime behavior. If a principle cannot be verified from source alone (such as mental-model fit without domain context or unobservable runtime overflow), downgrade to `Not statically verifiable` rather than speculating.

### 4. Deliver the Audit Report (Read-Only)

Do not edit target project files during the audit. Output directly in chat (write a `.md` file only if the user explicitly requests one) using this structure in the user's language:

1. **Inferred Context:** Target user profile, assumed environment, primary flow audited, and files/paths inspected (plus whether live browser inspection ran).
2. **Principle Compliance Table:** Compact table covering all 9 rubric dimensions with their status (`Pass` / `Partial` / `Fail` / `Not applicable` / `Not statically verifiable`) and a one-line note.
3. **Prioritized Findings (max 15):** Group by severity (`Critical` → `High` → `Medium`; omit empty groups; note if lower-priority items were omitted). Each finding must include:
   - **Principle violated**
   - **Evidence** (`file:line` or exact runtime selector/observation)
   - **User impact**
   - **Suggested fix** (minimal design or code change)
   - **Verifiable technical acceptance criterion** (binary QA/E2E assertion — measurable, never vague aesthetic advice)
4. **Next Step Offer:** Briefly offer to apply fixes for specific findings if the user confirms afterward.
