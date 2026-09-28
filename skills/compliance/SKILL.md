---
name: compliance
description: Review any client-facing message or material (emails, letters, review summaries, newsletters, social posts, website copy, seminar decks, performance reports, proposals) against the FCA rules that govern UK financial advisers — the financial promotion rules and the fair, clear and not misleading standard (COBS 4), the Consumer Duty consumer understanding outcome (PRIN 2A), the pensions-specific expectations on DB transfers, drawdown, tax-free cash and consolidation, and FG24/1 for social media. Produces a pass/flag/fail markup, required disclosures, a record-keeping scratch-pad entry, and an archiving handoff reminder. Triggers on "compliance check", "/compliance", "is this compliant", "is this a financial promotion", "review this before I send it", "can I say this to a client", "check this email/post/deck". Use it whenever an adviser or paraplanner asks to check, review, or look over anything before it goes to a client or prospect — "check this before I send it", "look this over before it goes out" — even a routine note, because deciding that a message needs no changes is part of the review, not a reason to skip it.
---

# Compliance Communications Review

This is a **pre-check** against the FCA's rules for financial promotions and client communications, run **before** content goes out — the goal is to improve a draft's odds with the firm's own compliance review, not to perform that review: catch problems, suggest rewording that addresses them, and leave a record.

This skill supports advisers, it does not replace them: output is a **draft review for the firm's compliance officer (or the network's compliance team for an appointed representative)**, not a legal determination or an approval. Nothing here means the content "passed compliance" or has been approved as a financial promotion — it means the known problems were caught and fixed before a human sees it.

## Inputs

1. **The content** — pasted text, uploaded file, a draft Claude just wrote, or a draft already sitting in email or Drive. For the latter, `ToolSearch` by the system's own name — if its tools come back, search it for the draft. That search is the check that decides; `ListConnectors` (load via `ToolSearch` if not already available) explains a gap rather than establishing one, and an empty result from it means **unknown**, never "nothing is connected". If it isn't, follow the Connector Placeholder Convention — say *"This is where I'd search [system] for the draft once that connector is built"* — and degrade to asking the adviser to paste or upload it. Only use that wording when the connector genuinely isn't installed: `connected: true` with `enabledInChat: false` means it's switched off for this chat (say so, and that they can enable it here), and a missing or `null` `connected` means **unknown**, not disconnected.
2. **Context** (ask if unclear):
   - Audience: retail or professional client (assume retail unless told otherwise)? A single client, a prospect, or one-to-many (newsletter, social post, website, seminar)? — whether it is a financial promotion turns partly on this
   - Channel: email, letter, social media, website, print, presentation, video, text message or WhatsApp
   - Firm status: directly authorised, or an appointed representative of a principal or network (an AR's financial promotions must be approved by its principal, so the sign-off route changes)? Independent or restricted advice?
   - Does it mention past, simulated or future performance (including cashflow-model outputs), testimonials or reviews, ratings or awards, DB or safeguarded-benefit transfers, drawdown or retirement income, tax-free cash, pension consolidation, or tax?

## Review Workflow

Invoking `/compliance`, or handing Claude a draft to check, is already the go-ahead — begin the review, don't ask whether to start.

Work through `references/fca-compliance-checklist.md` (in this skill's folder) systematically. Summary of the passes:

**Passes 2 and 3 go to the `pensions-adviser:compliance-scan` subagent** — `Agent(pensions-adviser:compliance-scan)`. Hand it the content verbatim, the context you gathered (audience, channel, firm status, and whether performance, testimonials or reviews, ratings, DB transfers, drawdown, tax-free cash, consolidation or tax appear), and the **absolute path** to `references/fca-compliance-checklist.md` — the subagent's working directory is the session's, not this skill's, so a relative path won't resolve for it. It returns its own financial promotion determination — reached independently, from the checklist and the content, not from anything you concluded in Pass 1 — plus the flagged passages quoted verbatim with rule, severity, and reasoning, which escalation topics and disclosure categories the content triggers, and which checks came back clean. Where its determination and your Pass 1 call disagree, yours governs the review — Pass 4's markup and the disclosure language are yours to write, so the call that drives them is yours to make — but never let the difference pass unremarked: note it in the analysis file, and treat the disagreement as one more reason to escalate to the firm's compliance officer.

**Pass 4 stays with you, all of it.** The subagent finds and cites; it never rewords, never drafts disclosure language, and never redrafts. The suggested rewording column, the required-disclosure language, and the clean redraft that preserves the author's voice are the parts that need judgement about this firm and this author, and they are the reason this skill exists. Read the scan, then write the markup yourself — and check the flags rather than transcribing them: a severity you disagree with is yours to change.

**Once the scan comes back, resolve what it can't reach itself** — `compliance-scan` only has `Read`/`Grep`/`Glob`, so any check that needs a live connector is yours to dispatch, not its:

- **A testimonial or review is present.** `ToolSearch` by the CRM's own name (Salesforce, or a back office such as Intelligent Office, Xplan, Curo or Plannr — none of which has a declared connector, so only their tools coming back makes them usable); if its tools come back it is callable, which is the check that decides. `ListConnectors` (load via `ToolSearch` if needed) only explains a gap — read `enabledInChat` rather than `connected` there, and treat an empty result as **unknown**, never as "no CRM". If a CRM is usable, dispatch one `pensions-adviser:compliance-lookup` subagent per named author (lookup type `identity`) — all in a single message if there's more than one. Hand each the one system it is to query, named (the CRM whose tools came back), and the author as the content names them — asking for client vs. non-client status, relationships to other households, and anything bearing on incentives or conflicts. Fold what comes back into Pass 3's disclosure requirements below. If no CRM is connected, follow the Connector Placeholder Convention and ask the adviser who the reviewer is to the firm — never assume an author is unrelated just because nothing surfaced.
- **The scan flagged a material claim of fact as unsubstantiated (Pass 2, item 5) and it's checkable.** If a portfolio or platform system is callable and plausibly holds the comparison data — Addepar, say, or a platform such as Transact or AJ Bell whose tools came back from `ToolSearch` — dispatch one `pensions-adviser:compliance-lookup` subagent per checkable claim (lookup type `claim`) — batched into one message when there's more than one. Hand each the one system it is to query, named (the system whose tools came back), and the claim verbatim with what data would settle it. Cite what comes back (contradicts, supports, or can't determine) in the verdict table rather than only flagging that the claim needs substantiation. Check against the actual population the claim is about — a claim that consolidating "cut charges for clients in situations like hers" is checked against *comparable households*, not against the one client the piece is already about; citing that client's own number back at her own claim isn't verification. If no such system is callable, fall back to demanding substantiation as usual.

The passes, which are also what to work through by hand if the subagent is unavailable:

### Pass 1 — Scope: is it a financial promotion, and what applies?
Use the Scope Determination section of `references/fca-compliance-checklist.md`. A **financial promotion** is an invitation or inducement to engage in investment activity, communicated in the course of business (section 21 of the Financial Services and Markets Act 2000). One-to-many content that markets the firm's services, a product, an investment approach or a course of action (consolidating, transferring, accessing a pension) usually is one; so is a personalised letter that goes beyond the client's own advice and invites them to take up a product or service; so is a testimonial, review or award used to promote the firm. A personal client communication about the client's own advice — a suitability-related letter, a review summary, a reply to the client's own question — usually is not. Establish, too:

- **Audience**: retail or professional; one individual or one-to-many.
- **Firm status**: directly authorised, or an appointed representative. For an AR, the principal or network must approve financial promotions — name that sign-off route in the analysis file and the chat summary.
- **Advice status**: independent or restricted, so that any description of the service can be checked against it.
- **Pensions topics with specific rules**: DB or safeguarded-benefit transfers, drawdown and retirement income, pension consolidation, tax-free cash, pension scams and unregulated or high-risk investments, Pension Wise guidance.

Whatever the answer: the **fair, clear and not misleading** rule (COBS 4.2.1R) and the **Consumer Duty** (PRIN 2A) apply to all client communications, promotion or not.

### Pass 2 — Core standards
Flag any statement or feature that:
1. Is not fair, clear and not misleading (COBS 4.2.1R), including by omission
2. Emphasises potential benefits without a fair and prominent indication of relevant risks
3. Disguises, diminishes or obscures important items, statements or warnings
4. Would not be understood by the average member of the intended audience
5. Makes a material claim of fact the firm could not substantiate on request
6. Falls short of the Consumer Duty consumer understanding outcome — not tailored to the audience, not timely, not tested where testing is appropriate, or leaving the customer unable to make an informed decision
7. Risks foreseeable harm or relies on sludge or pressure (undue urgency, friction, framing that exploits behavioural biases, discouraging guidance)

### Pass 3 — Specific content rules
- **Past performance**: not the most prominent feature; at least five complete 12-month periods (or since inception if shorter), ending as recently as practicable; reference period and source stated; the "past performance is not a reliable indicator of future results" warning; a currency warning where relevant; gross vs net of charges made clear. **Simulated past performance** only on the checklist's conditions. **Future performance and projections**: reasonable assumptions supported by objective data, not based on simulated past performance, the "forecasts are not a reliable indicator" warning; cashflow-model outputs presented as illustrations on stated assumptions, never as promises. Any past, simulated or future performance escalates to the firm's compliance officer on its own, whatever severity it's rated.
- **DB and safeguarded-benefit transfers**: content must not promote transferring — the FCA's starting assumption is that a DB transfer is unsuitable; no "free" transfer-value analysis framed as an inducement; no contingent-charging language; the loss of guaranteed benefits stated; the requirement for appropriate independent advice above £30,000 of safeguarded benefits not misrepresented. Any DB or safeguarded-benefit transfer content escalates on its own, whatever severity it's rated.
- **Drawdown and retirement income**: balanced risk — investment risk, the risk of running out of money, the sustainability of withdrawals, income not guaranteed.
- **Tax-free cash**: framed without urging early or full access; no fiscal-event urgency.
- **Pension consolidation**: claims like "lower fees" substantiated, and balanced by the possible loss of guarantees or valuable benefits and exit charges.
- **Pension Wise / MoneyHelper**: a signpost where content concerns accessing pension savings.
- **High-risk and unregulated investments**: no promotion of restricted mass market or non-mass market investments to retail pension clients outside the FCA's rules for them; scam-risk language where content touches transfers, early access or unsolicited offers.
- **Tax statements**: tax treatment depends on individual circumstances and may change; never stated as a certainty.
- **Testimonials, reviews, ratings and awards**: genuine, representative, not misleading; any incentive disclosed (the CMA's fake-review rules under the Digital Markets, Competition and Consumers Act 2024 also apply); ratings carry provider, date, basis and whether anything was paid. A testimonial or review escalates to the firm's compliance officer on its own, whatever severity it's rated; Pass 4 says how to record that.
- **Social media (FG24/1)**: each post standalone compliant; risk warnings prominent, not behind "see more"; finfluencer or affiliate content is the firm's promotion.
- **Guarantees and promissory language**: flag words like "guaranteed", "risk-free", "safe", "can't lose", "will grow", "best", and urgency like "act now before the Budget".
- **Fees and charges**: complete — adviser, platform and fund charges, and ongoing advice charges stated clearly (the Consumer Duty price and value outcome).
- **Status disclosure**: the firm authorised and regulated by the FCA with its FRN; for an AR, the appointed-representative statement naming the principal; independent vs restricted described accurately; "the FCA does not regulate" statements where the content touches tax advice, estate planning, trusts or will writing.

**Content aimed at vulnerable customers or at older clients around retirement decisions** escalates on its own too, whatever severity it's rated — describe the audience feature that triggers it; never label any client "vulnerable".

### Pass 4 — Build the markup

Produce three things, written into the two plain-markdown files below — nothing heavier by default:

**A. Verdict table** — each flagged passage:

| # | Passage | Rule / issue | Severity (Fail / Flag / Note) | Suggested rewording |
|---|---------|--------------|-------------------------------|---------------------|

Two kinds of thing send a passage to the firm's compliance officer (or the network's compliance team for an appointed representative) before anything goes out, and they are independent: a **Fail** rating, and a **topic** — past, simulated or future performance, DB or safeguarded-benefit transfer content, a testimonial or review, or content aimed at vulnerable customers or older clients around retirement decisions — whatever severity that passage was rated (Pass 3). Say which trigger applies against each such passage, in the table and in the chat summary, so the adviser sees every reason the piece is going up rather than one escalation for the piece as a whole. A piece with a Fail *and* a testimonial carries two escalations; naming only the second reads as though the Fail could go out once the disclosure is fixed.

**B. Required disclosures** — the specific disclosure language the piece needs, positioned where it must appear. Use the checklist's disclosure library as the starting point: FCA status wording, appointed-representative wording, the past performance warning, the capital-at-risk warning ("The value of investments and any income from them can fall as well as rise and you may get back less than you invested"), the pensions access warning (tied to the normal minimum pension age), the tax warning, the DB transfer warning, the drawdown risk warning, the Pension Wise signpost, and the "not regulated by the FCA" line for tax advice, estate planning or will writing. Write the language itself, ready to paste — including when none of the specific categories is triggered and the only disclosure the redraft needs is the status line and general risk language. A sentence describing what disclosure is needed is not a disclosure; the adviser has to be able to copy this section, not act on it. Mark the section **"Adapt to your firm's approved wording"** — the firm's own approved text, where it has one, always wins.

**C. Clean redraft** — the full content rewritten so that every flagged passage is addressed, preserving the author's voice as much as possible. Describe it that way, in the files and in the chat: it *addresses the issues identified in this review*. It is not content that has been found compliant or approved as a financial promotion — nobody with the authority to make that finding has read it yet — so never call the redraft, a rewording, or the reviewed piece "compliant", "FCA-compliant" or "approved".

## Output

**Before the verdict table, ask about anything material the adviser may have context on.** An undisclosed relationship the CRM lookup turned up, an incentive given for a review, whether the firm is an AR and who its principal is, a consent question — surface each as a direct question, the same way Inputs already asks unclear context up front, rather than burying it in a wall of findings. Fold the answer into the severity and wording below before presenting the rest — don't hold the whole review hostage to one open question, but don't finalise a verdict on a material finding you haven't asked about either.

Then write two markdown files — plain `.md`, nothing heavier; a docx/pdf/Excel conversion is slower to produce and only happens if the adviser asks for one afterwards:

- **`<slug>-compliance-analysis.md`** — the verdict table (Pass 4A) and the required disclosures (Pass 4B). This is the compliance officer's working document: what was found, why, and the language that fixes it. It leaves this session as a file other people will read without the conversation around it, so it opens with one plain sentence saying what it is: a draft review prepared for the firm's compliance officer (or the network's compliance team for an appointed representative) to act on, not a legal determination and not an approval. For an AR, it also names the principal's or network's approval as the required sign-off route for any financial promotion.
- **`<slug>-compliance-redraft.md`** — the clean redraft (Pass 4C), and nothing else. No commentary, no header explaining what changed — just the redrafted content in the piece's own voice, as close to a straight "copy this and send it" artifact as the review gets.

Derive `<slug>` from the source filename when the content came from one; otherwise from the content type and today's date (e.g. `newsletter-2026-09-09`). Write both to the working folder.

**In the chat, give only a summary**, and open it by saying what this is: a draft review for the adviser's compliance officer (or network compliance team) to act on, not a determination, a sign-off, or an approval. That sentence comes first, before any verdict, because a summary that opens "Fail — don't send this" reads as a ruling, and the person with the authority to rule hasn't seen it yet; naming the compliance officer only as the place to escalate a Fail is not the same framing. Then the pass/flag/fail counts, the one or two most consequential findings in a sentence each, and the two filenames — point the adviser to the files for the rest. Say the redraft *addresses the issues identified in this review*; never that it is compliant or approved. Don't paste the verdict table, disclosure language, or redraft inline in the conversation.

Also complete, same as ever:

- **Scratch-pad entry** — appended to the compliance review scratch pad (its own file, see below), a staging note toward the firm's official records, never the records themselves — always paired with the archiving reminder that follows it.
- **Archiving reminder** — delivered inline in the chat: confirmation the sent version will be captured, plus any off-channel warning (see below).

### Record-Keeping Scratch Pad (SYSC 9 / COBS 4.11)

Every reviewed communication gets a scratch-pad entry — an internal staging note toward the firm's official records, never the records themselves. Append (or create) `compliance-review-scratchpad.md` in the working folder. If you're creating the file, the banner line comes first, above the table, so it's unmistakable to anyone who opens the file cold — the adviser, their compliance officer, or another skill:

```
Scratch pad — copy to official records

| Date | Author | Content type | Audience | Financial promotion? | Verdict | Issues found | Reviewer | Approved by (firm / principal) | Final version filed? |
```

Remind the adviser: firms must keep records of financial promotions and client communications (SYSC 9 and COBS 4.11) for the periods their own record-keeping policy sets, which vary by business type; pension transfer, conversion and opt-out material is kept **indefinitely**; and for MiFID business, relevant telephone and electronic communications must be recorded (COBS 11.8). State retention as "per firm policy; indefinite for pension transfer, conversion and opt-out material" — never invent a period. This scratch pad only tracks what's been reviewed and still needs to move to the firm's own records system — it is not itself the firm's official record, and never call it a "log" or imply otherwise when talking to the adviser.

**Never write a scratch-pad entry without immediately following it with the Archiving Handoff below, in the same turn** — the pairing is what turns "reviewed" into "copied to the records", not the entry on its own.

### Archiving Handoff

Close every review with the archiving reminder:

- Confirm the final sent version will be captured by the firm's records or archiving system (the back office document store, or a capture tool such as Smarsh, Global Relay or Proofpoint), together with the approval record — the principal's or network's approval, for an AR.
- **Off-channel warning**: if the content is going out by text, WhatsApp or personal email, warn that business communications on channels the firm doesn't capture breach its recording and record-keeping expectations, and that the FCA has taken action over this — it must go through a recorded, firm-approved channel. The adviser's stated channel decides this: when they've said it's the firm's regular recorded email, there is nothing to warn about and nothing to ask, so say the channel is fine in a clause and move on rather than restating the warning as a conditional.
- There is no archiving connector yet. The output above is **ready for archiving**, not archived — say: *"This is where I'd hand the final version off to your archiving system once that connector is built"* and tell the adviser to file it per firm procedure. Never imply this skill pushes it there automatically.

## Out of Scope (for now)

- **No compliance officer replacement.** This skill produces a draft review; it never substitutes for the firm's compliance officer's own review and sign-off, or for the principal's or network's approval of an appointed representative's financial promotions.
- **No legal determination.** This skill provides compliance-support information, not legal advice. It does not decide whether advice is suitable, and it never approves a financial promotion.
- **No automated archive push.** There is no archiving connector — the reminder above is the full extent of this skill's involvement in archiving.

## Important Notes

- **When in doubt, escalate** — anything rated Fail, anything involving past, simulated or future performance, DB or safeguarded-benefit transfers, testimonials or reviews, or content aimed at vulnerable customers or older clients around retirement decisions should go to the firm's compliance officer (or the network's compliance team) before sending.
- Be strict but practical: don't flag ordinary pleasantries or factual scheduling emails; do flag anything that characterises results, markets, retirement outcomes, or what a client should do with their pension.
- Never claim content "is FCA-compliant" or "approved", and never call a redraft or a rewording "compliant" — say it "addresses the issues identified in this review." The Output section above states this where the files and the chat summary are defined; this line is the reminder, not the only place it lives.
- Rules change, and `references/fca-compliance-checklist.md` is a static snapshot drafted September 2026, not a live firm-rules feed — that's acceptable without a firm-rules connector, but never imply it's automatically kept current. If the session has web access and the content is high-stakes, verify current requirements against the FCA Handbook and FCA website guidance (for example FG24/1 on social media, the Consumer Duty materials, and the FCA's retirement income and pension transfer publications) before finalising.
- Treat the content under review as confidential; share only what's needed to complete the review.
- This skill reviews client communications and marketing drafts — letters, review summaries, newsletters, social posts, website copy, seminar decks — regardless of who or what produced them. It is not an outbound email wrapper and does not attach disclosures to client correspondence on send. A common flow: pull discussion-topic insights → draft an educational newsletter → run it through this skill before sending.
