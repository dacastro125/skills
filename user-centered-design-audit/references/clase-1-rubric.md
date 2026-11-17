# UCD / DCU Clase 1 Audit Rubric (Design & Code)

Closed-scope rubric covering strictly the UI design, interaction, and software engineering principles from Class 1. Only flag a principle when an observable code or runtime signal matches.

---

## A. Design & Interaction Principles

| # | Principle | Observable Code / UI Signals to Check | When `Not applicable` / `Not statically verifiable` |
|---|---|---|---|
| 1 | **Mental Models** | Navigation labels, icons, routes, or button verbs contradict actual behavior (e.g., "Back" discards unsaved form state without warning; destructive action styled/labeled like "Save" or "Continue"; inconsistent navigation behavior across screens). | Mark `Not statically verifiable` if terminology accuracy depends on domain-specific user jargon not present in code/README. |
| 2 | **Affordances, Signifiers, Natural Mapping & Immediate Feedback** *(Norman)* | Clickable handlers on non-semantic elements (`<div onClick>`, `<span>`) lacking `role="button"`, `tabIndex`, `cursor: pointer`, or focus styles; missing `:focus-visible` or `:disabled` visual cues; spatial control order mismatching flow direction; async actions (`fetch`, submit, heavy calculation) lacking pending state (`disabled`/spinner) or accessible live confirmation (`aria-live`, toast, inline message). | Mark `Not applicable` for async feedback if the app is purely synchronous/static with no user actions or async calls. |
| 3 | **Direct Manipulation & Reversible Control** *(Shneiderman)* | Irreversible state changes, deletions, or form submissions with no confirmation, undo, cancel, or direct inline editing; modal/wizard traps blocking the user from stepping back or inspecting prior input. | Mark `Not applicable` on read-only views with no mutable state or submissions. |
| 4 | **Physical/Touch Ergonomics & Error Prevention** *(Dreyfuss)* | Primary CTA placed adjacent to a destructive action (`Delete`/`Reset`) with identical styling; cramped or tiny interactive hit targets (< ~36–44px height/padding on touch-first layouts); unrestricted inputs (free text for dates/numbers/emails) or submit handlers that fire on accidental Enter/double-click without guard or debounce. | Mark `Not statically verifiable` for exact rendered hit-box overlap if styling uses complex dynamic layout and no browser check ran. |
| 5 | **Avoid Creeping Featurism** *(Norman, Ch. 6)* | Primary task viewport or main flow crowded with secondary widgets, promotional panels, redundant controls, or unrequested configuration toggles competing visually and structurally with the core user action. | Mark `Not applicable` on minimal single-purpose components with <= 2 controls. |

---

## B. Applied Code, Architecture & QA Principles

| # | Principle | Observable Code / Architecture Signals to Check | When `Not applicable` / `Not statically verifiable` |
|---|---|---|---|
| 6 | **Real User & Environment Adaptation** *(ISO 9241-210 P01)* | Fixed widths (`width: 900px` without `max-width`), missing responsive rules/breakpoints causing horizontal overflow on mobile; keyboard traps, missing `<label>`/`aria-label` on controls, missing `.skip-link` in multi-section pages, or missing `Escape`/backdrop close on modals; unguarded heavy iframes/media auto-loading without lazy/on-demand loading or offline/slow-network fallback. | Mark `Not statically verifiable` if responsive overflow depends on dynamic content sizes not inspectable without rendering. |
| 7 | **Complete Experience Beyond Happy Path** *(ISO 9241-210 P05)* | Missing empty states (`items.length === 0` renders blank area); swallowed errors (`catch (e) {}` with no UI recovery); vague or missing loading/timeout/retry states; multi-step or long forms lacking local draft persistence (`localStorage`/state preservation) or post-action confirmation. | Mark `Not applicable` for draft persistence on single-field search/filter or static reading views. |
| 8 | **Measurable Usability & Verifiable Criteria** *(ISO 9241-11 + Diap. 31)* | Unnecessary authentication/registration walls blocking read-only exploration before committing; excessive step/screen hops or redundant re-entry in the critical flow; lack of measurable flow guards. **Requirement:** every reported finding must translate into a binary QA/E2E acceptance criterion. | Always assessable when an interactive user flow exists (`Not applicable` only on pure static non-interactive fragments). |
| 9 | **Decoupled Iteration & User Goals over DB/API Convenience** *(ISO 9241-210 P04 + Closing Principle)* | Hard-coded rigid multi-screen chains or UI directly mirroring internal database/API artifacts: exposing raw UUIDs/foreign keys, snake_case DB field names, internal enum codes, or raw HTTP/stack-trace error strings in user-facing UI text. | Mark `Not applicable` for internal developer-only tools where raw IDs/payloads are the explicit domain task. |

---

## Verifiable Technical Acceptance Criterion Standard (Diap. 31)

Never write vague aesthetic criteria like *"Make the form cleaner"* or *"Improve error UX"*. Every criterion must be binary and testable in QA or automated E2E tests:

- **Weak:** *"The error message should be clearer and friendlier."*
- **Verifiable:** *"When the appointment POST request fails (HTTP 500 or offline), the UI must retain all entered form fields, display an inline alert inside an `aria-live="polite"` container with a retry button, and keep submit re-enabled."*
- **Verifiable:** *"Users must be able to browse available specialties before creating an account, completing selection in at most 3 screens at `375px` viewport width with zero horizontal overflow (`scrollWidth <= innerWidth`)."*
