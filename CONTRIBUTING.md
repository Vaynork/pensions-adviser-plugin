# Contributing to Pensions Adviser (UK)

Everything in this repo is Markdown and JSON. Issues and pull requests are welcome, especially from advisers, paraplanners and compliance professionals who spot an outdated rule, a missing pension feature or a UK system that now has an MCP connector.

## What goes where

- **Skills** live in `skills/<skill-name>/SKILL.md` with the same frontmatter the existing skills use (`name`, `description`). Keep the description focused on trigger phrases advisers actually say. Supporting material goes in `skills/<skill-name>/templates/` or `skills/<skill-name>/references/`.
- **Agents** live in `agents/<name>.md`. Each one has a single, narrow job and states which systems it reads from.
- **Connectors** are declared once in `.mcp.json` and described in [README.md](README.md). Add a connector only when a skill actually reads from it, and only with an endpoint the vendor publishes.
- **Maintainer context** (regulatory frame, tax snapshot, UK tech stack) lives in [`docs/uk-pensions-context.md`](docs/uk-pensions-context.md). Update it first when rules change, then the skill references that depend on it.

## Design rules

- **No client data in the repo.** Demo material must be clearly fictional. Never paste real statements, plan numbers, names or National Insurance numbers, even redacted.
- **Every write to an external system pauses for adviser approval.** A skill may draft a file note, task or client message, but it must stop and ask before anything leaves the session.
- **No recommendations and no suitability judgements.** Skills describe options and surface facts; the adviser decides. This matters most for anything involving safeguarded benefits, where the regulatory starting assumption is that a DB transfer is unsuitable.
- **Client-facing output routes through `/compliance`.** If a skill produces something a client might see, say so in the skill and point at the compliance check.
- **Cite, don't compute, constants.** Tax allowances and regulatory figures come from the connected system, the firm, the adviser or a clearly dated snapshot marked "verify before use".
- **Degrade gracefully.** When a connector isn't available, fall back to paste or upload rather than failing.
- **UK English**: adviser, organise, judgement, £, and 6 April to 5 April tax years.

## Checks

Before pushing, confirm that `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and `.mcp.json` are valid JSON, that any relative paths referenced from a `SKILL.md` exist, and that every `pensions-adviser:<agent>` reference names an agent in `agents/`. The `check-mcp-urls` workflow probes every connector URL on pull requests.

## Upstream

This fork tracks [anthropics/claude-for-financial-advisors](https://github.com/anthropics/claude-for-financial-advisors) as `upstream`. Improvements to the regime-neutral machinery (connector discovery, subagent rules) are worth pulling across. The upstream repo isn't accepting contributions, so don't open pull requests there from this fork.
