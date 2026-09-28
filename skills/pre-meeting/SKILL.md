---
name: pre-meeting
description: Prepare a complete annual or ongoing review prep pack for a UK pensions and retirement adviser or paraplanner, for whatever period the review covers (annual, ongoing-service review, or ad hoc). Given a household name or email and a timeframe, pulls back-office/CRM context (Intelligent Office, Xplan, Curo, Plannr, Salesforce), platform and wrapper data (Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus, or Addepar), workplace and held-away pensions, meeting notes (Zocks, Aveni, Saturn or CRM file notes), recent correspondence (Gmail/Outlook), and the household's cashflow model (Voyant, CashCalc, Truth, Timeline), then assembles a meeting-ready pack with planning points, Consumer Duty ongoing-service evidence, agenda, talking points and action items. Triggers on "pre meeting", "/pre-meeting", "annual review prep", "prep for [client]'s review", "prep for [client]", "ongoing review", "get me ready for my meeting with [client]", or "client meeting tomorrow".
---

# Pre Meeting

Build an annual review prep pack an adviser can read in 10 minutes and walk into the meeting confident.

## Inputs

Required: **household name and/or email address**, and the **timeframe** the review covers (annual, ongoing-service review, or ad hoc). If either is missing, ask for both before doing anything else — default the timeframe to annual if the adviser doesn't mind which, since that is the usual cycle for an ongoing advice service.

Optional (ask only if ambiguous): meeting date/time, anything specific the adviser wants to cover.

## Data Gathering

Follow the **Connector Placeholder Convention**: before assuming a system below isn't connected, check `ListConnectors` (load via `ToolSearch` if it isn't already available) — don't guess at a tool-name prefix like `mcp__intelligent_office__*`, since real connector tool names use opaque prefixes. If it's connected, use `ToolSearch` (by system name) to find its actual tools. If it's not connected, say "This is where I'd make a call out to [system] to pull [data] once that connector is built," then offer the manual fallback (paste, upload an export, or skip) and keep going. Apply this to every source below, not just the first one that's missing — and if more than one connected tool could try to solve the same problem for this household (not necessarily two of the same kind), ask the adviser once which is the book of record, per the Ask-Once, Then Route Convention, rather than guessing, and offer to help them save the choice using the Personalization Convention. This gathering pass touches several systems in sequence, so the check isn't a one-time thing at the top: re-run it whenever a later source could answer something an earlier one already did, and if two sources you did pull disagree on a material fact, stop and surface it to the adviser as a blocking question before the pack is finalised rather than presenting both. If the disagreement is by orders of magnitude for the same household, follow the Magnitude-Conflict Convention: name the conflict, and exclude the outlier's figures from every table and total rather than quoting them as evidence.

**Look for the tools before you trust the registry.** `ToolSearch` by the system's own name is the check that decides: if its tools come back, that system is connected and callable — use them. `ListConnectors` can answer "No installed connectors found" even in a session with several live, working connectors, and in some clients it renders a user-facing card rather than returning data at all. So it explains a gap, it never establishes one, and an empty result means **unknown**, never "nothing is connected". When it does return entries, read `enabledInChat`, not `connected`: `connected: true` with `enabledInChat: false` is authenticated but switched off for this chat, so tell the adviser they can enable it here rather than reporting it as unconnected; a missing or `null` `connected` is unknown, not disconnected.

**UK systems have no declared connector.** Of the systems below, only Salesforce, Addepar, Zocks, Gmail and Microsoft 365 ship as declared connectors in this plugin. Intelligent Office, Xplan, Curo, Plannr, the platforms (Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus and the rest), the note-takers (Aveni, Saturn) and the cashflow tools (Voyant, CashCalc, Truth, Timeline) are looked for by name via `ToolSearch` like any other system — a firm may have added its own — and otherwise fall back to paste or upload. Never tell the adviser one of them is connected unless its tools actually came back.

Once identity is confirmed, **pull from all connected sources in parallel** — one slow or missing source degrades only its own section of the pack, not the rest. Before starting this multi-source pull, tell the adviser what you're about to gather and why, so it doesn't look like a silent hang. And once the household and timeframe are known, don't ask "should I start?" — narrate what you're doing and go; approval gates in this skill apply only to format conversions and length changes at the end, not to starting the work.

**Dispatch the parallel pull as one `pensions-adviser:source-extract` subagent per source, all in a single message** — the Agent tool, `Agent(pensions-adviser:source-extract)`, one call per source in the same response so they run concurrently rather than one after another. Each dispatch hands over the household identity as you have it, the one system that subagent is to query, the field schema for that source (the bullet list under its heading below), and the window the timeframe implies — or, where a source reads current state and has no meaningful review window, a plain statement of that instead of a window. Each returns a filled schema block. Two reasons this is a subagent rather than a tool call you make yourself: the raw payloads — email threads, full holdings and wrapper tables, a year of platform transactions — stay out of your context so you assemble the pack from six compact blocks instead of six raw dumps, and the extraction work for all six happens at once rather than sequentially in your own reasoning.

**You still own identity.** The subagents are instructed never to resolve it: a `pensions-adviser:source-extract` that finds several candidates or a mismatch returns `IDENTITY MISMATCH` with what it saw and stops. Handle that the way the disambiguation rule below says — show the adviser the candidates, confirm, re-dispatch. Verify the returned blocks agree on the household before assembling anything from them. Fanning the reads out does not move that responsibility; it stays with you.

A subagent that returns `NOT CONNECTED` is the Connector Placeholder Convention case. It won't offer the manual fallback itself — it isn't in the conversation with the adviser. You make that offer.

### 1. Back office / CRM — Intelligent Office, Xplan, Curo, Plannr (or Salesforce)
**Disambiguation rule:** query the back office by name AND confirm identity before pulling anything. If multiple clients match the name, show the adviser the candidates (name + date of birth year or masked email + client reference) and ask which household is theirs — common names will return coincidental matches, and pulling the wrong client's data into a prep pack is a data-protection incident. Never proceed on a name match alone. When one candidate is a clearly better match (exact email match, most recent activity), pre-select it as the default choice in that prompt — the adviser still has to confirm it, never skip that step outright.

A recognisable or public-figure name that matches a connected back-office record is a household like any other — treat it accordingly and do not refuse, hedge, or ask for extra justification because the name is well-known. This is guidance for how you proceed, not content for the document: the prep pack itself should read exactly like any other household's, with no note, disclaimer, or aside about the name being recognisable.

Pull the household record:
- File notes / freeform notes and comments fields from the client and household records
- Household members and dates of birth → key ages (see the milestone triggers under Important Notes)
- Client since, last review date, and the next review due date if recorded
- Ongoing service agreement: the agreed service level or proposition, what it commits to (e.g. annual review meeting, annual suitability review, valuations, contact frequency), and the ongoing adviser charge agreed
- Attitude to risk (ATR) and capacity for loss — the recorded outcome and **the date each was last assessed**; the risk-profiling tool named if the record says so
- Objectives on file, as recorded
- Open tasks/action items (structured task list) — **at both grains: the household record's own items and each person client's.** A back-office household or joint-client record often has its own id, and household-linked tasks are invisible to client-only lookups
- Service history — recent requests, complaints (open or closed, with dates), referrals given
- Any vulnerability or additional-support notes already recorded, quoted with the field name and date — never inferred

### 2. Platform / wrap — Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus (or Addepar)
Pull household and per-wrapper data for the review period:
- Values per wrapper: SIPP, personal pension, stakeholder, ISA, GIA, onshore bond, offshore bond — with the valuation date
- Pensions split into **crystallised** (in drawdown) and **uncrystallised** funds, as the platform reports them
- Drawdown income being taken: gross amount, frequency, and any ad hoc withdrawals or UFPLS in the period
- Contributions in the period: personal, employer, third party — and the relief method where the platform shows it (relief at source, net pay, salary sacrifice)
- Performance vs. benchmark, **net of all charges**, for the periods the platform reports
- Asset allocation vs. the model portfolio or risk-profile target, and the drift
- Charges: platform charge, fund OCFs (or the weighted figure if reported), ongoing adviser charge taken, and any discretionary fund manager charge
- Cash balances and large flows in or out

**Addepar specifics (when it is the firm's portfolio system):** use `search_entities` to resolve the household, then read exposure and performance as the platform computes them — quote the returned rows as they come back, and don't re-aggregate them into totals of your own. Addepar is often the firm's consolidated view rather than the product provider, so it may not carry wrapper-level detail such as crystallised/uncrystallised splits or relief method; mark any such field "— pending [platform]" rather than inferring it from an Addepar total.

Where the connector exposes reconciliation or valuation-date status, pull and surface it — flag stale or unreconciled data before quoting balances built on it.

### 3. Workplace and other held-away pensions
Usually paste/upload: the client's latest benefit statements, scheme annual statements or a pension-tracing result. Look for a tool by name first (the scheme administrator, a pensions dashboard export) per the Connector Placeholder Convention, then ask for the documents. Pull, per scheme:
- Scheme name and type (defined contribution / defined benefit), and whether the client is an active, deferred or pensioner member
- DC: value and statement date, current contributions (personal and employer), selected fund or default strategy
- DB: deferred scheme pension at normal retirement age (NRA) as stated, the NRA itself, the revaluation basis if stated, and any tax-free cash / commutation terms quoted
- Any safeguarded benefits flagged in the paperwork (e.g. guaranteed annuity rates) — noted only, for `/pension-transfer-check` to pick up
- The date of the latest statement received — and "no statement on file" where there isn't one

Quote figures exactly as the statement gives them; never project a DB pension forward or estimate a transfer value.

### 4. Meeting Notes — Zocks (or Aveni, Saturn, or CRM file notes as fallback)
If Zocks isn't connected, look for other note-takers by name via `ToolSearch` (Aveni, Saturn, Microsoft Copilot meeting recaps) before falling back to back-office file notes. The guidance below is written for Zocks; apply the same principles — summaries first, dedupe, cite by meeting date, the back office as book of record — to any other note-taker you find.

There is no Zocks "prep" endpoint — Zocks' MCP only exposes atomised reads (contacts, meetings, per-meeting AI results, insights), not the finished brief its own product UI generates. Build the picture yourself:

- **Fan out, then dedupe.** Resolve the household's contacts, list their past meetings, then pull AI results/summaries per meeting. Per-meeting extractions repeat near-duplicate household/financial detail across meetings, and a long-standing household can return dozens of results and summaries — collapse those into one current picture instead of listing each copy.
- **Precedence, in order:** prefer Zocks' AI results/summaries over the raw transcript; use the transcript only when you need the client's own words verbatim (e.g., a direct quote), not as the default source; if Zocks isn't connected, or is connected but returns no contact/meetings for this household, fall back to whatever the back office has logged from prior meetings — the common case is the latter, not a missing connector; only fall back further to a manual paste/upload if neither is available.
- **Default to summary-first.** Don't dump every `ai_results_*` payload for every meeting — pull summaries for the last 1-2 meetings by default. Treat a full extraction fan-out across more meetings as a deeper, slower pass and ask the adviser before spending that extra latency.
- **Household is a relationship, not a record.** Zocks has no household object — it's "the people who usually meet together." Treat the back office's household record as the book of record and use Zocks only to colour it; reconcile what a meeting extraction says against the back office rather than treating any single meeting's extraction as authoritative.
- **One item, one row.** When a Zocks action item and a back-office task describe the same underlying thing (e.g. a request for a State Pension forecast mentioned in a meeting and tracked as a back-office task), merge them into a single line using the back office's status — never list it twice just because it showed up unresolved in Zocks and resolved in the back office.
- **Cite the meeting**, by date (and meeting ID if the tool returns one), for anything sourced from Zocks — and never attribute a fact to a back-office or cashflow source that the Zocks MCP itself didn't return — its tools expose Zocks's own meeting data only, not the systems Zocks integrates with.
- **Layer firm-level Insights separately**, when the connector has an insights tool — firm-wide trending topics, sentiment, referral opportunities. That's distinct from "what changed for this household" and belongs in Talking Points (see below), not folded into Since We Last Met. A household-scoped insight or sentiment result from the same tool, tied to this client specifically, is a Relationship Signal, not a firm trend — route it there instead.
- **Relationship signals — source from insights and notes, not task fields.** Populate the Relationship Signals section from Zocks' AI results/summaries and insights (`insights_query_insights`, when the connector exposes it) first, then back-office freeform notes fields (file notes, "notes"/"comments" on the client or household record) — never from structured task/action-item fields. Task fields track what's due, not what's true about the relationship, and are used inconsistently across firms; a back office with an empty task list can still have a rich file-notes field. This section should still populate from whichever of Zocks or back-office notes is available — it does not wait on both, and it never blocks on the task list being empty or unmaintained. If both Zocks and back-office notes are unavailable, mark the section "— pending Zocks / back-office connector" per the Connector Placeholder Convention rather than omitting it. Cite every signal the same way as above: date (and meeting ID if returned) for anything Zocks-sourced, the field name (e.g. "per Intelligent Office file note, 14/03/2026") for anything back-office-sourced. A signal with no source behind it doesn't go in the doc.
- **Possible vulnerability indicators — flag, never label.** While reading notes and summaries, watch for anything touching the four FCA FG21/1 drivers: **health** (physical or mental illness, a diagnosis, cognitive decline), **life events** (bereavement, divorce or separation, redundancy, becoming a carer, retirement itself), **resilience** (low savings, reliance on this income, debt, a sudden change in circumstances) and **capability** (low confidence with money or digital channels, language barriers, reliance on a family member to engage). Record each one cited to its source, framed as "for the adviser to consider" — for example "Bereavement mentioned (Zocks, 12/02/2026) — for the adviser to consider whether additional support is needed." Never write that the client **is** vulnerable, never infer an indicator the source doesn't state, and never add anything to a vulnerability field in any system.
- **This skill still writes the Proposed Agenda itself** from the gathered data — never call a Zocks-generated agenda/prep or its Default Prompts a substitute for that section.

### 5. Email — Gmail / Outlook (available today for most users)
Search correspondence with the household's email address over a window that follows the chosen timeframe — roughly the last 12 months for an annual review, the period since the last review for an ongoing-service review, or whatever's appropriate for an ad hoc one. Extract:
- Open requests or questions the client is waiting on
- Commitments the adviser made ("I'll get you a State Pension forecast", "I'll chase the old employer scheme for a statement")
- Life events mentioned (retirement date moving, redundancy, new grandchild, house move, health, bereavement, inheritance)
- Tone/sentiment — anything suggesting concern or dissatisfaction, or anything that reads like an expression of dissatisfaction that may need handling as a complaint (flag it; don't classify it)
- Evidence of ongoing service delivered: valuations or reports sent, review invitations issued, responses given

### 6. Cashflow model — Voyant, CashCalc, Truth, Timeline
**This source has no review window.** It reads the household's cashflow plan as it stands right now, so the dispatch hands that fact over in the window's place — never a blank, and never the review timeframe, which would imply a lookback this source doesn't have.

**Identity stays inside this pull**, the same way every other source resolves its own system: the subagent searches the cashflow tool for the household using whatever search that tool offers, and returns `IDENTITY MISMATCH` with what it saw if several match or none do.

Pull:
- The plan's last-updated date, which dates the plan without saying what changed in it
- The headline sustainability outputs **exactly as the tool reports them** — e.g. whether the plan shows funds lasting to the modelled age, the age at which assets run out if it reports one, any stress-test or scenario result it states, and the assumptions it names (growth, inflation, charges, target income)
- Goals or income targets as recorded in the plan

Quote every figure exactly as the tool returns it: never recompute, re-derive or re-round it, never convert a plan's output into a probability or a "funded" percentage the tool didn't itself state, and never fill a gap with a figure of your own.

**No plan on file** is a normal, informative answer, not a degraded read: sustainability outputs and goals are marked "not applicable — no cashflow plan on file" rather than left blank. An absent result is never rendered as zero or as a failing plan, never dropped silently — and never marked pending either, which would send the adviser chasing a connector problem instead of reading the honest answer. (A cashflow tool that isn't connected at all is still the "— pending [tool]" case.)

## Assemble the Prep Doc

Use `templates/pre-meeting-template.md` in this skill's folder as the document skeleton. Fill every section; where data was unavailable, mark it "— pending [source]" rather than leaving blanks silently.

The doc's sections, in order:
1. **Client Snapshot** — household and ages, client since and last review date, total under advice in £ across wrappers, ATR and capacity for loss with the date each was last assessed, and the ongoing service level agreed
2. **Relationship Signals** — client concerns/sentiment, life events, upcoming personal dates and milestones, possible vulnerability indicators (FG21/1 drivers, framed for the adviser to consider), proactive talking points — each signal cited to its source
3. **Since We Last Met** — open action items from last meeting with assignee and status (mark "unknown — pending back office" unless the back office's own task list confirms done; never infer "done" from a meeting-notes source that doesn't report completion), notable correspondence
4. **Pensions & Portfolio Review** — wrapper table (value, crystallised/uncrystallised, valuation date), performance net of charges vs. benchmark, allocation vs. risk-profile model and drift, drawdown income taken vs. what the plan or last review assumed, contributions in the period, held-away pensions, cash
5. **Planning Points to Discuss** — a checklist, populated only from figures and facts on file:
   - Annual allowance usage this tax year and carry-forward headroom from the three previous years — only from contribution figures on file; if the figures for any year are missing, say which and stop rather than estimating
   - MPAA — has it been triggered (flexible drawdown income, UFPLS), per the platform or back office, and with what effect on contributions
   - Tax-free cash and crystallisation timing — what is uncrystallised, and any stated plans
   - Drawdown sustainability — point to `/retirement-income-review` for the full picture; quote the cashflow tool's own headline here only as colour
   - State Pension — forecast on file (and its date) and State Pension age
   - Deferred DB benefits — what is held and at what NRA
   - Consolidation questions (old workplace pensions, multiple small pots) — point to `/pension-transfer-check`, especially where safeguarded benefits appear
   - Expression of wish / nomination review — last updated date, and the change from 6 April 2027 bringing most unused pension funds and death benefits into the estate for inheritance tax — point to `/death-benefits-and-tax-brief`
   - ISA allowance use this tax year
   - Protection gaps noted on file
   - Lasting power of attorney and will status, as recorded
6. **Ongoing Service & Consumer Duty evidence** — what the ongoing service agreement promises vs. what the records show was delivered this year, the charges paid in the period (from the platform), and fair-value talking points. Say plainly when evidence is missing ("no record of an annual valuation being sent — pending back office") rather than smoothing it over; the adviser needs to see the gap before the client or the FCA does
7. **Proposed Agenda** — a 45-60 minute agenda with time boxes
8. **Talking Points & Anticipated Questions** — 3-5 talking points in plain English (portfolio/market-facing — personal talking points live in Relationship Signals); firm-level Insights/trends when available; likely client questions (especially about underperformance or markets) with suggested framing
9. **Action Items Draft** — pre-drafted next steps to confirm in the meeting

This skill never computes or invents a plan probability, a "funded" status, a sustainable withdrawal rate or a stochastic result — the cashflow tool's own outputs go under Planning Points to Discuss as colour, quoted exactly as they came back, never as a plan section of their own. Tax constants (annual allowance, MPAA, ISA limit, State Pension age and the like) are quoted only as given by the adviser, the firm's technical source or a connected system for the applicable tax year — never recomputed or supplied from memory as if confirmed.

## Output

- Write the prep pack as a markdown file first. One page-ish summary up front, supporting tables behind it.
- Keep language client-friendly — the adviser may screen-share parts of it.
- After writing the markdown file, ask the adviser whether they'd like it converted to .docx or .pdf (via the docx skill) — don't create either format unless they ask. Also ask whether they'd like the pack longer or shorter, and revise if so.
- End the chat response with a 2-3 sentence "if you only read one thing" summary of the client's situation.

## Out of Scope (for now)

- **No recommendation or suitability determination.** This pack gathers facts and raises points to discuss; whether anything is suitable is the adviser's judgement, recorded in their own suitability process.
- **No trade, switch or fund-change execution.** This skill never places, stages or confirms a trade, a fund switch, a rebalance or a change to drawdown income.
- **No sending to the client.** The prep pack is for the adviser; sharing it is the adviser's call, through their normal workflow.
- **No computing plan probabilities, performance or tax constants not given.** See "Assemble the Prep Doc" above.
- **No legal or tax advice.** Death-benefit, IHT and will/LPA findings are flagged for the adviser (and the household's solicitor or accountant where relevant) to evaluate, not acted on here.

## Important Notes

- **Underperformance goes first, not buried.** If the portfolio trailed its benchmark after charges, put it in talking points with an honest explanation — advisers lose trust by dodging it.
- Never fabricate performance numbers, plan outputs, contribution figures or client details. If a source is unavailable and the adviser can't provide data, show the section as pending.
- Flag compliance-sensitive content: if the prep pack will be shared with the client, recommend running client-facing excerpts through **/compliance**.
- Watch for milestone triggers in the data and put them in the Client Snapshot and Relationship Signals:
  - **55** — normal minimum pension age; **57 from 6 April 2028**, so check dates of birth near the boundary and any protected pension age recorded
  - **Protected pension age** — where the scheme or back office records one, it overrides the NMPA for that arrangement; quote it, don't infer it
  - **State Pension age** — 66, rising to 67 between 2026 and 2028 depending on date of birth; quote the client's own SPA from a forecast where one is on file
  - **Approaching a scheme's normal retirement date** — for any workplace or DB scheme within the next few years
  - **75** — the death-benefit tax threshold: death before 75 generally lets beneficiaries draw free of income tax (within the allowance, if paid within two years); at or after 75, beneficiaries are taxed at their marginal rate
- Treat all client data as confidential; only include what's needed for this meeting.
