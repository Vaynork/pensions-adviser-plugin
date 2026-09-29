# Pensions Adviser (UK)

**Claude workflows for UK pensions and retirement advisers and paraplanners.** Upload a client's statements and meeting notes and get back a pre-filled fact-find in your firm's own format. Prepare an annual review pack in minutes. Pre-check a client letter against FCA rules before it goes to compliance. Fact-find a pension transfer without missing a guarantee.

It is a plugin for Claude: a set of plain-language instructions (skills) that turn Claude into a careful assistant for pensions advice work. You stay the adviser. Claude gathers, organises and drafts; you check, decide and advise.

> **Unofficial community project.** This is an independent UK adaptation of Anthropic's [Claude for Financial Advisors](https://github.com/anthropics/claude-for-financial-advisors) reference plugin, which was built for US advisers. It is **not affiliated with, endorsed by or supported by Anthropic.** For use by professionals at FCA-authorised firms only; it does not give advice (see [Important information](#important-information)).

## What it looks like in practice

*A fictional example.*

> **Adviser:** `/fact-find` for Priya and Tom Hartley. *(uploads six pension statements, two P60s, a State Pension forecast and yesterday's meeting transcript)*
>
> **Claude:** reads every document in parallel, then writes out:
> - **the firm's own fact-find, pre-filled**: 94 of 130 fields, each with its source;
> - **a filled copy of the firm's PDF form**;
> - **a gaps list**: 11 questions for the client, 3 values to request from providers, and a note that one plan has a guaranteed annuity rate (with a pointer to `/pension-transfer-check`);
> - **one conflict to resolve**: the transcript says retirement at 63, but the workplace scheme has a selected retirement age of 65.
>
> Declarations, signatures and the attitude-to-risk result are left blank for the client and adviser. Nothing is written to your back office until you approve it.

## Who it's for

- **Advisers and paraplanners** at directly authorised firms and appointed representatives, doing pensions accumulation, consolidation and transfers, drawdown and retirement income, and death-benefit and tax planning.
- **Compliance and operations teams** who want consistent fact-finds, review files and pre-checked client communications.

It is **not** a robo-adviser or a replacement for your advice process, your risk-profiling tool, your cashflow model or your compliance sign-off. It works alongside them.

## What you need

- **Claude with plugins:** Claude Code, or the Claude desktop app with plugin support, on a plan your firm has approved for client data.
- **Optional connectors** for systems you already use: Microsoft 365 or Google Workspace, Salesforce, Zocks, document stores. Most UK back offices and platforms don't have connectors yet; every skill works from uploads and pasted exports instead (see [Connecting your systems](#connecting-your-systems)).
- **Optional: Python with `pypdf`** (`python -m pip install pypdf`), only if you want `/fact-find` to fill your firm's PDF form directly.
- **Your firm's approval** to use an AI assistant with client data, and a lawful basis for any health data you record.

## Get started

**1. Install the plugin.** In Claude Code, run:

```bash
claude plugin marketplace add Vaynork/pensions-adviser-plugin
```

```bash
claude plugin install pensions-adviser@pensions-adviser
```

Or, inside a Claude session: `/plugin marketplace add Vaynork/pensions-adviser-plugin`, then `/plugin install pensions-adviser@pensions-adviser`. If you use plugins in the Claude desktop app instead, add the same GitHub repository, `Vaynork/pensions-adviser-plugin`, as a plugin marketplace there and install **Pensions Adviser (UK)**.

**2. Run `/onboarding`.** A short guided setup. It asks about your role, whether your firm is directly authorised or an appointed representative, and your tech stack. It connects what can be connected, then walks you through a demo annual review for a fictional household, so no real client data is needed for your first run.

**3. Run `/fact-find-setup`.** Point it at your firm's fact-find (PDF, Word, Excel or a back-office import template), or at the shared setup your firm has already made. It takes a few minutes and you only do it once. See [Your firm's fact-find](#your-firms-fact-find).

**4. Try it on real work.** Good first runs:
- `/fact-find` for a new client, with their documents and your meeting notes.
- `/pre-meeting` for your next annual review.
- `/compliance` on a draft client email, review letter or social post.

Want to try it without any client data? The [`examples/`](examples/) folder has a fictional firm's fillable fact-find to practise on.

## What you can do

Each skill is a slash command, and you can also just ask in plain English ("prep me for the Hartleys' review on Thursday").

### Set up once

| Skill | What it does |
| :---- | :---- |
| `/onboarding` | First-run tour and setup: firm type, tech stack and connectors, then a demo on a fictional household. |
| `/fact-find-setup` | Loads your firm's own fact-find so `/fact-find` fills *your* form, in your order and wording. Run once per firm (by the form's owner) and once per adviser (to point at the shared setup). |

### New clients and transfers

| Skill | What it does |
| :---- | :---- |
| `/fact-find` | Pre-fills your fact-find from uploaded documents (photos and scans are fine), the meeting transcript or notes, and the CRM record. Every answer shows where it came from; conflicts are raised rather than guessed; gaps become a question list. Outputs your completed fact-find, a filled PDF or back-office import row, a source trail and a gaps list. |
| `/prospect-intake` | Turns a prospect's pile of pension and investment statements into a summary for the prospect, a paraplanner handoff and a "what happens next" note. It never misses the features that must be preserved (safeguarded benefits, guaranteed annuity rates, protected tax-free cash, exit charges, market value reductions) and tracks outstanding letters of authority. |
| `/pension-transfer-check` | Fact-find for a proposed transfer or consolidation: a table of the ceding scheme's features and guarantees, whether safeguarded benefits bring in the £30,000 advice requirement, scam red and amber flag indicators, a ceding-versus-receiving cost comparison and a chase list. It never judges suitability; that stays with the adviser and the pension transfer specialist. |

### Reviews and meetings

| Skill | What it does |
| :---- | :---- |
| `/pre-meeting` | Annual or ongoing review pack: client snapshot, wrapper-by-wrapper review, drawdown income taken, when attitude to risk and capacity for loss were last assessed, planning points to discuss, evidence that the ongoing service was delivered (Consumer Duty), agenda and talking points. |
| `/post-meeting` | Turns the meeting into a file note, follow-up tasks and opportunities, with everything the FCA expects to see evidenced. You approve the lot in one go before anything is written to your CRM. |

### Planning

| Skill | What it does |
| :---- | :---- |
| `/retirement-income-review` | Drawdown sustainability evidence: income taken against plan, the withdrawal rate, cash buffer and sequencing-risk flags, your cashflow model's outputs as reported, and a checklist against the FCA's retirement income advice expectations. |
| `/portfolio-rebalance-review` | Drift against the client's risk profile or your model portfolios across SIPP, ISA, GIA and workplace pensions. It sets out tax-aware options for you to weigh and drafts a rationale memo for the file. |
| `/death-benefits-and-tax-brief` | Checks each plan's expression of wish against what the client wants. It also sets out the pension tax position (annual allowance, carry forward, MPAA, LSA and LSDBA, protections) and the facts relevant to pensions coming into inheritance tax from April 2027. |

### Compliance

| Skill | What it does |
| :---- | :---- |
| `/compliance` | Pre-checks client-facing material (emails, letters, newsletters, social posts, presentations) against FCA financial promotion rules, the Consumer Duty and pensions-specific expectations. It produces a findings table, disclosure wording to adapt, and a clean redraft for your compliance officer or network to review. |

## How it keeps you safe

- **It never gives advice.** No recommendations, no suitability judgements, no risk profiles. It prepares; you decide.
- **Every figure has a source.** Values are marked as read from a document, stated by the client, or worked out, and missing information is marked as missing, never estimated.
- **Nothing leaves without your say-so.** Every write to a CRM, every upload and every email waits for your explicit approval. Anything client-facing is routed through `/compliance` first.
- **It checks identity.** It won't proceed on a name match alone, so one client's data can't end up in another's file.
- **Some boxes are always yours.** Declarations, signatures, consents, and the assessed attitude to risk and capacity for loss are never filled in.
- **It stores no client data.** The plugin is instructions only. Client data stays in your Claude session, your working folder and your own systems.
- **Documents are treated as data.** Text inside a statement or email that looks like an instruction is ignored.

## Your firm's fact-find

Every firm's fact-find is different, so the plugin doesn't assume one. `/fact-find-setup` reads your form and builds a **fact-find schema**: a description of your sections and fields, in your order and wording, with each field linked to a standard meaning. "Scheme / insurer" and "Name of provider" both mean *pension provider*, so the same fact from a statement lands in the right box on any firm's form.

1. **Once per form version:** whoever owns the fact-find (usually the compliance lead or a senior paraplanner; the network, for appointed representatives) runs `/fact-find-setup` with the blank form. It checks the result and shows the fields it was unsure about. It always saves a **draft**, which a person at the firm reviews and marks approved.
2. **Once per adviser:** each adviser runs `/fact-find-setup`, picks the firm's shared schema, and pastes the one line it gives them into their Claude settings.
3. **For every client:** `/fact-find` with the client's documents and meeting notes.

Accepted forms: fillable PDF (filled directly), flat PDF or scan, Word, Excel, or a back-office import template (Claude produces a ready-to-import row). No setup yet? `/fact-find` falls back to a generic UK pensions fact-find and labels it clearly. Firms that keep their own copy of this plugin can put their schema in [`firm-config/`](firm-config/) so every adviser gets it on install. The file format is documented in [`skills/fact-find-setup/references/schema-format.md`](skills/fact-find-setup/references/schema-format.md).

## Connecting your systems

Connectors let Claude read from (and, with your approval, write to) the systems you already use. These come with the plugin; you sign in to each from Claude's connector settings:

| Connector | Used for |
| :---- | :---- |
| Microsoft 365 | Outlook email and calendar, SharePoint and OneDrive documents |
| Gmail, Google Calendar, Google Drive | Email, calendar and documents for Google Workspace firms |
| Box, Dropbox | Client document stores |
| Salesforce | CRM for firms on Salesforce Financial Services Cloud |
| Zocks | AI meeting notes and action items |
| Zoom, Slack | Meetings and internal collaboration |
| Addepar | Portfolio data, for wealth managers who use it |
| Morningstar, FactSet | Fund and market research |

**Most UK adviser systems don't have connectors yet.** That includes back offices (Intelligent Office, Xplan, Curo, Plannr), platforms (Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus), cashflow tools (Voyant, CashCalc, Truth, Timeline), research and risk tools (FE Analytics, Defaqto, Dynamic Planner, Synaptic) and transfer tools (Origo Options, Selectapension). That's fine: every skill asks you to upload or paste an export instead and carries on. If your firm adds a connector for one of them, the skills find it by name automatically.

## Keeping it current

UK pension rules change at every fiscal event. The FCA checklist used by `/compliance` and the tax figures used by `/death-benefits-and-tax-brief` are **snapshots for the 2026/27 tax year**, not live feeds. Check them against the FCA Handbook, HMRC guidance and your firm's technical resources before relying on them. Contributions that update them are very welcome.

## What's in this repository

```
skills/          one folder per skill (SKILL.md plus its templates, references and scripts)
agents/          narrow helper agents the skills hand work to (e.g. reading one statement)
examples/        a fictional firm's fillable fact-find and its schema, for practice
firm-config/     where a firm's own fork keeps its fact-find schema
docs/            maintainer notes: the UK regulatory frame, the tax snapshot, the UK tech stack
.mcp.json        the connectors that ship with the plugin
```

Everything is Markdown, JSON and a few small Python scripts; there's no server and no database.

## Contributing

Corrections from advisers, paraplanners and compliance professionals are especially welcome: an outdated rule, a pension feature we should never miss, a UK system that now has a connector. See [CONTRIBUTING.md](CONTRIBUTING.md). Never include real client data in an issue or pull request.

<details>
<summary><strong>How this differs from Anthropic's original</strong></summary>

- **Regulation:** SEC Marketing Rule, Section 206, Rule 204-2, Reg BI and FINRA 2210 are replaced by FCA COBS 4, the Consumer Duty (PRIN 2A), the COBS 9 and 19 pension transfer and retirement income rules, SYSC 9 and COBS 11.8 record keeping, FG21/1 on vulnerable customers, FG24/1 on social media, and the 2021 pension transfer conditions regulations.
- **Products and tax:** IRAs, 401(k)s, RMDs, Social Security, 529s, wash sales and step-up in basis are replaced by SIPPs, workplace and personal pensions, DB schemes, ISAs and GIAs, drawdown and UFPLS, State Pension, AA, MPAA, carry forward, LSA and LSDBA, the 30-day share-matching rule, and pensions and IHT from April 2027.
- **Skills:** `fact-find-setup`, `fact-find`, `retirement-income-review` and `pension-transfer-check` are new. `death-benefits-and-tax-brief` replaces `estate-and-tax-brief`, and `alts-brief` has been removed. The `nomination-compare` and `fact-extract` agents are new; `titling-compare` has been removed.
- **Connectors:** US wealth-tech connectors have been removed. The UK tech stack is handled by finding systems by name, with an upload fallback.
- **Kept from the original:** the careful engineering — finding connectors by name, marking missing data rather than inventing it, confirming identity before reading, one approval for a batch of writes, read-only helper agents, and treating third-party content as data.

Maintainer context is in [`docs/uk-pensions-context.md`](docs/uk-pensions-context.md).

</details>

## Security

To report a vulnerability, see [SECURITY.md](SECURITY.md).

<details>
<summary><strong>Security design notes</strong></summary>

The skills and agents here are instructions, not code, apart from three small Python scripts that read and fill PDF forms. Some guardrails are structural: the file-reading helper agents are limited to read-only tools, and the connector-reading agents are denied shell, file-write and web tools. The rest are enforced by the model following instructions rather than by the runtime: adviser approval before any write, connector-reading agents never calling a write or send tool, arithmetic in a shell that never sees document text, and form values passed to the PDF filler through a file rather than the command line. Helper agents read third-party content (pension statements, provider letters, client emails, CRM notes), so treat that content as untrusted. If you adapt these agents, keep the read-only and shell rules in place, prefer connectors that expose read-only tools, and don't widen any agent's tool list without reviewing what it reads.

</details>

## Important information

**For use by professionals at FCA-authorised firms only.** This plugin is a community-maintained set of instructions for an AI assistant. It supports research, information gathering, issue identification and the preparation of drafts and summaries. Neither the maintainer nor Anthropic is acting as, or holding itself out as, a financial adviser, investment manager, pension transfer specialist or any other regulated person.

The plugin does not give financial, investment, pension, tax or legal advice or personal recommendations. It does not assess suitability or appropriateness and does not make decisions on behalf of clients. It does not execute transactions, submit transfers or letters of authority, complete nomination forms, or sign or verify a fact-find on a client's behalf. It does not take account of any individual's circumstances beyond what the adviser chooses to supply for a specific task.

Outputs are generated by AI and may contain errors, omissions or outdated information, including outdated regulatory and tax references. Outputs must be independently reviewed and must not be relied on as the sole basis for advice, a suitability report, a financial promotion approval or any client-facing decision. Firms and individuals remain solely responsible for the advice they give, for their obligations under the FCA Handbook (including the Consumer Duty and SM&CR), for data protection, for record keeping, and for their firm's or network's own sign-off processes. Content from third-party providers remains subject to those providers' terms.

## Licence

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE).

Original work copyright 2026 Anthropic PBC. Modifications copyright 2026 Vaynork.
