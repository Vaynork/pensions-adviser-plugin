---
name: post-meeting
description: Turn a client meeting into next-best-action follow-up for a UK pensions and retirement adviser or paraplanner — no drafting required. Given a meeting (via Zocks, Aveni, Saturn, back-office notetaker summaries, or a pasted transcript), finds the right household, drafts a file note that evidences what the FCA expects to see (objectives and circumstances, attitude to risk and capacity for loss, income needs, charges, whether the ongoing review was delivered, possible vulnerability indicators) plus the action items and opportunities it heard, shows them all in one batch for approval, then writes what's approved to the back office/CRM and offers to file the record in Drive. Triggers on "log the meeting", "log my meeting with [client]", "file note", "write up the review", "meeting follow-up", "post meeting", "/post-meeting", or "follow up on my meeting with [client]".
---

# Post Meeting

Turn a client meeting into a file note plus a confirmed set of follow-ups and opportunities — the write-up, to-do chasing, and opportunity-spotting advisers and paraplanners would otherwise do by hand, done for them, with the adviser approving every write before it happens. This is next-best-action: doing the follow-up, not drafting an email for the adviser to send. If the adviser wants something sent to the client, that goes through `/compliance` — this skill's default path is the back office/CRM, not a client-facing message.

## Inputs

Required: **the meeting itself** — identified by household/client name, or by whatever meeting metadata a connected source supplies. Pull the meeting's content in this order, stopping at the first that's available:

1. **Zocks AI results** — the meeting's AI-generated summary and extracted items, if Zocks is connected. Fall back to the raw transcript (also from Zocks) for direct quotes when the summary is ambiguous about wording.
2. **Other note-takers by name** — if Zocks isn't connected, look for Aveni (Aveni Assist) or Saturn via `ToolSearch` by the system's name. Neither ships as a declared connector in this plugin, so only use one if its tools actually come back; treat its summary the way Zocks' is treated above, and never claim it's connected when it isn't.
3. **Back-office/CRM notetaker summary** — when no note-taker is connected, the connected back office or CRM may hold a notetaker summary of the meeting (not a raw transcript). Use it as-is.
4. **Pasted transcript** — if none of these is available, ask the adviser to paste the transcript or their own rough notes.

Zoom is not a supported source yet — do not offer it or imply it's coming.

Infer the household and the meeting date rather than asking by default: from the transcript itself, from Zocks or other note-taker metadata (date and meeting ID, when present), or from the adviser's connected calendar. Only ask the adviser to identify the household or supply a date if none of those resolve it — never show a date picker as a first resort. Once you've inferred a date, put it on the note preview in Step 2 so the adviser can correct it if it's wrong.

Once the household and meeting are identified, don't ask "should I start?" — pull the meeting content per the waterfall above and go. The approval gate in this skill is on the write batch in Step 4, not on starting the work.

## Workflow

### 1. Identify the household

Query the household's back office/CRM by the client/household name — Intelligent Office, Xplan, Curo, Plannr or Salesforce, whichever is connected (only Salesforce ships as a declared connector here; look for the others by name via `ToolSearch`). **If more than one connected tool could try to solve this for the household**, ask the adviser once which is the book of record — per the Ask-Once, Then Route Convention — rather than guessing, and use that one for the rest of this workflow, including the Step 5 write. Offer to help the adviser save the choice using the Personalization Convention so they aren't asked again next session. If the adviser mentions a second back office or notes source later in the workflow, that's the same question again before anything from it gets merged in — and if two sources ever disagree on a material fact, stop and ask rather than writing a footnoted or averaged version back to the back office.

**Disambiguation rule:** never proceed on a name match alone. If more than one household matches, show the adviser the candidates (name + household + masked email or last-activity date) and ask which one is correct before touching any record — logging a meeting against the wrong household is a data-protection incident, not a minor mistake. Confirm identity even on a single match if anything about the context (household, recent activity) doesn't line up with what the adviser said.

Follow the **Connector Placeholder Convention**: if the back office's tools aren't available in this session, say "This is where I'd search [system] for this household once that connector is built," then ask the adviser to confirm the household manually and continue.

Whatever the back-office record turns up here — prior file notes, open tasks, past meetings — is auxiliary context for identifying the household and spotting duplicates in Step 3. It is never the source of *this* meeting's content; that always comes from the waterfall in Inputs above, with Zocks AI results as the primary source when connected.

### 2. Draft the file note

Draft the file note (the meeting content pulled via the Inputs waterfall, plus the inferred meeting date and type — e.g. annual review, ongoing-service review, ad hoc) and show the adviser what will be written, with the inferred date called out so it's easy to correct. Getting this right before writing matters more here than for most writes — in many back offices file notes are never edited in place, only replaced by deleting and recreating them, and the file note is part of the firm's record of the advice relationship.

Structure the note so it evidences what the FCA expects to see on file for a review. Under each heading, record only what the meeting content actually says, and write "not discussed" where it's silent — never fill a heading by inference:

- **Objectives and circumstances** — any change to the client's objectives, health, employment, retirement date, family, property, or other assets and liabilities, or confirmation that nothing has changed
- **Attitude to risk and capacity for loss** — whether they were discussed, and any change the client described or the adviser noted
- **Income needs** — any change to the income the client needs or is drawing, or to planned lump sums
- **Charges** — whether charges were discussed, and anything the client said about them
- **Ongoing review delivered** — whether this meeting constituted the review the ongoing service agreement commits to, as the adviser or the meeting content states it
- **Possible vulnerability indicators** — anything mentioned touching the FCA FG21/1 drivers (health, life events, resilience, capability), quoted or closely paraphrased, flagged **for the adviser to consider**. Never write that the client is vulnerable, and never populate a vulnerability field in the back office — raise it in the batch for the adviser to decide what, if anything, to record

### 3. Identify action items and opportunities

Read the meeting content for two distinct things and list them back to the adviser separately:

- **Action items** — commitments the adviser made or next steps that were agreed to (e.g., "I'll send the updated cashflow plan," "let's request a State Pension forecast," "I'll get a statement from the old scheme").
- **Opportunities** — things mentioned in passing that could grow or protect the relationship (e.g., "mentioned an old workplace pension from a previous employer," "bonus due in March — possible carry forward," "expecting an inheritance," "planning to retire next year," "hasn't reviewed their expression of wish since remarrying"). These are signals from *this meeting only*, not a full back-office opportunity review — call out that a deeper look (a dedicated opportunity-review pass) is a separate step if the adviser wants one.

Only include things actually said in the meeting content — never infer a commitment or opportunity that isn't there, and label anything uncertain as a possibility rather than a fact.

**Dup-check before proposing writes:** Zocks (the product, separately from its MCP) and other note-takers may already export their own summaries, tasks, and opportunities into the back office. Check the back office for tasks/opportunities already logged against this household around the meeting date — **at both grains, the household record's own items and each person client's** (household-linked items are invisible to client-only lookups) — before drafting new ones, and drop anything that's already there rather than proposing a duplicate.

### 4. Show the batch for approval

Present everything from Steps 2–3 as **one schema-shaped table**, not prose, and ask for a single confirmation on the whole batch rather than approving items one by one:

| Type | What | When | Who | Notes |
|---|---|---|---|---|
| File note | (note preview, with inferred date and the evidence headings) | meeting date | household | — |
| Task | action item text | due/target date if known | owner (usually the adviser or paraplanner) | — |
| Opportunity | opportunity description | — | — | any metadata the connected back office exposes (e.g. estimated size, stage) |
| Flag | possible vulnerability indicator, for the adviser to consider | meeting date | adviser | source quote; nothing written to a vulnerability field unless the adviser says so |

The adviser can approve all, some, or edited versions of any row.

### 5. Write what's approved

For whichever rows the adviser approves, create the corresponding record using the connected back office's or CRM's own entities — for example Salesforce's own note/task/opportunity objects, or the file-note, task and opportunity (or equivalent) records that Intelligent Office, Xplan or Curo expose through whatever tools a firm has connected — rather than assuming a generic mapping (e.g. Salesforce custom fields, or a field name from a different back office) that may not exist for the connected system. If the connected system has no entity for a row type, say so and leave that row unwritten rather than forcing it into another field. Confirm back with a short summary of what was logged.

### 6. Offer to file the record in Drive

After the back-office writes are done, if Drive is connected, offer to file the meeting record (as markdown) there too. If Drive isn't connected, skip this step silently — never hold up the back-office writes on it.

## Output

- The file note, action items, and opportunities are written directly to the back office/CRM per the approved batch — that's this skill's primary output, not a document.
- If filing the record to Drive, file it as markdown. Don't create a `.docx`/`.pdf`/`.xlsx` version unless the adviser asks for one.

## Out of Scope (for now)

- **Creating a new household/client** when no match is found — flag it to the adviser instead.
- **Editing any existing client field** (name, address, ATR, capacity for loss, vulnerability flag, etc.) noticed in the meeting content — flag it instead.
- **A full opportunity-analysis pass** against existing back-office records — this skill only surfaces what's in this meeting.
- **Recommendations or suitability.** The file note records what was discussed; it doesn't state that anything is suitable or draft a suitability report.
- **Sending anything to the client.** If the adviser wants to send a follow-up message, route it through `/compliance` — this skill's default path is the back office, not a client email.
- **Trade, switch or drawdown-income changes.**

## Important Notes

- **Every write pauses for adviser approval**, gated through the single batch in Step 4. Never create anything the adviser hasn't seen and confirmed.
- **Never fabricate** meeting content, action items, opportunities, or client details. If the meeting content is ambiguous about whether something was a firm commitment or a real opportunity, ask rather than assume.
- **Treat the meeting content as confidential client data** — it may contain financial, health, or family details beyond the meeting's stated purpose.
