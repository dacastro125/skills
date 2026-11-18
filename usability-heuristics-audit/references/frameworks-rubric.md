# Usability Engineering Frameworks Rubric (Design & Code)

Closed-scope operational rubric consolidating the UI design, microcopy, interaction flow, and frontend engineering rules from Class 2 (Nielsen, ISO 9241-11 / 9126, Preece, Redish, Quesenbery, Shneiderman, Krug, and Web Abandonment Causes). Flag a failure only when backed by an observable signal in static source (`file:line`) or live browser execution.

## Table of Contents
1. [Filtered Theoretical Frameworks (9 Sources)](#1-filtered-theoretical-frameworks-9-sources)
2. [8 Consolidated Operational Pillars](#2-8-consolidated-operational-pillars)
3. [Severity Rules & Web Abandonment Escalation](#3-severity-rules--web-abandonment-escalation)
4. [Verifiable Technical Acceptance Criterion Standard](#4-verifiable-technical-acceptance-criterion-standard)

---

## 1. Filtered Theoretical Frameworks (9 Sources)

### 1.1 Jakob Nielsen — 5 Quality Attributes *(observable proxies only)*
* **Learnability:** Verify clear visual hierarchy, standard UI conventions, scannable labels, initial microcopy/onboarding hints, and task-aligned menus.
* **Efficiency:** Verify minimal step count for frequent paths, sensible default values, `autocomplete` attributes, keyboard navigation/shortcuts, and quick filtering on long lists.
* **Memorability:** Verify recognition cues over recall (text alongside icons, breadcrumbs, recent-item/filter visibility, consistent layout slots).
* **Errors (Low rate & recovery):** Verify inline validation near inputs, constraints (`type`, `min`/`max`), confirmation on destructive actions, Undo/Cancel paths, and actionable error recovery.
* **Out of scope (`Not statically verifiable`):** **Subjective user satisfaction** and empirical time-on-task / error-rate measurements with human participants (`SUS`, moderated usability tests).

### 1.2 Jakob Nielsen — 10 Heuristics (`H1–H10`) + Jakob's Law + Slips vs. Mistakes
| # | Heuristic | Concrete Code / UI Signals to Verify | Out-of-Scope / `Not applicable` |
|---|---|---|---|
| **H1** | **Visibility of System Status** | `<title>`/`<h1>` per view; active nav/tab markers (`aria-current`, `aria-selected`); loading spinners/progress indicators on async actions; `aria-live="polite"` / `"assertive"` announcements; post-action completion confirmation. | Purely static documents with no mutable state or async operations (`No aplica` for async/loading feedback). |
| **H2** | **Match Between System & Real World** | Human-language copy free of internal backend/DB terms (`UUID`, `500`, `snake_case`, raw enums, `Lorem Ipsum`); logical/natural sequence (days, chronological steps, country→city); localized numeric/currency formatting (`Intl.NumberFormat`). | Developer-facing devtool where technical identifiers/JSON schemas are explicitly the user task (`No aplica` for jargon flag). |
| **H3** | **User Control & Freedom** | Clear *Cancel* / *Back* buttons preserving form values; full modal/drawer exit (`Esc`, close button, backdrop click); *Undo* / *Redo* on destructive or batch edits; abortable requests (`AbortController`). | Read-only displays with zero dialogs, forms, or mutations (`No aplica`). |
| **H4** | **Consistency & Standards (Jakob's Law)** | Shared design tokens/patterns across views; familiar external platform conventions (cart top-right, search bar, standard modal close, links vs buttons); identical verbs and nouns across routes (`Delete` everywhere vs mixing `Erase`/`Remove`). | Isolated single fragment embedded into a host app (`No verificable estáticamente` for host-wide consistency). |
| **H5** | **Error Prevention (*Slips* vs. *Mistakes*)** | Prevent **slips** (inadvertent action on right goal): space apart destructive actions from primary CTAs, guard double-click submit (`disabled` while pending), prevent autocomplete/popovers from covering fields, enforce adequate tap targets (~36–44px+). Prevent **mistakes** (wrong mental model/plan): typed inputs (`email`, `date`, `number`), `min`/`max`, clear helper formats, inline validation before submit, destructive confirmation explaining exact impact. | Purely static content with zero interactive controls or inputs (`No aplica`). |
| **H6** | **Recognition Rather Than Recall** | Icons paired with labels or tooltips; clear distinction between single-choice (`radio`) and multi-choice (`checkbox`); visible selection summaries across steps; conditional dependent fields shown only when relevant; marked optional/required fields. | Minimal widgets with <= 2 self-evident controls (`No aplica` for complex state memory). |
| **H7** | **Flexibility & Efficiency of Use** | Keyboard operability (`Tab`, arrow keys, `Enter`, `Esc`); optional shortcuts/search (`/`, `Ctrl+K`) without blocking novices or requiring cryptic codes; partial draft persistence (`localStorage` / draft save) in long/multi-step forms; client-side type-ahead/filter on >7-item lists. | Short 1–3 field forms (e.g., simple search box) (`No aplica` for draft persistence/shortcuts). |
| **H8** | **Aesthetic & Minimalist Design** | High signal-to-noise ratio: remove filler paragraphs, redundant decorative boxes, competing promo banners, and unnecessary columns obscuring the main task; concise headings and short labels. | Always assessable whenever a view or component renders UI. |
| **H9** | **Recognize, Diagnose & Recover from Errors** | **Three-part error anatomy:** (1) visibility not relying on color alone (`aria-invalid` + icon/border + text), (2) human-language cause without raw stack traces or blameful wording (`fatal`, `illegal`), (3) direct recovery action (*Retry*, format example, *Back to home* on 404/500). Focus/scroll moves to first invalid field on failed submit. | Views with zero error paths or user inputs (`No aplica`). |
| **H10** | **Help & Documentation** | Task-oriented inline help/tooltips near complex inputs; contextual help accessible without losing unsaved form/scroll state (`drawer`, modal, `<details>`, `target="_blank" rel="noopener"`); clean progressive disclosure (*More info*). | Trivial single-action UI requiring no explanation (`No aplica`). |

### 1.3 ISO 9241-11 (Nigel Bevan) & ISO/IEC 9126
* **Technical Effectiveness:** End-to-end flows complete without dead ends, broken routes, uncaught promise rejections, or keyboard/touch traps.
* **Structural Efficiency:** Zero redundant confirmation screens, duplicate data entry, or blocking synchronous waits when avoidable.
* **Equipment & Environment Adaptation:** Responsive breakpoints (`375px` mobile through desktop) with zero unintended horizontal overflow (`scrollWidth <= innerWidth`), adequate contrast, and explicit handling of slow network / timeout / offline states.
* **ISO/IEC 9126 UI sub-characteristics:** Operability, understandability, and interface consistency across views.
* **Out of scope (`Not statically verifiable`):** Empirical completion rates, measured human task duration without runtime, `NASA-TLX`, `SUS`, `NPS`.

### 1.4 Jennifer Preece (*Interaction Design*)
* **6 Design Principles (100% applicable):** *Visibility*, *Feedback*, *Constraints* (`min`/`max`, `disabled`, selectors over free text), *Mapping* (natural spatial alignment between controls and affected items), *Consistency*, *Affordance* (native interactive semantics vs passive text).
* **5 Usability Goals (applicable via design/code):** *Effectiveness*, *Efficiency*, *Safety* (guarding against data loss/accidental deletes), *Learnability*, *Memorability*.
* **Out of scope:** Product *Utility* (business feature-market fit) and subjective emotional UX goals (*Fun, Entertaining, Emotionally fulfilling*), unless blatant hostile friction blocks use.

### 1.5 Janice Redish (*Letting Go of the Words*)
* **Optimize for Skimming & Scanning:** Proper semantic heading outline (`<h1>` -> `<h2>` -> `<h3>` without skipped levels), concise chunks, scannable lists and structured tables rather than walls of prose.
* **Meaningful Action Links:** Every `<a>` / link must describe its destination or action with specific words; flag generic *"Click here"*, *"Clic aquí"*, *"Ver más"*, *"Read more"*, or raw URLs lacking contextual labels.
* **Live HTML over Forced Static Documents:** Flag forcing PDF/DOC downloads for operational instructions, policies, or forms that can live directly in accessible responsive HTML.
* **Conversational Clarity:** Active voice, direct user-focused wording without corporate or bureaucratic jargon.
* **Out of scope:** Long-form editorial *Personas* definition and external blog content marketing strategy.

### 1.6 Whitney Quesenbery — The 5 Es
* **Applicable (`4/5`):** *Effective* (completable paths), *Efficient* (few steps, defaults, `autocomplete`, shortcuts), *Error tolerant* (preventive input constraints, `trim()`/case tolerance, undo & non-destructive recovery), and *Easy to learn* (clear initial orientation & progressive help).
* **Out of scope:** *Engaging* (subjective emotional immersion/delight).

### 1.7 Ben Shneiderman — 8 Golden Rules
1. **Strive for consistency:** Uniform terminology, sequences, layout slots, and styling across screens.
2. **Enable frequent users to use shortcuts:** Direct keyboard shortcuts/quick actions without degrading novice discoverability.
3. **Offer informative feedback:** Feedback proportional to action importance (subtle inline cue vs explicit completion toast/dialog).
4. **Design dialog to yield closure:** Explicit beginning, progression, and final confirmation/receipt state on transactions and multi-step flows (never silently returning or leaving uncertainty whether submission succeeded).
5. **Offer simple error handling & prevention:** Catch errors early inline, allow fixing without erasing valid already-entered inputs.
6. **Permit easy reversal of actions:** *Undo*, *Cancel*, *Back* navigation preserving entered state.
7. **Support internal locus of control:** User initiates actions; flag surprise auto-redirects, unrequested timer navigations, unmuted `autoPlay`, or unexpected focus hijacking.
8. **Reduce short-term memory load:** Keep summary/context visible across multi-page steps (cart totals, selected plan, entered summary) instead of making users memorize values from previous screens.

### 1.8 Steve Krug — *Don't Make Me Think*
* **1st Law ("Don't Make Me Think") & Self-Evident Design:** Zero ambiguous labels, mysterious icons, or riddle-like button copy forcing users to guess outcomes.
* **Follow Conventions:** Place navigation, search, login, settings, and dialog controls in familiar expected locations.
* **Clear Visual Hierarchy:** Visual prominence proportional to task importance; proximity grouping separating distinct sections cleanly.
* **Clearly Clickable Areas (True Affordance):** Visible button/link boundaries, contrast, `cursor: pointer`, `:hover`/`:focus-visible`; flag **false affordances** (underlined or button-styled non-clickable text/cards).
* **3rd Law ("Omit Needless Words") & Scannability:** Cut welcome fluff, repetitive instructions over forms, and bloated labels.
* **2nd Law (Clarity over artificial click-count):** Never pack dense choices into cryptic micro-widgets just to claim "fewer clicks" when clear step-by-step choices reduce thinking.
* **Theory/research outside code:** Descriptive cognitive models (*Satisficing*, *Muddle through*) explain rationale; DIY 3-user testing sessions lie outside static audit.

### 1.9 The 4 Web Abandonment Causes
Use these to escalate severity whenever found in real flows:
1. **Confusing navigation & information architecture** -> Escalate to **High / Critical**.
2. **Incomprehensible or task-misaligned content / jargon** -> Escalate to **High**.
3. **Missing feedback / unexplained waits without progress or cancel exit** -> Escalate to **Critical / High**.
4. **Technical errors, confusing forms, or gratuitous obstacles** (such as forced login walls blocking exploration before commitment, broken submit states, or lost draft input) -> Escalate to **Critical**.

---

## 2. 8 Consolidated Operational Pillars

Use these 8 pillars for the chat compliance table (mapping seamlessly to Pierotti's active categories and the 9 frameworks above):

| # | Pillar | Origin Frameworks | Mapped Pierotti Areas | Core Observable Checks |
|---|---|---|---|---|
| **1** | Visible Status & Timely Feedback | Nielsen `H1` + Shneiderman `#3, #4` + Preece + Abandonment #3 | Area 1 (Cat. 1) + Group B latency (`1.17–1.24`) | Titles/headers, active/selected states, spinners/progress, explicit closure/receipt, `aria-live`, cancelable long ops. |
| **2** | Human Language, Natural Order & Clarity | Nielsen `H2` + Redish + Krug `3rd Law` + Abandonment #2 | Area 2 (Cat. 2) | Zero backend/DB jargon, specific action verbs, meaningful links (no *"Click here"*), concise microcopy, natural field order, local number/currency format. |
| **3** | User Control, Reversibility & Emergency Exits | Nielsen `H3` + Shneiderman `#6, #7` + Quesenbery *Error-tolerant* | Area 3 (Cat. 3) | Confirmations on destructive ops, *Undo* / *Cancel* (`AbortController`), *Back* preserving state, complete modal exit (`Esc`/backdrop), internal locus of control. |
| **4** | Consistency, Conventions & Clear Clickables | Nielsen `H4` + Jakob's Law + Krug + Preece + ISO 9126 | Area 4 (Cat. 4) | Uniform design tokens/slots, native interactive elements (`<button>`, `<a>`), `:hover`/`:focus-visible`/`:disabled`, zero false affordance, coherent terminology. |
| **5** | Error Prevention & Resilient Forms | Nielsen `H5` (*Slips*/*Mistakes*) + Shneiderman `#5` + Abandonment #4 | Area 6 (Cat. 6) | `type`/`min`/`max`, non-blocking masks/format hints, physical/visual separation of destructive CTAs, `trim()`/case-blind normalization, anti-double-submit guards. |
| **6** | Human Error Diagnosis & Recovery | Nielsen `H9` + Shneiderman `#5` + Abandonment #4 | Area 5 (Cat. 5) | Three-part error anatomy (not color-only + human cause + action), non-blaming tone, preserved valid data, focus/scroll to error field, helpful 404/500 routes. |
| **7** | Recognition, Minimalism & Visual Hierarchy | Nielsen `H6, H8` + Krug + Shneiderman `#8` | Areas 7, 9 & part of 11 (Cat. 7, 9, 12) | High signal-to-noise, WCAG contrast (`4.5:1`/`3:1`), redundant cues alongside color, icon labels, conditional fields, visible cross-step memory context. |
| **8** | Efficiency, Operational Accessibility & Contextual Help | Nielsen `H7, H10` + ISO 9241-11 + Quesenbery | Areas 8, 10 & part of 11 (Cat. 8, 10, 11) + Group B docs (`10.10–10.18`) | Full keyboard operability (`Tab`/arrows/shortcuts), responsive `375px+` without horizontal scroll bugs, draft saving, in-context help without losing form state, no gratuitous auth walls. |

---

## 3. Severity Rules & Web Abandonment Escalation

* **Critical (`Crítico`):** Blocks critical task completion, causes unrecoverable data loss/destructive execution without guard, creates keyboard/modal traps, exposes raw crashes/`5xx`/stack traces with dead ends, enforces gratuitous pre-exploration login walls, or hits one of the **4 Web Abandonment Causes** on the primary flow.
* **High (`Alto`):** Serious friction, confusing IA/labels causing likely wrong choices, missing feedback during async waits, validation that wipes entered inputs, poor mobile layout overflow breaking primary actions, or unclear clickable affordances.
* **Medium (`Medio`):** Localized inconsistencies (mixed verbs/terminology, missing helper hints, suboptimal alignment, minor redundant words, ungrouped controls) that slow users down without blocking task completion.

---

## 4. Verifiable Technical Acceptance Criterion Standard

Every reported finding must close with a binary, measurable QA / E2E assertion—never vague aesthetic advice:
* **Weak (forbidden):** *"Make error messages friendlier and improve form UX."*
* **Verifiable (required):** *"On invalid email submit or HTTP 500 from `POST /api/signup`, the form must preserve all entered field values, keep submit re-enabled, move focus to the first invalid `<input>` (`aria-invalid="true"`), display an inline `role="alert"` message stating the fix without raw error codes, and avoid horizontal overflow at `375px` viewport width (`scrollWidth <= innerWidth`)."*
