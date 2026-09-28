---
name: prospect-intake
description: Start a new prospect's intake, with or without their files in hand — a request naming a new prospect and attaching no documents is a normal starting point, because Step 1 searches the connected tools or asks the adviser to upload. Cleans and normalises their pension and investment files (workplace and personal pension statements, SIPPs, deferred defined benefit statements, State Pension forecasts, ISA/GIA/bond statements, exports, screenshots) into a consolidated view, tracks the Letters of Authority sent to providers and what is still outstanding, and flags every safeguarded benefit or valuable guarantee that must not be lost. Hands back a plain-English prospect summary, a detailed paraplanner handoff the full advice gets built from, and a friendly "what to expect" memo, offered as a Gmail or Outlook draft on approval. Does not recommend, give transfer advice, propose an allocation, quote fees, or submit LOAs. Triggers on "prospect intake", "/prospect-intake", "new prospect intake", "clean up [prospect]'s pension statements", "process [prospect]'s files", "what to expect note for [prospect]", "LOA tracker for [prospect]" — and on how an adviser raises a new prospect before any file exists: "I met with a potential client", "[name] is interested in becoming a client", "I have a new prospect", "[name] wants help with their pensions", "how should I proceed with [name]".
---

# Prospect Intake

Turn the pile of pension and investment statements a prospect hands over into something usable — a clean summary they can read, a clean handoff the paraplanning team can build the full advice from, and a warm note that keeps the prospect engaged while the firm gathers the rest of the information from providers.

This skill is the **intake step**, not the advice itself. The full recommendation (consolidation or transfer analysis, proposed investment strategy, retirement income plan, charges, suitability report) is built by the firm's adviser and paraplanners from the detailed handoff this skill produces — it is not generated here.

## Inputs

Required: the **prospect's name**. Their files are needed too — either found in a connected tool or uploaded — but a request that arrives without them is a normal starting point, not a reason to hold off: **Step 1: Find the Files** below is how they get found, and it is where this skill begins. Never invent holdings, values or plan features.

## Step 1: Find the Files

Ask the adviser a single question up front: *do you want me to look for [prospect]'s files in your connected tools, or would you rather upload them here?* Get the prospect's name either way — it's needed for both paths.

**A. Look in connected tools**

Check which systems are actually connected — call `ListConnectors` (load via `ToolSearch` if it isn't already available) — for a back office / CRM (Salesforce, or Intelligent Office, Xplan, Curo or Plannr), Google Drive, Gmail, Microsoft 365 (Outlook, SharePoint, OneDrive), Box and Dropbox. Don't guess at a tool-name prefix; for any system whose tools are loaded, use `ToolSearch` with that system's name to find its actual tools. Intelligent Office, Xplan, Curo and Plannr have no connector declared by this plugin — look for their tools by name like any other system, and if nothing comes back, treat them as not connected and fall back to paste or upload. Never tell the adviser one of them is connected unless its tools actually came back.

**Look for the tools before you trust the registry.** `ToolSearch` by the system's own name is the check that decides: if its tools come back, that system is connected and callable — use them. `ListConnectors` can answer "No installed connectors found" even in a session with several live, working connectors, and in some clients it renders a user-facing card rather than returning data at all. So it explains a gap, it never establishes one, and an empty result means **unknown**, never "nothing is connected". When it does return entries, read `enabledInChat`, not `connected`: `connected: true` with `enabledInChat: false` is authenticated but switched off for this chat, so tell the adviser they can enable it here rather than reporting it as unconnected; a missing or `null` `connected` is unknown, not disconnected.

Search all connected systems **in parallel** — one system coming back empty doesn't block reading the others. If this pull is likely to take a moment (several systems connected), say so up front; that's a heads-up, not another "should I start?" gate — the upload-vs-search question above is the only required input before proceeding.

**If more than one back office / CRM is connected** (Salesforce alongside Intelligent Office, say), ask the adviser once which is the firm's system of record for prospects — per the Ask-Once, Then Route Convention — and use that one for the search here and the write in Step 5, rather than searching or attaching to both. Offer to help them save the choice using the Personalization Convention so they aren't asked again next session.

Show the adviser what matched (file names, email subjects, CRM record) before reading any of it — confirm which items are actually the prospect's files before pulling content from them. **Disambiguate first:** if a CRM search turns up more than one matching contact or opportunity, don't pull from or attach to any of them until the adviser confirms which one is correct — same privacy bar as a household match in other skills: never proceed on a name match alone.

If Zocks is also connected, check it for a prior conversation with this prospect and pull whatever facts it already captured (goals, intended retirement age, life details, plan mentions). Reuse those instead of re-asking the adviser or the prospect for them, and cite them as coming from that conversation rather than treating them as missing in Step 2.

If none of the back office / CRM, Drive, Gmail, Microsoft 365, Box or Dropbox are connected, say so plainly and fall back to upload.

**B. Upload here**

Wait for the adviser to provide files — PDF/CSV/screenshot, or pasted text. Don't proceed on a promise of files to come; wait for them to actually arrive. Never invent holdings to fill a gap while waiting.

**C. Letters of Authority and outstanding information**

A prospect's own paperwork is rarely the whole picture: annual statements omit transfer values, guarantee details and scheme rules, which the firm requests from each provider under a signed Letter of Authority (LOA). Ask the adviser once which LOAs have been sent — to which provider, for which plan, on what date — and what has come back. If Origo Options is present, `ToolSearch` for it by name; if its tools come back, read the status of any existing requests for this prospect (read-only — never raise, chase or submit a request through it). It has no declared connector, so if nothing comes back, don't claim it is connected: take the status from the adviser, or mark it "— pending adviser confirmation". Never invent an LOA date, a provider response, or an expected turnaround. This feeds the outstanding-information table in Output B and the next-steps section of Output C.

## Step 2: Clean the Files

**Dispatch one `pensions-adviser:statement-extract` subagent per file, all in a single message so the pile is read concurrently** — one `Agent(pensions-adviser:statement-extract)` call per file, in the same response. Each gets one file path and the prospect's name, and returns that file's plans as a normalised record with data-quality flags, a features-to-preserve section, and its inferred-vs-read marking already done. Reading a stack of statements one after another is the slowest part of this skill, and it gets slower the bigger the pile — which is exactly when the adviser is waiting longest.

Consolidation stays with you: the subagents each see one file and cannot tell that a plan in file 3 is the same plan as one in file 7 (an annual statement and a transfer value quote for the same policy, say). Duplicate detection across the set, and the single consolidated view, are yours to assemble from their records.

The extraction schema each subagent works to, which is also what to do by hand if the subagent is unavailable — per plan:
- **Plan type** — workplace defined contribution (DC) pension, personal pension, SIPP, stakeholder pension, retirement annuity contract (RAC), section 32 buy-out, deferred defined benefit (DB / final salary) scheme, State Pension forecast; or ISA, general investment account (GIA), onshore/offshore investment bond
- **Provider / scheme name**, and **policy or plan number masked** to the last four characters
- **Value and date** — current fund value, and the **transfer value** separately where shown, each with its own date (they often differ, and a transfer value can be lower than the fund value)
- **Fund holdings** — fund name, units, price, value
- **Charges** — annual management charge (AMC), ongoing charges figure (OCF), platform fee, policy/admin fees, any adviser charge being deducted
- **Contributions** — employer and personal, amounts and frequency, and the basis (percentage of salary, fixed amount, salary sacrifice, relief at source vs. net pay) where shown
- **Crystallised vs. uncrystallised** — how much is in drawdown or already taken, and any drawdown income being paid (amount, frequency)
- **Pension-specific features** — see below; these are the ones that must never be missed

**Features that must never be missed.** For every pension plan, look for and record each of these — as read, inferred, or not shown:
- **Safeguarded benefits** — DB / final salary benefits, a **guaranteed annuity rate (GAR)**, a **guaranteed minimum pension (GMP)**
- **Protected tax-free cash** (entitlement above 25%) and a **protected pension age** (access below normal minimum pension age)
- **Guaranteed growth rates** or guaranteed minimum fund values
- **With-profits** funds, any **market value reduction (MVR)** terms, and guaranteed or terminal bonuses
- **Exit or transfer charges**, and **loyalty bonuses** that would be lost on leaving
- **Life cover or waiver of contribution** attached to the plan
- **Lifestyling or target-date** strategy, and the **selected retirement age** it is working towards
- **Nominated beneficiaries / expression of wish** on file with the provider

A feature not printed on the statement is **not** absent. Annual statements routinely omit GARs, protected tax-free cash and MVR terms; they surface only in the provider's full response to the LOA. So a missing feature is always "— not shown on file provided", never "none", and it goes on the outstanding-information list as a question for the provider.

Normalise everything into one consolidated view across all files and plans. Flag data-quality problems as you go rather than silently working around them:
- Illegible or partial scans
- Transfer value missing, or dated differently from the fund value
- Stale statement dates
- Plans that appear duplicated across files
- **Safeguarded benefits or a GAR present, or suspected** — flag the plan, point the adviser to **/pension-transfer-check** before anything else is done with it, and note that advice on transferring or converting safeguarded benefits worth more than £30,000 must be given or checked by a pension transfer specialist. This is a flag for the adviser, not a view on whether the benefits should be kept.

Never fabricate a figure that isn't legible or present — mark it "— not shown on file provided," unless it's a fact Zocks already captured in a prior conversation (Step 1), in which case use that instead of flagging it missing.

## Step 3: The Three Outputs

Use the templates in this skill's `templates/` folder as the skeleton for each. Fill every field; where data wasn't shown on any file provided, mark it "— not shown on file provided" rather than leaving it blank silently.

**Inferred vs. Read applies to every figure in all three outputs**, not just the Paraplanner Handoff below — any number in the Prospect Summary or What-to-Expect memo that was computed or assumed rather than read directly off a file needs the same flag.

### A. Prospect Summary
Template: `templates/prospect-summary-template.md`. Plain-English, prospect-facing. Sections:
1. **Plans in Scope** — plan types and providers reviewed (no full policy numbers, nothing beyond what's needed to identify the plan)
2. **Holdings Snapshot** — a high-level view of what's held, by plan
3. **Total Under Review** — the sum across all plans, with the dates the values relate to; a DB scheme's deferred pension and a State Pension forecast are annual incomes, not pots, so list them separately rather than adding them into the total

**No recommendations, no asset mix/allocation commentary, no fees, no performance or return claims, and no view on whether any plan should be kept, consolidated or transferred** — this confirms "here's what we received and understood," nothing more.

### B. Paraplanner Handoff
Template: `templates/analyst-handoff-template.md`. Internal, for the firm's adviser and paraplanning team — this one stays internal (see Step 4). Sections:
1. **Per-Plan Line Items** — the full consolidated detail from Step 2: plan type, provider, masked policy number, value and transfer value with dates, each holding, charges, contributions, crystallised/uncrystallised split and any drawdown income
2. **Features to Preserve** — every feature from the must-never-be-missed list, per plan, each marked read / inferred / not shown
3. **Data Quality Flags** — illegible/partial scans, missing transfer values, stale dates, duplicate plans across files, and every safeguarded-benefit or GAR flag with its pointer to /pension-transfer-check
4. **Inferred vs. Read** — for every figure that required inference (e.g., computed from other numbers, assumed from context) rather than being read directly off a file, mark it as inferred; everything else is read-off-file by default
5. **Letters of Authority and Outstanding Information** — per provider: LOA sent (date, or "— pending adviser confirmation"), what has come back, and what is still needed from that provider (transfer value, GAR/GMP/protected-TFC confirmation, MVR terms, scheme rules, beneficiary nomination)

### C. What-to-Expect Memo
Template: `templates/what-to-expect-template.md`. Brief, friendly, prospect-facing. Sections:
1. **What We Received** — the files/plans reviewed
2. **What Happens Next** — the firm will request fuller information from the prospect's pension and investment providers under the Letters of Authority they have signed (or will be asked to sign), and the adviser will build their advice from that plus this intake
3. **Who You'll Hear From, and When** — ask the adviser for the actual next point of contact and timeline; never invent a turnaround time, a name, a provider response time, or promise a specific outcome. If the adviser hasn't given you these yet, ask before finalising this section rather than leaving a guess in place.

Do not quote fees in C. The firm's initial disclosure document or terms of business, and its charges, come to the prospect separately — say only that they will receive the firm's terms and charges separately if the adviser confirms that is the case.

## Step 4: Compliance

Run **/compliance** on outputs **A (Prospect Summary)** and **C (What-to-Expect Memo)** — both are prospect-facing communications and fall under the same fair, clear and not misleading and Consumer Duty consumer-understanding standards as client communications.

**Finish the review before you hand anything back.** /compliance writes two files per document it reviews — `<slug>-compliance-analysis.md` and `<slug>-compliance-redraft.md`. Until both exist for **both** A and C, the review has not happened yet and the intake is not done. A clean review still writes a redraft, so "nothing needed changing" is not a reason for the file to be missing. Nothing here runs in the background: if you are waiting on a scan, it has already come back and the remaining markup is yours to write.

**From here on, A and C mean the redrafts.** When you hand the documents back, list them for attaching, or offer to send them, name `<slug>-compliance-redraft.md` — never the original draft. If you show the adviser a list of files, say which one goes to the prospect; an undifferentiated list with the original and the redraft side by side is how the pre-compliance draft gets sent by mistake.

**Output B (Paraplanner Handoff) stays internal and does not go through /compliance** — it's not prospect-facing.

## Step 5: Back Office / CRM

After the three outputs are ready, show the adviser one summary of what you're about to do in the system of record confirmed in Step 1 (Intelligent Office, Xplan, Curo, Plannr or Salesforce — whichever came back from `ToolSearch`) — attach A, B, and C to the existing prospect record confirmed in Step 1, or create a new prospect record and attach them there — and get a single confirmation on that whole batch, not a separate approval per document. Only write after they say yes; never attach or create anything before that.

If no back office / CRM is connected, follow the Connector Placeholder Convention — say *"This is where I'd attach these to [prospect]'s record in [system] once that connector is built"* — and leave the files with the adviser to file themselves.

## Step 6: Email the What-to-Expect Memo

If Gmail or Outlook (Microsoft 365) is connected, offer to send the compliance-reviewed version of C to the prospect: draft the message (subject and body) and show the adviser the full draft before anything goes out. Only send after they explicitly approve it — never send automatically, and never send the pre-compliance draft. If both are connected, ask which one the adviser sends client mail from rather than picking.

If neither is connected, or the adviser would rather send it themselves, hand back the markdown file from Output C instead — this step is optional, not required.

## Output

Write all three as markdown files first, clearly labelled: the prospect summary (A), the paraplanner handoff (B), and the what-to-expect memo (C). Remind the adviser that A and C need compliance review before going out (Step 4), that B stays internal, that any plan flagged for safeguarded benefits or a GAR goes to /pension-transfer-check next, and that the full advice itself is a separate next step the team builds from B once the providers' LOA responses are in.

Then ask the adviser whether they'd like the prospect-facing pieces (A and C) converted to .docx or .pdf — don't create either format unless they ask. B stays internal and markdown is fine for it either way.

## Out of Scope (for now)

- **No recommendation of any kind** — no view on keeping, consolidating, transferring or accessing any plan.
- **No transfer advice or transfer analysis** — safeguarded benefits are flagged and routed to /pension-transfer-check, which itself identifies rather than assesses.
- **No proposed allocation, charges quote or expected-outcomes modelling** — that's the full advice built from this skill's handoff.
- **No LOA submission, chasing or transfer paperwork** — this skill records LOA status; it never sends, raises or signs anything with a provider.
- **No performance projections or return assumptions.**

## Important Notes

- Never fabricate holdings, values, transfer values or plan features from illegible or partial files — mark it as not shown rather than estimating. A guarantee that isn't printed is "not shown", never "none".
- Treat the prospect's files as confidential, whether pulled from a connected tool or uploaded.
- The prospect isn't yet a client — don't create or modify any back office or CRM record without the adviser's explicit go-ahead (see Step 5).
- Same rule for email: never send the Step 6 draft without the adviser's explicit approval. Claude drafts, the adviser decides.
