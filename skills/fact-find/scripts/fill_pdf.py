"""Fill a copy of a fillable PDF fact-find from a JSON values file.

Usage:
    python fill_pdf.py --template <blank-form.pdf> --values <values.json> --out <filled.pdf>

values.json is a flat object of {pdf_field_name: value}. Strings fill text
and choice fields; true/false tick or clear checkboxes (true uses the box's
own "on" state); a string matching one of a radio group's states selects it.

Values travel file -> script, never through the command line, so nothing a
client document said can become shell syntax. The template is never modified;
the output must be a new path (the script refuses to overwrite anything).
No network access, no execution of anything in either file.

Prints a JSON report: filled, not_found (names in values.json the form
doesn't have), skipped (values it could not apply, with the reason).
Exit codes: 0 written; 1 error; 3 pypdf missing.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, BooleanObject, IndirectObject, StreamObject
except ImportError:
    print(json.dumps({"error": "pypdf is not installed. Run: python -m pip install pypdf"}))
    sys.exit(3)


def resolve(obj):
    return obj.get_object() if isinstance(obj, IndirectObject) else obj


def full_name(annot):
    parts, node = [], annot
    while node is not None:
        if "/T" in node:
            parts.append(str(node["/T"]))
        node = resolve(node["/Parent"]) if "/Parent" in node else None
    return ".".join(reversed(parts))


def on_states(annot):
    ap = resolve(annot.get("/AP")) if "/AP" in annot else None
    if ap is None or "/N" not in ap:
        return []
    normal = resolve(ap["/N"])
    if isinstance(normal, StreamObject):  # text-style appearance, no named states
        return []
    return [str(k) for k in normal.keys() if str(k) != "/Off"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    template, out = Path(args.template).resolve(), Path(args.out).resolve()
    if out == template:
        raise SystemExit(json.dumps({"error": "--out must differ from --template; the blank form is never modified"}))
    if out.exists():
        raise SystemExit(json.dumps({"error": f"{out.name} already exists; choose a new file name"}))

    values = json.loads(Path(args.values).read_text(encoding="utf-8"))
    if not isinstance(values, dict):
        raise SystemExit(json.dumps({"error": "values file must be a JSON object of {field_name: value}"}))

    reader = PdfReader(str(template))
    known = set((reader.get_fields() or {}).keys())
    if not known:
        raise SystemExit(json.dumps({"error": "the template has no fillable fields (flat PDF)"}))

    writer = PdfWriter()
    writer.append(reader)

    text_values, filled, skipped = {}, [], []
    not_found = sorted(k for k in values if k not in known)

    for page in writer.pages:
        page_text = {}
        for annot in page.get("/Annots") or []:
            annot = resolve(annot)
            if annot.get("/Subtype") != "/Widget":
                continue
            name = full_name(annot)
            if name not in values:
                continue
            value = values[name]
            parent = resolve(annot["/Parent"]) if "/Parent" in annot else annot
            ftype = str(annot.get("/FT") or parent.get("/FT") or "")
            if ftype == "/Btn":
                states = on_states(annot)
                if isinstance(value, bool):
                    target = (states[0] if states else None) if value else "/Off"
                elif isinstance(value, str) and ("/" + value.lstrip("/")) in states:
                    target = "/" + value.lstrip("/")
                elif isinstance(value, str):
                    target = "/Off"  # radio option belonging to a sibling widget
                else:
                    skipped.append({"field": name, "reason": "checkbox/radio needs true/false or a state name"})
                    continue
                if target is None:
                    skipped.append({"field": name, "reason": "checkbox has no 'on' appearance state"})
                    continue
                annot[NameObject("/AS")] = NameObject(target)
                if target != "/Off":
                    parent[NameObject("/V")] = NameObject(target)
                    filled.append(name)
                elif isinstance(value, bool):
                    parent[NameObject("/V")] = NameObject("/Off")
                    filled.append(name)
            else:
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                if value is None:
                    continue
                page_text[name] = str(value)
        if page_text:
            writer.update_page_form_field_values(page, page_text, auto_regenerate=False)
            text_values.update(page_text)
            filled.extend(page_text)

    missing_radio = [k for k, v in values.items() if k in known and isinstance(v, str) and k not in filled and k not in text_values]
    for name in missing_radio:
        skipped.append({"field": name, "reason": "value did not match any state of this button field"})

    root = writer._root_object
    if "/AcroForm" in root:
        resolve(root["/AcroForm"])[NameObject("/NeedAppearances")] = BooleanObject(True)

    with open(out, "wb") as handle:
        writer.write(handle)

    print(json.dumps({"written": str(out), "filled": sorted(set(filled)),
                      "not_found": not_found, "skipped": skipped}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        sys.exit(1)
