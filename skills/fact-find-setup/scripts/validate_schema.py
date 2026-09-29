"""Validate a fact-find schema and (optionally) render its markdown companion.

Usage:
    python validate_schema.py <fact-find-schema.json> [--markdown <out.md>] [--pdf <form.pdf>]

With --pdf, also confirms every pdf_field the schema names exists in the form
(a missing one is an error) and lists the form's fields the schema never maps.

Checks the file against references/schema-format.md
(pensions-adviser/fact-find-schema@1) and references/canonical-fields.md,
both resolved relative to this script. Prints a JSON report on stdout:
{"valid": bool, "errors": [...], "warnings": [...], "summary": {...}}.

Read-only apart from the optional --markdown output file. Never executes
anything in the schema; labels and help text are treated as plain strings.

Exit codes: 0 valid (warnings allowed); 1 invalid or unreadable.
"""

import argparse
import json
import re
import sys
from pathlib import Path

FORMAT = "pensions-adviser/fact-find-schema@1"
TYPES = {"text", "long_text", "date", "currency", "percentage", "number", "boolean", "enum", "multi_enum"}
REPEATS = {"once", "per_client", "per_item"}
SOURCE_HINTS = {"document", "conversation", "crm", "adviser", "client_only"}
SOURCE_TYPES = {"fillable-pdf", "flat-pdf", "docx", "xlsx", "csv-export", "json", "default"}
ID_RE = re.compile(r"^[a-z0-9_]+$")
NEVER_FILLED_PREFIXES = ("declaration.",)
NEVER_FILLED = {"adviser.signature", "adviser.date_signed", "atr.result", "capacity_for_loss.result"}
ANSWER_KEYS = {"value", "answer", "values", "answers", "data"}

HERE = Path(__file__).resolve().parent
CANONICAL_FILE = HERE.parent / "references" / "canonical-fields.md"


def load_canonical():
    keys, special = set(), set()
    for line in CANONICAL_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*`([a-z_]+\.[a-z0-9_]+)`\s*\|(.*)\|\s*$", line)
        if m:
            keys.add(m.group(1))
            if "(SC)" in m.group(2):
                special.add(m.group(1))
    return keys, special


def never_filled(key):
    return key in NEVER_FILLED or key.startswith(NEVER_FILLED_PREFIXES)


def validate(schema, canonical, special):
    errors, warnings = [], []
    if not isinstance(schema, dict):
        return ["top level is not a JSON object"], warnings

    if schema.get("schema_format") != FORMAT:
        errors.append(f"schema_format must be exactly '{FORMAT}'")
    for key in ("firm", "name", "version"):
        if not str(schema.get(key) or "").strip():
            errors.append(f"missing top-level '{key}'")
    if schema.get("status") not in ("draft", "approved"):
        errors.append("status must be 'draft' or 'approved'")
    if schema.get("status") == "approved" and not str(schema.get("approved_by") or "").strip():
        errors.append("status is 'approved' but approved_by is empty")
    source = schema.get("source") or {}
    if source.get("type") not in SOURCE_TYPES:
        errors.append(f"source.type must be one of {sorted(SOURCE_TYPES)}")
    clients = schema.get("clients")
    if clients not in (["client1"], ["client1", "client2"]):
        errors.append("clients must be [\"client1\"] or [\"client1\", \"client2\"]")
        clients = ["client1"]
    is_fillable = source.get("type") == "fillable-pdf"

    sections = schema.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be a non-empty list")
        return errors, warnings

    section_ids = set()
    pdf_names = {}
    for s_index, section in enumerate(sections):
        where = f"sections[{s_index}]"
        sid = section.get("id", "")
        if not ID_RE.match(str(sid)):
            errors.append(f"{where}: id '{sid}' must match a-z0-9_")
        if sid in section_ids:
            errors.append(f"{where}: duplicate section id '{sid}'")
        section_ids.add(sid)
        where = f"section '{sid}'"
        if not str(section.get("title") or "").strip():
            errors.append(f"{where}: missing title")
        repeat = section.get("repeat")
        if repeat not in REPEATS:
            errors.append(f"{where}: repeat must be one of {sorted(REPEATS)}")
        if repeat == "per_item" and section.get("max_items") is not None:
            if not isinstance(section["max_items"], int) or section["max_items"] < 1:
                errors.append(f"{where}: max_items must be a positive integer")
        fields = section.get("fields")
        if not isinstance(fields, list) or not fields:
            errors.append(f"{where}: fields must be a non-empty list")
            continue

        field_ids = set()
        for f_index, field in enumerate(fields):
            fid = field.get("id", "")
            fwhere = f"{sid}.{fid or f'[{f_index}]'}"
            if ANSWER_KEYS & set(field):
                errors.append(f"{fwhere}: carries an answer key ({sorted(ANSWER_KEYS & set(field))}) — a schema holds no client data")
            if not ID_RE.match(str(fid)):
                errors.append(f"{fwhere}: id must match a-z0-9_")
            if fid in field_ids:
                errors.append(f"{fwhere}: duplicate field id in section")
            field_ids.add(fid)
            if not str(field.get("label") or "").strip():
                errors.append(f"{fwhere}: missing label")
            ftype = field.get("type")
            if ftype not in TYPES:
                errors.append(f"{fwhere}: type '{ftype}' not one of {sorted(TYPES)}")
            if ftype in ("enum", "multi_enum"):
                opts = field.get("options")
                if not isinstance(opts, list) or not opts:
                    errors.append(f"{fwhere}: {ftype} needs a non-empty options list")
            canon = field.get("canonical")
            if not canon:
                errors.append(f"{fwhere}: missing canonical (use 'custom' if nothing fits)")
            elif canon != "custom" and canon not in canonical:
                errors.append(f"{fwhere}: canonical '{canon}' is not in canonical-fields.md")
            if canon in special and field.get("special_category") is not True:
                warnings.append(f"{fwhere}: maps to special category key '{canon}' but special_category is not true")
            if field.get("source_hint") not in SOURCE_HINTS:
                errors.append(f"{fwhere}: source_hint must be one of {sorted(SOURCE_HINTS)}")
            if canon and never_filled(canon) and field.get("source_hint") != "client_only" and not canon.startswith(("atr.", "capacity_for_loss.", "adviser.")):
                warnings.append(f"{fwhere}: '{canon}' is never filled — source_hint is usually 'client_only'")
            if field.get("required") not in (True, False):
                errors.append(f"{fwhere}: required must be true or false")

            pdf_field = field.get("pdf_field")
            if is_fillable:
                if pdf_field is None:
                    warnings.append(f"{fwhere}: fillable-pdf schema but no pdf_field — this field will only appear in the markdown output")
                elif repeat == "per_client":
                    if not isinstance(pdf_field, dict) or set(pdf_field) - set(clients):
                        errors.append(f"{fwhere}: per_client pdf_field must be an object keyed by {clients}")
                    else:
                        for name in pdf_field.values():
                            pdf_names.setdefault(name, []).append(fwhere)
                elif repeat == "per_item":
                    if not isinstance(pdf_field, str) or "{n}" not in pdf_field:
                        errors.append(f"{fwhere}: per_item pdf_field must be a string containing {{n}}")
                    else:
                        pdf_names.setdefault(pdf_field, []).append(fwhere)
                else:
                    if not isinstance(pdf_field, str):
                        errors.append(f"{fwhere}: pdf_field must be a string for a 'once' section")
                    else:
                        pdf_names.setdefault(pdf_field, []).append(fwhere)
            elif pdf_field is not None:
                warnings.append(f"{fwhere}: pdf_field set but source.type is not fillable-pdf — it will be ignored")

    for name, users in pdf_names.items():
        if len(users) > 1:
            errors.append(f"pdf_field '{name}' is used by more than one field: {users}")
    return errors, warnings


def summary(schema):
    sections = schema.get("sections") or []
    fields = [f for s in sections for f in (s.get("fields") or [])]
    return {
        "firm": schema.get("firm"),
        "name": schema.get("name"),
        "version": schema.get("version"),
        "status": schema.get("status"),
        "source_type": (schema.get("source") or {}).get("type"),
        "sections": len(sections),
        "fields": len(fields),
        "required": sum(1 for f in fields if f.get("required") is True),
        "custom": sum(1 for f in fields if f.get("canonical") == "custom"),
        "special_category": sum(1 for f in fields if f.get("special_category") is True),
        "never_filled": sum(1 for f in fields if f.get("canonical") and never_filled(f["canonical"])),
    }


def expected_pdf_names(schema):
    """Every concrete PDF field name the schema can write to."""
    names = []
    clients = schema.get("clients") or ["client1"]
    for section in schema.get("sections") or []:
        for field in section.get("fields") or []:
            pdf_field = field.get("pdf_field")
            if pdf_field is None:
                continue
            if section.get("repeat") == "per_client" and isinstance(pdf_field, dict):
                names += [pdf_field[c] for c in clients if c in pdf_field]
            elif section.get("repeat") == "per_item" and isinstance(pdf_field, str):
                for n in range(1, (section.get("max_items") or 1) + 1):
                    names.append(pdf_field.replace("{n}", str(n)))
            elif isinstance(pdf_field, str):
                names.append(pdf_field)
    return names


def pdf_coverage(schema, pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return {"error": "pypdf is not installed. Run: python -m pip install pypdf"}
    try:
        form_names = set((PdfReader(pdf_path).get_fields() or {}).keys())
    except Exception as exc:
        return {"error": f"cannot read PDF: {type(exc).__name__}: {exc}"}
    if not form_names:
        return {"error": "the PDF has no fillable fields — use source.type 'flat-pdf'"}
    expected = expected_pdf_names(schema)
    for section in schema.get("sections") or []:
        if section.get("repeat") == "per_item" and not section.get("max_items") and any(
                isinstance(f.get("pdf_field"), str) for f in section.get("fields") or []):
            return {"error": f"section '{section.get('id')}' is per_item with pdf_fields but no max_items"}
    return {
        "form_fields": len(form_names),
        "mapped": len(set(expected) & form_names),
        "missing_from_pdf": sorted(set(expected) - form_names),
        "unmapped_form_fields": sorted(form_names - set(expected)),
    }


def cell(value):
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def markdown(schema):
    s = summary(schema)
    lines = [
        f"# {cell(schema.get('name'))} — fact-find schema",
        "",
        f"**Firm:** {cell(schema.get('firm'))} · **Version:** {cell(schema.get('version'))} · "
        f"**Status:** {cell(schema.get('status'))}"
        + (f" (approved by {cell(schema.get('approved_by'))})" if schema.get("status") == "approved" else " — not yet signed off by the firm"),
        "",
        f"Built from: {cell((schema.get('source') or {}).get('type'))} · {cell((schema.get('source') or {}).get('file'))}. "
        f"{s['sections']} sections, {s['fields']} fields ({s['required']} required, {s['custom']} custom, "
        f"{s['special_category']} special category, {s['never_filled']} never filled by /fact-find).",
        "",
        "Generated from `fact-find-schema.json` — edit the JSON, not this file. This file describes the form's shape and holds no client data.",
        "",
    ]
    for section in schema.get("sections") or []:
        extra = {"per_client": "one per client", "per_item": "repeats per item", "once": "once per case"}.get(section.get("repeat"), "")
        if section.get("max_items"):
            extra += f", up to {section['max_items']} on the form"
        lines += [f"## {cell(section.get('title'))}", "", f"*{extra}*", "",
                  "| Field | Type | Maps to | Required | Notes |", "|---|---|---|---|---|"]
        for f in section.get("fields") or []:
            notes = []
            if f.get("special_category"):
                notes.append("special category")
            if f.get("canonical") and never_filled(f["canonical"]):
                notes.append("never filled")
            if f.get("options"):
                notes.append("options: " + " / ".join(map(str, f["options"])))
            lines.append(f"| {cell(f.get('label'))} | {cell(f.get('type'))} | `{cell(f.get('canonical'))}` | "
                         f"{'yes' if f.get('required') else ''} | {cell('; '.join(notes))} |")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("schema")
    parser.add_argument("--markdown")
    parser.add_argument("--pdf")
    try:
        args = parser.parse_args()
    except SystemExit:
        print(json.dumps({"valid": False, "errors": ["usage: python validate_schema.py <schema.json> [--markdown <out.md>] [--pdf <form.pdf>]"]}))
        sys.exit(1)
    try:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"valid": False, "errors": [f"cannot read schema: {type(exc).__name__}: {exc}"]}))
        sys.exit(1)
    canonical, special = load_canonical()
    errors, warnings = validate(schema, canonical, special)
    report = {"valid": not errors, "errors": errors, "warnings": warnings,
              "summary": summary(schema) if isinstance(schema, dict) else {}}
    if args.pdf and not errors:
        coverage = pdf_coverage(schema, args.pdf)
        report["pdf_coverage"] = coverage
        if coverage.get("error"):
            errors.append(coverage["error"])
        for name in coverage.get("missing_from_pdf", []):
            errors.append(f"pdf_field '{name}' does not exist in {Path(args.pdf).name}")
        report["valid"] = not errors
    if not errors and args.markdown:
        Path(args.markdown).write_text(markdown(schema), encoding="utf-8")
        report["markdown"] = args.markdown
    print(json.dumps(report, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
