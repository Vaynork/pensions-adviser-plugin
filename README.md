# Pensions Adviser (UK)

A Claude plugin for **UK pensions and retirement advisers and paraplanners** at FCA-authorised firms. It gives you ready-to-run workflows for annual review preparation, meeting write-ups, compliance pre-checks, pension statement intake, pension transfer fact-finding, drawdown reviews, portfolio reviews, and death-benefit and allowance briefs. The workflows draw on the tools your firm already uses, through connectors where they exist and paste or upload where they don't.

> **Unofficial community adaptation.** This is a fork of Anthropic's [Claude for Financial Advisors](https://github.com/anthropics/claude-for-financial-advisors) reference plugin. The original targets US advisers (SEC Marketing Rule, Reg BI, IRAs and 401(k)s, US wealth platforms). This fork reworks it for the UK regime: FCA rules, Consumer Duty, UK pension wrappers and the UK adviser tech stack. It is **not affiliated with, endorsed by or supported by Anthropic.**

The plugin is a set of skills written as plain instructions (Markdown and JSON). It holds no client data. When an adviser runs a skill, Claude pulls what it needs from connected systems or from files the adviser provides. The adviser must approve any action that writes back to an external system (CRM notes, tasks, email drafts). Claude gathers, organises, summarises, compares and presents information. The adviser exercises judgement, makes the recommendation and gives the advice.

Professional support for advisers only. Nothing here is financial, tax, legal or regulated advice, and nothing here is a suitability determination.

## Skills

| Skill | What it does |
| :---- | :---- |
| `/onboarding` | Guided first-run setup. Learns your role, whether your firm is directly authorised or an appointed representative, whether you give independent or restricted advice, and your tech stack. Then it connects what can be connected and runs a demo on a fictional UK household. |
| `/pre-meeting` | Annual or ongoing review prep pack: client snapshot, wrapper-by-wrapper pension and investment review, drawdown income taken, attitude to risk and capacity-for-loss dates, planning points to discuss (allowances, crystallisation, State Pension, nominations), Consumer Duty evidence that the ongoing service was delivered, agenda and talking points. |
| `/post-meeting` | Turns a meeting (from a note-taker, CRM summary or transcript) into a file note, follow-up tasks and opportunities, all approved in one batch before anything is written. It captures what the FCA expects to see evidenced. |
| `/compliance` | Pre-checks client-facing material against FCA financial promotion rules (COBS 4: fair, clear and not misleading; past and future performance), the Consumer Duty consumer-understanding outcome, pensions-specific expectations (DB transfers, drawdown, consolidation, tax-free cash) and FG24/1 for social media. It produces a findings table, disclosure wording to adapt and a clean redraft for your compliance officer or network. |
| `/prospect-intake` | Normalises a prospect's pension and investment statements into a summary, a paraplanner handoff and a "what to expect" note. It never misses the features that must be preserved: safeguarded benefits, guaranteed annuity rates, protected tax-free cash, exit charges and market value reductions. It also tracks outstanding letters of authority. |
| `/fact-find-setup` | One-off setup that loads **your firm's own fact-find** — a fillable or flat PDF, Word, Excel, a back-office import template, or an existing schema — maps every field to a standard vocabulary, validates it, and saves a reusable schema for your compliance owner to sign off. Each adviser runs it once to point at the firm's shared schema. Without it, `/fact-find` uses a generic UK pensions fact-find. |
| `/fact-find` | Pre-fills that fact-find from what you already hold: uploaded statements, photos or scans of client documents, the meeting transcript or file notes, and the CRM record. Every answer shows its source and whether it was read, stated by the client or inferred. Conflicts are surfaced, never resolved silently. Declarations, signatures and the assessed risk result are always left blank. Produces the completed fact-find, a filled copy of your PDF form (if it's fillable) or a back-office import row, a source trail, and a gaps list of questions still to ask. |
| `/pension-transfer-check` | Fact-finds a proposed transfer or consolidation. It builds a ceding-scheme features table, identifies safeguarded benefits and the £30,000 advice requirement, lists scam red and amber flag indicators under the 2021 transfer regulations, compares costs from supplied figures and produces an information chase list. It never assesses suitability; that stays with the adviser and the pension transfer specialist. |
| `/retirement-income-review` | Drawdown sustainability evidence: income taken against plan, withdrawal rate from supplied figures, cash buffer and sequencing-risk flags, cashflow-model assumptions and outputs quoted as reported, and a checklist against the FCA's retirement income advice expectations (TR24/1). |
| `/portfolio-rebalance-review` | Drift against the client's risk-profile model or your centralised investment proposition, across SIPP, ISA, GIA and workplace wrappers. Lays out tax-aware options (wrappers first, the CGT annual exempt amount, the 30-day share-matching rule, Bed & ISA and Bed & SIPP) without disrupting drawdown income, and drafts a rationale memo for the file. |
| `/death-benefits-and-tax-brief` | Checks each plan's expression of wish or nomination against what the client intends. It also reports the pension tax position (annual allowance, carry forward, MPAA, LSA and LSDBA, protections) from figures on file and summarises the facts relevant to the April 2027 pensions and inheritance tax change. It refers every flag to the client's solicitor or the scheme administrator. |

Every skill falls back to paste or upload when a system isn't connected, and every write to a client system pauses for adviser approval.

## Using your firm's own fact-find

Every firm's fact-find is different, so the plugin doesn't assume one. It works from a **fact-find schema**: a JSON description of your form's sections and fields, in your order and wording, with each field mapped to a standard meaning (`pension.provider`, `retirement.income_need` and so on). That mapping is what lets the same extracted fact land in the right box on any firm's form.

1. **Once per form version** — whoever owns the fact-find (usually the compliance lead or a senior paraplanner; the network, for appointed representatives) runs `/fact-find-setup` with the blank form. It builds the schema, validates it, and shows the mappings it was unsure of. Save it somewhere shared, have it reviewed, and mark it approved.
2. **Once per adviser** — each adviser runs `/fact-find-setup`, chooses the firm's shared schema, and pastes the one line it gives them into their Claude settings.
3. **For every client** — `/fact-find` with the client's documents and meeting notes.

Firms that keep their own fork of this plugin can commit the schema to [`firm-config/`](firm-config/) so every adviser gets it on install. The format is documented in [`skills/fact-find-setup/references/schema-format.md`](skills/fact-find-setup/references/schema-format.md). A fictional sample form and its schema are in [`examples/`](examples/) to try it out. Filling a PDF form needs Python with `pypdf` (`python -m pip install pypdf`); everything else works without it.

## Connectors

Connectors declared in [`.mcp.json`](.mcp.json):

| Connector | Used for |
| :---- | :---- |
| Microsoft 365 | Outlook email and calendar, SharePoint and OneDrive documents |
| Gmail, Google Calendar, Google Drive | Email, calendar and documents for Google Workspace firms |
| Box, Dropbox | Client document stores |
| Salesforce | CRM for firms on Salesforce Financial Services Cloud (instance URL set at connect time) |
| Zocks | AI meeting notes and extracted action items |
| Zoom, Slack | Meetings and internal collaboration |
| Addepar | Portfolio data for wealth managers who use it |
| Morningstar, FactSet | Fund and market research |

**Most UK adviser systems don't have MCP connectors yet.** That includes back office systems (Intelligent Office, Xplan, Curo, Plannr), platforms (Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus), cashflow tools (Voyant, CashCalc, Truth, Timeline), research and risk tools (FE Analytics, Defaqto, Dynamic Planner, Synaptic) and transfer tools (Origo Options, Selectapension). The skills look for these systems by name in case your organisation has added a connector. If none is found, they ask you to paste or upload an export and carry on. If a vendor ships an MCP server, add it to `.mcp.json` and the skills will pick it up.

## Installation

```
claude plugin marketplace add Vaynork/pensions-adviser-plugin
claude plugin install pensions-adviser
```

## What changed from the original

- **Regulation:** SEC Marketing Rule, Section 206, Rule 204-2, Reg BI and FINRA 2210 are replaced by FCA COBS 4, the Consumer Duty (PRIN 2A), the COBS 9 and 19 pension transfer and retirement income rules, SYSC 9 and COBS 11.8 record keeping, FG21/1 on vulnerable customers, FG24/1 on social media, and the 2021 pension transfer conditions regulations.
- **Products and tax:** IRAs, 401(k)s, RMDs, Social Security, 529s, wash sales and step-up in basis are replaced by SIPPs, workplace and personal pensions, DB schemes, ISAs and GIAs, drawdown and UFPLS, State Pension, AA, MPAA, carry forward, LSA and LSDBA, the 30-day share-matching rule, and pensions and IHT from April 2027.
- **Skills:** `fact-find-setup` and `fact-find` are new: they fill any firm's own fact-find from client documents and meeting notes. `alts-brief` has been removed. `estate-and-tax-brief` has been replaced by `death-benefits-and-tax-brief`, and `retirement-income-review` and `pension-transfer-check` are new. The `titling-compare` agent has been replaced by `nomination-compare`.
- **Connectors:** US wealth-tech connectors have been removed. The UK tech stack is handled through name-based discovery with a paste or upload fallback.
- **Engineering discipline kept:** everything that made the original careful. Discovery by tool name, the "pending" markers for missing data instead of invented figures, no proceeding on a name match alone, one approval for a batch of writes, read-only subagents, and treating third-party content as data rather than instructions.

Maintainer context (regulatory frame, the 2026/27 tax snapshot, UK tech stack) is in [`docs/uk-pensions-context.md`](docs/uk-pensions-context.md).

## Keeping it current

UK pension rules change at every fiscal event. The regulatory checklist in `skills/compliance/references/` and the tax-constant snapshot in `skills/death-benefits-and-tax-brief/references/` are **static snapshots for 2026/27**, not live feeds. Check them against the FCA Handbook, HMRC guidance and your firm's technical resources before relying on them, and update them each tax year.

## Security

See [SECURITY.md](SECURITY.md).

**Security considerations.** The skills and agents here are instructions, not code. Some guardrails are structural: the file-parsing subagents are allowlisted to read-only tools, and the connector-reading subagents are denied shell, file-write and web tools. The rest are enforced by the model following them, not by the runtime: adviser approval before any write, connector-reading subagents never calling a write or send tool, and arithmetic in a shell that never sees document text. Subagents read third-party content (pension statements, provider letters, client emails, CRM notes), so treat that content as untrusted. If you adapt these agents, keep the read-only and shell rules in place, prefer connectors that expose read-only tools, and don't widen any agent's tool list without reviewing what it ingests.

## Important information: for use by professionals at FCA-authorised firms only

This plugin is a community-maintained set of instructions for an AI assistant. It supports research, information gathering, issue identification and the preparation of drafts and summaries. Neither the maintainer nor Anthropic is acting as, or holding itself out as, a financial adviser, investment manager, pension transfer specialist or any other regulated person.

The plugin does not give financial, investment, pension, tax or legal advice or personal recommendations. It does not assess suitability or appropriateness and does not make decisions on behalf of clients. It does not execute transactions, submit transfers or letters of authority, complete nomination forms, or sign or verify a fact-find on a client's behalf. It does not take account of any individual's circumstances beyond what the adviser chooses to supply for a specific task.

Outputs are generated by AI and may contain errors, omissions or outdated information, including outdated regulatory and tax references. Outputs must be independently reviewed and must not be relied on as the sole basis for advice, a suitability report, a financial promotion approval or any client-facing decision. Firms and individuals remain solely responsible for the advice they give, for their obligations under the FCA Handbook (including the Consumer Duty and SM&CR), for record keeping, and for their firm's or network's own sign-off processes. Content from third-party providers remains subject to those providers' terms.

## Licence

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE).

Original work copyright 2026 Anthropic PBC. Modifications copyright 2026 Vaynork.
