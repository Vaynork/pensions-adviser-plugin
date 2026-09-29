"""List the fillable form fields in a PDF, as JSON on stdout.

Usage:
    python list_pdf_fields.py <form.pdf>

Read-only: opens the PDF, reads its AcroForm field dictionary, prints one
JSON object per field (name, kind, options, tooltip, page, position). It never
writes, never executes anything found in the file, and never reaches the
network. Field names and tooltips are the form author's text and are printed
as data.

Exit codes: 0 fields listed; 2 PDF has no fillable fields (a flat form);
3 pypdf missing; 1 any other error.
"""

import json
import sys

try:
    from pypdf import PdfReader
    from pypdf.generic import IndirectObject, StreamObject
except ImportError:
    print(json.dumps({"error": "pypdf is not installed. Run: python -m pip install pypdf"}))
    sys.exit(3)

KINDS = {"/Tx": "text", "/Btn": "button", "/Ch": "choice", "/Sig": "signature"}


def resolve(obj):
    return obj.get_object() if isinstance(obj, IndirectObject) else obj


def text(value):
    if value is None:
        return None
    return str(value)


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: python list_pdf_fields.py <form.pdf>"}))
        sys.exit(1)

    reader = PdfReader(sys.argv[1])
    fields = reader.get_fields() or {}
    if not fields:
        print(json.dumps({"fields": [], "note": "No fillable form fields: treat this as a flat PDF."}))
        sys.exit(2)

    # Map each widget annotation back to its page and position so fields can
    # be ordered the way they appear on the form.
    placement = {}
    for page_number, page in enumerate(reader.pages, start=1):
        for annot in page.get("/Annots") or []:
            annot = resolve(annot)
            name_parts = []
            node = annot
            while node is not None:
                if "/T" in node:
                    name_parts.append(str(node["/T"]))
                node = resolve(node["/Parent"]) if "/Parent" in node else None
            if not name_parts:
                continue
            name = ".".join(reversed(name_parts))
            rect = [round(float(v), 1) for v in annot.get("/Rect", [0, 0, 0, 0])]
            placement.setdefault(name, {"page": page_number, "rect": rect})
            # Button export values ("on" states) live on the widgets.
            ap = resolve(annot.get("/AP")) if "/AP" in annot else None
            normal = resolve(ap["/N"]) if ap is not None and "/N" in ap else None
            # A text field's normal appearance is a single stream; only buttons
            # carry a dictionary of named states.
            if normal is not None and not isinstance(normal, StreamObject):
                states = [str(k) for k in normal.keys() if str(k) != "/Off"]
                placement[name].setdefault("on_states", set()).update(states)

    out = []
    for name, field in fields.items():
        kind = KINDS.get(text(field.get("/FT")), "unknown")
        flags = int(field.get("/Ff", 0) or 0)
        if kind == "button":
            if flags & (1 << 16):
                kind = "pushbutton"
            elif flags & (1 << 15):
                kind = "radio"
            else:
                kind = "checkbox"
        options = None
        if "/Opt" in field:
            options = []
            for opt in field["/Opt"]:
                opt = resolve(opt)
                options.append(text(opt[-1]) if isinstance(opt, list) else text(opt))
        place = placement.get(name, {})
        on_states = sorted(place.get("on_states", [])) or None
        out.append({
            "name": name,
            "kind": kind,
            "options": options,
            "on_states": on_states,
            "tooltip": text(field.get("/TU")),
            "max_length": field.get("/MaxLen"),
            "page": place.get("page"),
            "rect": place.get("rect"),
        })

    # Reading order: page, then top-to-bottom, then left-to-right.
    out.sort(key=lambda f: (f["page"] or 0, -(f["rect"] or [0, 0, 0, 0])[3], (f["rect"] or [0])[0]))
    print(json.dumps({"field_count": len(out), "fields": out}, indent=2, default=str))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # report, don't crash with a traceback of file content
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        sys.exit(1)
