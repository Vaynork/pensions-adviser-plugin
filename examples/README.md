# Examples

Everything here is **fictional**: it is for trying the fact-find tooling without using a real firm's form or a real client.

| File | What it is |
|---|---|
| `sample-firm-fact-find.pdf` | A short, fillable, two-client "Retirement Fact-Find" for the fictional Harbour Lane Financial Planning Ltd. |
| `sample-firm-fact-find.schema.json` | The schema `/fact-find-setup` would build from it. It maps all 36 form fields and shows each schema pattern: per-client fields, a repeating pension table, one custom field, one special category field, and never-filled declaration, signature and risk-result boxes. |
| `make_sample_form.py` | Regenerates the PDF (needs `reportlab`). |

## Try it

In Claude, with this plugin installed:

1. Run `/fact-find-setup` and upload `sample-firm-fact-find.pdf`. Compare the schema it builds with `sample-firm-fact-find.schema.json`.
2. Run `/fact-find` for a made-up client and give it a few made-up documents or a short made-up meeting note. It fills a copy of the sample form and writes the source trail and the gaps list.

Or check the scripts directly from the repo root:

```bash
python skills/fact-find-setup/scripts/list_pdf_fields.py examples/sample-firm-fact-find.pdf
```

```bash
python skills/fact-find-setup/scripts/validate_schema.py examples/sample-firm-fact-find.schema.json --pdf examples/sample-firm-fact-find.pdf
```
