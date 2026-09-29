# firm-config

This folder is empty in the public repository. It is for **firms that keep their own fork** of this plugin and want every adviser who installs that fork to get the firm's fact-find automatically.

To use it, run `/fact-find-setup` on your firm's fact-find and choose the "firm's own fork" option at the save step. Then commit these files here:

| File | What it is |
|---|---|
| `fact-find-schema.json` | The schema `/fact-find` fills. Must pass `skills/fact-find-setup/scripts/validate_schema.py`. |
| `fact-find-schema.md` | The readable summary, for whoever signs the schema off. |
| `fact-find-template.pdf` | For a fillable-PDF fact-find only: the untouched blank form. `/fact-find` fills a copy and never this file. |

`/fact-find` looks here fourth: after a path the adviser names, a pointer in the adviser's own settings, and a schema in the adviser's working folder. So an individual adviser can still override the firm's schema.

**Never commit client data here.** A schema describes the form, not anyone's answers, and the validator rejects a schema that carries answer fields. Completed fact-finds belong in the firm's records, not in a repository.

Before advisers rely on the schema, have your compliance owner (or your network, for an appointed representative) review `fact-find-schema.md`. They should then set `"status": "approved"` and `"approved_by"` in the JSON themselves.
