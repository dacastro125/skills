#!/usr/bin/env python3
"""Render and validate complete 225+22 Pierotti usability audit checklists.

Single source of truth: reads canonical Group A (225) and Group B (22) criteria
from ../references/pierotti-225-checklist.md so agents can supply concise
JSON evaluations + feature-class bulk rules and deterministically generate a
zero-omission, zero-miscount audit checklist markdown file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REF_PATH = SKILL_ROOT / "references" / "pierotti-225-checklist.md"

STATUS_ES = [
    "Cumple",
    "Parcial",
    "No cumple",
    "No aplica",
    "No verificable estáticamente",
]
STATUS_EN = [
    "Pass",
    "Partial",
    "Fail",
    "Not applicable",
    "Not statically verifiable",
]
STATUS_CANON_MAP = {
    "cumple": 0, "pass": 0,
    "parcial": 1, "partial": 1,
    "no cumple": 2, "fail": 2,
    "no aplica": 3, "not applicable": 3, "n/a": 3,
    "no verificable estáticamente": 4, "no verificable estaticamente": 4,
    "not statically verifiable": 4,
}


def load_reference():
    """Parse areas (225 Group A) and Group B (22) from pierotti-225-checklist.md."""
    lines = REF_PATH.read_text(encoding="utf-8").splitlines()
    areas = []
    group_b = []
    all_items = {}
    ordered_a = []
    ordered_b = []

    cur_area = None
    in_gb = False

    row_re = re.compile(r"^\|\s*\*\*(\d+\.\d+)\*\*\s*\|\s*\*\*(.*?)\*\*<br>_(.*?)_\s*\|")
    for line in lines:
        if line.startswith("## Área "):
            cur_area = {"title": line[3:].strip(), "ids": []}
            areas.append(cur_area)
            in_gb = False
        elif line.startswith("## Anexo Grupo B"):
            cur_area = None
            in_gb = True
        elif line.startswith("## Trazabilidad Grupo C"):
            cur_area = None
            in_gb = False
        else:
            m = row_re.match(line)
            if m:
                pid, en_txt, es_txt = m.group(1), m.group(2).strip(), m.group(3).strip()
                all_items[pid] = {"id": pid, "en": en_txt, "es": es_txt}
                if cur_area is not None:
                    cur_area["ids"].append(pid)
                    ordered_a.append(pid)
                elif in_gb:
                    group_b.append(pid)
                    ordered_b.append(pid)

    assert len(ordered_a) == 225, f"Reference broken: expected 225 Group A, got {len(ordered_a)}"
    assert len(ordered_b) == 22, f"Reference broken: expected 22 Group B, got {len(ordered_b)}"
    return areas, group_b, all_items, ordered_a + ordered_b


def _num_key(pid: str) -> tuple[int, int]:
    maj, min_ = pid.split(".")
    return int(maj), int(min_)


def expand_id_spec(spec: str, ordered_all: list[str]) -> list[str]:
    """Expand numeric ranges like '1.25-1.29' or single IDs against canonical 247 items."""
    expected_set = set(ordered_all)
    spec = spec.strip()
    m = re.match(r"^(\d+\.\d+)\s*[–—\-]\s*(\d+\.\d+)$", spec)
    if m:
        s, e = m.group(1), m.group(2)
        ks, ke = _num_key(s), _num_key(e)
        if ks[0] != ke[0]:
            raise ValueError(f"Cross-category range not allowed: {spec}")
        if ks > ke:
            raise ValueError(f"Inverted numeric range in spec: {spec}")
        matched = [pid for pid in ordered_all if ks <= _num_key(pid) <= ke]
        if not matched:
            raise ValueError(f"No canonical active IDs in range: {spec}")
        return matched
    if spec not in expected_set:
        raise ValueError(f"Unknown Pierotti ID: {spec}")
    return [spec]


def normalize_status(raw: str, lang: str) -> tuple[int, str]:
    key = raw.strip().lower()
    if key not in STATUS_CANON_MAP:
        raise ValueError(f"Invalid status '{raw}'. Allowed: {STATUS_ES + STATUS_EN}")
    idx = STATUS_CANON_MAP[key]
    return idx, (STATUS_EN[idx] if lang == "en" else STATUS_ES[idx])


def esc(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def cmd_render(input_json: Path, output_md: Path) -> None:
    areas, group_b, all_items, ordered_all = load_reference()
    data = json.loads(input_json.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    lang = "en" if str(meta.get("lang", "es")).lower().startswith("en") else "es"

    resolved: dict[str, tuple[int, str, str]] = {}

    for rule in data.get("bulk_rules", []):
        st_idx, st_label = normalize_status(rule["status"], lang)
        ev = rule.get("evidence", "").strip()
        if not ev:
            raise ValueError(f"Bulk rule for {rule.get('ids')} requires non-empty 'evidence'")
        for raw_spec in rule.get("ids", []):
            for pid in expand_id_spec(raw_spec, ordered_all):
                resolved[pid] = (st_idx, st_label, ev)

    for pid, entry in data.get("items", {}).items():
        if pid not in all_items:
            raise ValueError(f"Unknown Pierotti ID in 'items': {pid}")
        st_idx, st_label = normalize_status(entry["status"], lang)
        ev = entry.get("evidence", "").strip()
        if not ev:
            raise ValueError(f"Item '{pid}' requires non-empty 'evidence'")
        resolved[pid] = (st_idx, st_label, ev)

    missing = [pid for pid in ordered_all if pid not in resolved]
    if missing:
        raise ValueError(f"Missing {len(missing)} Pierotti IDs (first 10): {missing[:10]}")

    def count_subset(pids: list[str]) -> list[int]:
        counts = [0, 0, 0, 0, 0]
        for p in pids:
            counts[resolved[p][0]] += 1
        return counts

    ordered_a = [pid for a in areas for pid in a["ids"]]
    cnt_a = count_subset(ordered_a)
    cnt_b = count_subset(group_b)
    cnt_tot = [cnt_a[i] + cnt_b[i] for i in range(5)]

    labels = STATUS_EN if lang == "en" else STATUS_ES
    lines: list[str] = []

    if lang == "en":
        lines.append("# Usability Heuristics & Pierotti 225 Audit Checklist")
        lines.append("")
        lines.append(f"- **Target:** `{meta.get('target', 'N/A')}`")
        if meta.get("dependencies"):
            lines.append(f"- **Connected dependencies:** `{meta['dependencies']}`")
        lines.append(f"- **Date:** `{meta.get('date', 'N/A')}`")
        lines.append(f"- **Audit Mode:** `{meta.get('mode', 'Static')}`")
        if meta.get("profile"):
            lines.append(f"- **Inferred Context:** {meta['profile']}")
        lines.extend([
            "",
            "## Summary Counts (`225` Group A + `22` Group B = `247` Items)",
            "",
            f"| Scope | {labels[0]} | {labels[1]} | {labels[2]} | {labels[3]} | {labels[4]} | Total |",
            "|---|---:|---:|---:|---:|---:|---:|",
            f"| **Group A (Active Pierotti Checklist)** | {cnt_a[0]} | {cnt_a[1]} | {cnt_a[2]} | {cnt_a[3]} | {cnt_a[4]} | **225** |",
            f"| **Group B (Conditional Appendix)** | {cnt_b[0]} | {cnt_b[1]} | {cnt_b[2]} | {cnt_b[3]} | {cnt_b[4]} | **22** |",
            f"| **Grand Total** | **{cnt_tot[0]}** | **{cnt_tot[1]}** | **{cnt_tot[2]}** | **{cnt_tot[3]}** | **{cnt_tot[4]}** | **247** |",
        ])
    else:
        lines.append("# Auditoría de Usabilidad y Checklist Pierotti (`225 + 22` ítems)")
        lines.append("")
        lines.append(f"- **Objetivo auditado:** `{meta.get('target', 'N/A')}`")
        if meta.get("dependencies"):
            lines.append(f"- **Dependencias conectadas:** `{meta['dependencies']}`")
        lines.append(f"- **Fecha:** `{meta.get('date', 'N/A')}`")
        lines.append(f"- **Modo de auditoría:** `{meta.get('mode', 'Estático')}`")
        if meta.get("profile"):
            lines.append(f"- **Contexto inferido:** {meta['profile']}")
        lines.extend([
            "",
            "## Resumen cuantitativo Pierotti (`225` Grupo A + `22` Grupo B = `247` ítems)",
            "",
            f"| Conjunto | {labels[0]} | {labels[1]} | {labels[2]} | {labels[3]} | {labels[4]} | Total |",
            "|---|---:|---:|---:|---:|---:|---:|",
            f"| **Grupo A (11 áreas activas)** | {cnt_a[0]} | {cnt_a[1]} | {cnt_a[2]} | {cnt_a[3]} | {cnt_a[4]} | **225** |",
            f"| **Grupo B (Anexo condicional)** | {cnt_b[0]} | {cnt_b[1]} | {cnt_b[2]} | {cnt_b[3]} | {cnt_b[4]} | **22** |",
            f"| **Total evaluado** | **{cnt_tot[0]}** | **{cnt_tot[1]}** | **{cnt_tot[2]}** | **{cnt_tot[3]}** | **{cnt_tot[4]}** | **247** |",
        ])

    if meta.get("pillars"):
        lines.extend([
            "",
            "## 8 Consolidated Pillars" if lang == "en" else "## Resumen: 8 Pilares Consolidados",
            "",
            "| # | Pillar | Status | Key Pierotti IDs | Observation |" if lang == "en" else "| # | Pilar | Estado | IDs Pierotti clave | Observación |",
            "|---:|---|---|---|---|",
        ])
        for row in meta["pillars"]:
            lines.append(f"| **{row['id']}** | {esc(row['name'])} | **{esc(row['status'])}** | {esc(row.get('pierotti', ''))} | {esc(row['note'])} |")

    if meta.get("nielsen"):
        lines.extend([
            "",
            "## Nielsen Heuristics (`H1–H10`)" if lang == "en" else "## Heurísticas de Jakob Nielsen (`H1–H10`)",
            "",
            "| # | Heuristic | Status | Key Pierotti IDs | Observation |" if lang == "en" else "| # | Heurística | Estado | IDs Pierotti clave | Observación |",
            "|---|---|---|---|---|",
        ])
        for row in meta["nielsen"]:
            lines.append(f"| **{row['id']}** | {esc(row['name'])} | **{esc(row['status'])}** | {esc(row.get('pierotti', ''))} | {esc(row['note'])} |")

    lines.extend(["", "---", ""])
    col_hdr = (
        "| ID | Criterion | Status | Evidence / Rationale |"
        if lang == "en"
        else "| ID | Criterio | Estado | Evidencia / Justificación |"
    )

    for a in areas:
        lines.extend([f"### {a['title']}", "", col_hdr, "|---|---|---|---|"])
        for pid in a["ids"]:
            _, st_label, ev = resolved[pid]
            crit = esc(all_items[pid]["en"] if lang == "en" else all_items[pid]["es"])
            lines.append(f"| **{pid}** | {crit} | **{st_label}** | {esc(ev)} |")
        lines.append("")

    lines.extend([
        "### Group B Conditional Appendix (`22` items)" if lang == "en" else "### Anexo Grupo B · Ítems condicionales (`22` ítems)",
        "",
        col_hdr,
        "|---|---|---|---|",
    ])
    for pid in group_b:
        _, st_label, ev = resolved[pid]
        crit = esc(all_items[pid]["en"] if lang == "en" else all_items[pid]["es"])
        lines.append(f"| **{pid}** | {crit} | **{st_label}** | {esc(ev)} |")
    lines.append("")

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Rendered {output_md} -> 225 Group A + 22 Group B = 247 items. Counts A={cnt_a}, B={cnt_b}")


def cmd_validate(md_path: Path) -> None:
    areas, group_b, _, ordered_all = load_reference()
    expected_set = set(ordered_all)
    text = md_path.read_text(encoding="utf-8")
    row_ids = [
        m.group(1)
        for m in re.finditer(r"^\|\s*\*{0,2}`?(\d+\.\d+)`?\*{0,2}\s*\|", text, re.MULTILINE)
        if m.group(1) in expected_set
    ]
    c = Counter(row_ids)
    missing = [pid for pid in ordered_all if c[pid] == 0]
    dups = [(pid, cnt) for pid, cnt in c.items() if cnt > 1]
    print(f"Validated {md_path.name}: total_rows={len(row_ids)}, unique={len(c)}/247, missing={len(missing)}, dups={len(dups)}")
    if missing or dups or len(c) != 247:
        if missing:
            print(f"  Missing IDs (first 10): {missing[:10]}")
        if dups:
            print(f"  Duplicate IDs (first 10): {dups[:10]}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Render or validate Pierotti 225+22 usability audit checklists.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_render = sub.add_parser("render", help="Render 225+22 checklist .md from compact JSON input")
    p_render.add_argument("--input", required=True, type=Path, help="Input JSON evaluations path")
    p_render.add_argument("--output", required=True, type=Path, help="Output markdown checklist path")

    p_val = sub.add_parser("validate", help="Validate that a generated checklist .md covers all 247 items 1:1")
    p_val.add_argument("checklist_md", type=Path, help="Checklist markdown file to validate")

    args = parser.parse_args()
    if args.cmd == "render":
        cmd_render(args.input, args.output)
    elif args.cmd == "validate":
        cmd_validate(args.checklist_md)


if __name__ == "__main__":
    main()
