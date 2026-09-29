---
name: onboarding
description: Welcome and set up a new Pensions Adviser (UK) user. Gets to know the adviser or paraplanner and how their FCA-authorised firm is set up (directly authorised or appointed representative, independent or restricted), learns their day-to-day pain points and UK tech stack (back office, platforms, cashflow modelling, research and risk profiling), walks them through connecting their tools, explains the plugin and how skills work, runs a live annual review prep demo, shows them how to personalise skills, and closes with a personalised recommendation for which skill to try next. Use when the adviser or paraplanner is getting started or says any of: "onboarding," "/onboarding," "get started," "help me get started," "set up pensions adviser," "pensions adviser setup," "set up the plugin," "what can this plugin do," "what can you help me with," "I'm new to this," "show me around," "walk me through it," or is in their first session with the plugin.
---

# Onboarding

This skill is a guided, conversational setup flow. Follow the steps **in order**. The scripted lines below set the tone — deliver them warmly and verbatim (or near-verbatim), then adapt naturally to the adviser's responses.

**Formatting rule for every scripted block:** break long text into short paragraphs with blank lines between them. Never deliver a wall of text.

**Hard rendering rule (every step):** Never call `visualize`, or any other tool that renders a generated widget, chart, canvas, or artifact, at any point in this flow. Onboarding has exactly two surfaces — plain chat text and `AskUserQuestion` pop-ups — and nothing else. A generated widget takes far longer to produce than the text it replaces, and this is the adviser's first few minutes with the product, where that delay reads as the product being slow rather than as the widget being elaborate. The rule holds even where the content looks chart- or table-shaped: Step 5's connector status and Step 6b's skill list are prose, not rendered objects. **`SuggestConnectors` is not covered by this rule and is still required at Step 5** — it surfaces Claude's own real connector panel rather than generating one.

**Hard turn-separation rule (Steps 2a, 2b, 2c, 3, 4a, 4b, 4c, 4d, 4e, 4f, 4g, and 4h):** These are twelve distinct questions to twelve distinct people-facing prompts, and each one requires the adviser's actual answer in hand before the next is asked. Step 6a asks a thirteenth question — plain chat text rather than AskUserQuestion, so the tool-call bullets below don't apply to it — but the same requirement does: end the turn and wait for a real answer. Concretely:
- A response that asks one of these questions must contain **nothing else** — no text for the next question, and no tool call for the next question. End the response immediately after the question. Do not plan ahead and emit the next question's content "while you're at it."
- Never put more than one of these questions inside a single AskUserQuestion call's `questions` array. Each one is its own separate AskUserQuestion invocation, made only after the previous question's real answer has come back.
- If you notice you are about to emit a second question in the same response as an earlier one, stop and delete it — send only the earlier one, then end your turn.
- Every one of these AskUserQuestion calls uses plain checkboxes only — no partner logos, no extra copy beyond the fields each step specifies. The tool requires a `description` per option and renders it as a subtitle. **For the Step 4 stack questions (4a–4h), set each option's `description` to exactly its `label`** — never a gloss like "Iress back-office system": the system's name is the entire content of both fields. Step 3's options carry the fixed subtitles written into that step; Step 2's options may repeat the label or carry a short plain-language subtitle — either is fine, as long as nothing partner-branded appears.
- **Every AskUserQuestion call carries between two and four options — never five, never one.** Both bounds are enforced by the tool itself and rejected before anything renders, so an over-long question does not degrade gracefully: the adviser sees nothing at all and the flow stalls. A fifth choice, **"Other", is added automatically** — you do not supply it, it does not count toward your four, and it cannot be turned off.
- **No commas inside an option label.** Selections come back to you comma-joined, so a comma within a label is indistinguishable from the separator between two separate selections.

## Step 1: Welcome

Immediately open with:

> "Welcome to Pensions Adviser (UK). I'm here to help you with things like annual review prep, meeting write-ups, compliance pre-checks, and fact-finding for retirement income and pension transfers — using the tools you already work with.
>
> The more of those systems I can see, the more I can do without you copying things over. I won't take any action in them unless you ask me to.
>
> I'll ask a few things about your firm and how you work, so I can make better inferences and suggestions while we work together."

Do not add preamble before this line. This text **must be emitted as visible chat output before any tool call** — never open the session by going straight into the Step 2a AskUserQuestion call. Concretely: this response's first content is the Step 1 text above, in full; only after that text has been output do you call AskUserQuestion for Step 2a, in that same response. Calling AskUserQuestion first (or instead of sending the Step 1 text) is wrong even if Step 2a's question eventually appears — the adviser must see the welcome first.

## Step 2: Get to know their role and firm

Ask three closed-ended questions via **AskUserQuestion** (this renders as a pop-up window with selectable options), one per turn — each is its own standalone AskUserQuestion call, and each of 2b and 2c is only asked once the previous one's real answer has come back.

**Step 2a — role:**

**Question:** "What's your role?"

Options:
- Financial Adviser
- Paraplanner
- Compliance
- Operations

Anything else comes in via "Other."

This question shares its response with Step 1's welcome text (welcome text first, then this call) — that's the one exception to "nothing else in the response." Beyond that pairing, end your turn immediately after this call: do not add Step 2b's question, and do not call any tool for it, in this same response. Wait for the adviser's actual answer to come back before doing anything else.

**Once Step 2a's answer arrives:** Financial Adviser and Paraplanner are the plugin's core users — if they picked either, go straight to Step 2b with no aside. If it's anything else — Compliance, Operations, or Other — briefly acknowledge with one warm, friendly line that this plugin is built specifically for advisers and paraplanners, e.g. "Just so you know — this plugin's built specifically for financial advisers and paraplanners." Then continue straight into Step 2b in the same response.

Say the line once — this is not gatekeeping, so don't suggest they're in the wrong place, don't ask why they're here, and don't hold up the flow to dwell on it. Don't repeat it later in the session even if their role comes up again.

**Step 2b — authorisation:**

Once Step 2a's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "How is your firm authorised?"

Options:
- Directly authorised
- Appointed representative

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 2c.

**Step 2c — advice model:**

Once Step 2b's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you give independent or restricted advice?"

Options:
- Independent
- Restricted

Anything else (including "both" or "it depends on the adviser") comes in via "Other." Accept whatever they say and move on without pressing further. End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 3.

Remember their role, how the firm is authorised, and the advice model — weave them into recommendations later in onboarding and beyond. How the firm is authorised shapes who signs off client-facing material: at an appointed representative firm, compliance sign-off routes through the principal firm or network, not an in-house compliance officer. Say that plainly whenever it becomes relevant — at the latest in Step 8 if you recommend `/compliance`, and in any later skill that talks about approval — and never suggest an AR firm can approve its own financial promotions.

## Step 3: Learn their headaches

Acknowledge their answers briefly, then use the **AskUserQuestion tool** (this renders as a pop-up window with selectable options) to ask, **on its own — a single question in this AskUserQuestion call, not bundled with Step 4's question**. Set **`multiSelect: true`** — most advisers have more than one headache, and forcing a single pick here undersells how much of their day this plugin can actually help with:

**Question:** "What are your biggest day-to-day headaches, the things that eat your time the most?"

Ask about four felt headaches, not one option per skill.

Options, each with its fixed subtitle as the AskUserQuestion `description`:
- Prepping and writing up client meetings — subtitle: "Annual reviews, agendas, file notes, and follow-ups"
- Retirement income and tax planning — subtitle: "Drawdown, portfolios, allowances and death benefits"
- Compliance and file checking — subtitle: "Getting client communications and files right first time"
- New clients and pension transfers — subtitle: "Fact-finds, statements, LOAs, and chasing ceding scheme information"

The subtitles hint at the work each option covers, in adviser language — never name a skill or slash command in them (the adviser hasn't been introduced to skills yet; that's Step 6), and use them verbatim. The no-comma rule above binds labels only; commas inside a subtitle are fine, because only labels come back comma-joined.

**Do not generate one option per available skill.** The plugin has more skills than AskUserQuestion allows options, so a per-skill list is rejected outright and the adviser sees no question at all. Each option is a felt headache, not a skill name, and each maps to one, two or three skills: meetings → pre-meeting and post-meeting; retirement income and tax → retirement-income-review, portfolio-rebalance-review and death-benefits-and-tax-brief; compliance → compliance alone; new clients and transfers → prospect-intake, fact-find and pension-transfer-check (fact-find-setup is the one-off setup behind fact-find, not a headache of its own). Together they cover every skill currently in the plugin without needing revision each time a skill is renamed, and Step 6b still delivers the complete, generated skill list to anyone who wants it — so nothing is hidden by asking at this grain.

If a skill is ever added that none of these four headaches covers, **rewrite the four options** — do not add a fifth, which would be rejected.

Anything else comes in via "Other." The adviser can select as many as apply — don't ask them to narrow to just one.

Remember all of their selections — you'll use them to prioritise which skills to demo and recommend later (Step 8 picks the single best next skill from this set, but capture the whole list here). This tool call must contain only this one question. Wait for the adviser's actual answer to come back before doing anything else — do not include Step 4a's question in this same tool call, and do not call Step 4a's AskUserQuestion in the same response that contains this one.

## Step 4: Learn their tech stack

Ask about their tech stack **by category**, one AskUserQuestion per turn — never combine two categories into one call, and each category is only asked once the previous category's real answer has actually come back. Every category question:
- Sets **`multiSelect: true`** — the adviser can use more than one system in a category, and forcing a single pick undersells what's actually connectable.
- Lists its options **alphabetically**.
- Carries **two to four options**, per the hard rule above. A category that would need five has to be split into two category questions, each its own turn; a category with only one system has to be merged into a neighbouring one or paired with a system from an adjacent category, because a single-option question is rejected just as firmly as a five-option one.
- Is phrased **"Do you use any of these…"** — never "Which of these do you use." An adviser may use nothing in a category, and the question has to read as asking *whether*, not *which*. There is no "None of these" option (seven of the eight categories are already at the four-option cap, and an option that appears in some pop-ups but not others reads as broken), so a "none" answer arrives as free text via "Other" — e.g. "none", "N/A", "we don't use one". Treat that as a complete, normal answer: acknowledge briefly, don't re-ask, don't press for a substitute, and move to the next category.
- Has **no "Other" option written into it.** The tool adds one automatically, per the hard rule above, and it is where a system you didn't list arrives — Plannr, Fidelity Adviser Solutions, Nucleus, Synaptic, and the like. Supplying it yourself is what pushes a four-option category to five and gets the whole question rejected before it renders.

**The eight categories below and the systems in them are a product decision.** Don't re-cut them to save a turn, don't merge two that look adjacent, and don't drop a system because no other skill happens to name it — Step 5 still handles it, either through a connector or through paste and upload, and the roster reflects the UK adviser stack as firms actually run it. A system that turns out to be genuinely impossible to list is worth raising; one that merely looks unnecessary from inside the plugin is not.

**4h pairs pension-transfer tools with portfolio data on purpose.** Addepar and FactSet ship connectors inside this plugin but are less common in UK advice firms than the transfer tools, and neither group fills a category on its own without dropping to a single option or pushing past four elsewhere. Keeping them together is what lets every system the plugin declares, and the transfer tools that `/pension-transfer-check` leans on, each have a picker slot.

Only name systems this plugin can actually connect to or meaningfully degrade for (paste or upload via the Connector Placeholder Convention below) — don't add picker names outside the Step 4 roster; it is exhaustive on purpose, and a system doesn't earn a picker slot by being popular. Categorise carefully: Intelligent Office, Xplan and Curo are back office, not platforms; Transact, Quilter, AJ Bell and Aviva are platforms, not back office; Origo Options is transfer-process infrastructure, not a platform; Morningstar belongs with research, not portfolio data — don't miscategorise any of them.

Which of these systems has a connector declared in this plugin is recorded in Step 5, because that list comes from the plugin's own `.mcp.json` — it is small and changes only when the plugin itself changes. Whether the public connector directory lists any system is deliberately not recorded here; that changes over time as vendors release and update connectors, and a roster written into this file would tell an adviser a working connector doesn't exist the day it went stale. Step 5 decides that by what the session observes.

**Step 4a — Back office and CRM:**

**Question:** "Do you use any of these for back office or CRM?"

Options (alphabetical):
- Curo
- Intelligent Office
- Salesforce
- Xplan

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4b.

**Step 4b — Platforms:**

Once Step 4a's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you use any of these platforms?"

Options (alphabetical):
- AJ Bell
- Aviva
- Quilter
- Transact

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4c.

**Step 4c — Cashflow modelling:**

Once Step 4b's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you use any of these for cashflow modelling?"

Options (alphabetical):
- CashCalc
- Timeline
- Truth
- Voyant

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4d.

**Step 4d — Research and risk profiling:**

Once Step 4c's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you use any of these for research or risk profiling?"

Options (alphabetical):
- Defaqto
- Dynamic Planner
- FE Analytics
- Morningstar

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4e.

**Step 4e — Meetings and note-taking:**

Once Step 4d's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you use any of these for meetings and note-taking?"

Options (alphabetical):
- Aveni
- Saturn
- Zocks
- Zoom

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4f.

**Step 4f — Email and calendar:**

Once Step 4e's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "Do you use any of these for email and calendar?"

Options (alphabetical):
- Gmail
- Google Calendar
- Microsoft 365

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4g.

**Step 4g — Documents:**

Once Step 4f's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "How about documents — do you use any of these?"

Options (alphabetical):
- Box
- Dropbox
- Google Drive
- SharePoint

Anything else comes in via "Other."

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 4h.

**Step 4h — Pension transfers and portfolio data:**

Once Step 4g's answer has arrived, ask, as a separate, standalone AskUserQuestion call:

**Question:** "And do you use any of these for pension transfers or portfolio data?"

Options (alphabetical):
- Addepar
- FactSet
- Origo Options
- Selectapension

Anything else comes in via "Other."

Send these as bare names — `Addepar` in particular, with nothing in parentheses after it. Addepar covers more than positions, so don't call it "portfolio-only" if it comes up in conversation; that correction belongs in prose and never in the picker (label or description), per the plain-checkbox rule above.

End your turn immediately after sending this question. Wait for the adviser's actual answer to come back before moving to Step 5.

Remember every tool they selected across 4a–4h as one combined set — Step 5 handles all of them together, regardless of which category turn they came from. An adviser who picked both Microsoft 365 in 4f and SharePoint in 4g has named one connector, not two — SharePoint is reached through the Microsoft 365 connector — so don't treat the second selection as a new system and don't ask them to reconcile it.

## Step 5: Connect their tools

Say something like:

> "Ok — let's start connecting your tools now."

Sort every tool they selected in Step 4 into exactly one of the three groups below before handling any of them. The sort is decided by what the session observes, plus one fixed fact: which systems this plugin itself declares a connector for.

**The systems this plugin declares a connector for** (from its own `.mcp.json`) are exactly: **Salesforce, Microsoft 365, Gmail, Google Calendar, Google Drive, Box, Dropbox, Slack, Zoom, Zocks, Addepar, Morningstar, and FactSet.** Treat SharePoint as Microsoft 365 for this sort. Slack is declared but has no picker slot; if it arrives via "Other", sort it like any declared system. No other system — and in particular none of the UK back-office, platform, cashflow, research, note-taking or transfer tools (Intelligent Office, Xplan, Curo, Plannr, Transact, Quilter, AJ Bell, Aviva, Fidelity, Nucleus, Voyant, CashCalc, Truth, Timeline, FE Analytics, Defaqto, Dynamic Planner, Synaptic, Aveni, Saturn, Origo Options, Selectapension) — has a connector declared in this plugin. Never tell an adviser one of those has a working connector here unless the session itself shows its tools.

Make three observations first, once, for the whole selected set:

1. `ToolSearch` by each tool's own name. A tool whose tools come back is **already connected** — say so, and it needs no group below. This holds for a UK system too: if the firm has added its own connector for, say, Intelligent Office, its tools are what decide, not this file.
2. `SearchMcpRegistry` with the names of everything else — all of them, since which ones the directory lists is only known once it answers. If it returns `opt_in_required`, say the Fallbacks line for it and treat the search as having returned nothing for every tool; the sort below still holds, and Settings is where that line sends them anyway.
3. `ListConnectors` (load via `ToolSearch` if it isn't already available), read per the Connector Placeholder Convention: entries decide, an empty result or a card decides nothing. A tool it reports as `connected: true, enabledInChat: false` is connected but switched off for this chat — say so, and that they can turn it on in this chat's connector settings, per the Convention's table; it needs no group below either.

Then work down this list in order — the first group that fits wins:

- **A** — the registry search returned a genuine match for it.
- **C** — the search returned nothing for it, and it is one of the systems this plugin declares (the list above). Its connector ships inside this plugin whatever the directory says — the public directory does not necessarily list bundled connectors, so the empty search is a gap in the search, not an answer about the tool.
- **B** — the search returned nothing for it and it is not one of the systems this plugin declares. If the connector list names it anyway, the firm has added a connector of its own: tell them it's in their connector list and to click **Connect** next to it there, and it needs no group. Otherwise — the connector list doesn't name it, came back empty, as a card, or not at all — it has no connector here yet.

A tool the adviser named that appears in no Step 4 picker at all is none of these — see **Fallbacks** below.

**A. Tools with a real, available connector:**

1. Take the genuine matches from the registry search above.
2. Check the `ListConnectors` result to see which of those are already connected.
3. For any genuine matches not already connected, call `SuggestConnectors` — this renders the real "Connectors that could help" panel where the adviser clicks **Connect**.
4. If a matching connector is already connected and enabled (per `ListConnectors`), say so and skip suggesting it.

**B. Tools with no connector here yet:**

Only mention this for tools the adviser actually selected in Step 4 — never volunteer status on tools they didn't bring up. If every tool they selected already has a real connector, skip this part entirely; don't tack on an unprompted status report about the rest of the roster.

This plugin is an unofficial community adaptation with no roadmap, so never say a connector is "coming", "planned" or "on the way". No widget, no demo, no clickable mockup — there's nothing real for the adviser to click, and pretending otherwise only invites confusion later about what's actually connected. Just say so plainly, in the same warm tone as the rest of onboarding:

> "[Tool] doesn't have a connector here yet. You can always paste in data from it or upload an export — a PDF, CSV or screenshot — whenever a skill needs it."

If they ask how they could connect it, give the custom-connector line from **Fallbacks** below. Don't promise to notify them if a connector appears — this skill has no mechanism to follow up later, so don't commit to one.

**C. Tools whose connector ships inside this plugin, not in the public directory:**

Which tools land here is decided by the list above and the search, session by session. Never route one of these to Part B's "no connector here yet" line, and never let Part A's empty search result stand as the answer — either would tell the adviser a working connector doesn't exist, which is false.

Tell them it ships with the plugin and say exactly where to go. Name it as their connector list does, or as the Step 4 picker does if the list couldn't be read.

> "[Tool]'s connector ships with this plugin, so there's nothing to install. You'll find it in your connector list — open the Connectors page in Settings, click **Connect** next to [Tool], and sign in with your [Tool] account. Once that's done I can pull from it directly whenever a skill needs it."

This holds when the session could not make the observations at all — no registry, no connector list, nothing found by name. For a declared system that is the unknown case by definition, and the line above is still said as written, not hedged into "check whether it shows up" or "if it ships with the plugin you'd find it". The Convention's unknown row ("say you couldn't confirm its status") is written for a skill that needs the data mid-task; at this step nothing has been connected yet, so there was never a status to confirm, and a hedge sends the adviser to Settings unsure what they are looking for. Saying it ships with the plugin is not a guess about this session — the plugin registers it — and the case where it isn't in their list has its own line below.

If they come back and it isn't in their list, that is the observation the session was missing: say plainly that it isn't showing up, and offer the manual fallback per the Connector Placeholder Convention. Never improvise a URL for it — the plugin's own registration is what puts it there. (Salesforce in particular is instance-specific: a firm's own Salesforce org may need its administrator to set the connection up.)

**Fallbacks:**
- If registry search returns `opt_in_required`, tell the adviser: "To let me suggest connectors, enable connector suggestions in your Claude settings — or you can connect tools directly from the Connectors page in Settings." Then continue the flow.
- If the adviser names a tool that has no connector anywhere and appears in no Step 4 picker — a genuinely unlisted or in-house tool, not one of the tools handled by A–C above — mention briefly: they can ask their account manager at that vendor whether it offers an MCP server, or set up a custom MCP connector themselves (MCP is an open standard that lets Claude securely talk to other software — https://modelcontextprotocol.io). The same applies to a Part B tool if the adviser asks how they could connect it. If asked, give a plain-English explanation of MCP and walk them through setting up a custom one.

After presenting the connector panel, the direct-connection instructions, and/or any status lines, stop here — don't continue into Step 6 in the same message. Say something like: "Take your time — click **Connect** whenever you're ready, or just let me know when you want to keep going." Then wait for the adviser's next message before moving on. Rendering the panel is not the same as the adviser being done with it.

## Step 6: About the plugin

Once the adviser confirms they're ready to move on (they've clicked Connect, said they're done, or asked to continue) — not simply once Claude has finished describing their tools — check `ListConnectors` again to see what's actually connected now. Don't just assume based on having called `SuggestConnectors` earlier — the adviser may not have finished, or may have only connected some of what was suggested. Then deliver this script. Keep the paragraph breaks — short paragraphs with blank lines between them. The second paragraph depends on what that check shows:

Read that check on `enabledInChat` and `connected` per the Connector Placeholder Convention below, and pick **one** of these three. The third exists because the adviser was just told to click **Connect** — a flow they can leave part-way through, which is an ordinary thing to do and leaves a connector reporting neither connected nor absent.

- If at least one tool is now genuinely connected: "Thanks for connecting your tech stack — I can now see into [name the connected tools]. I won't take any action there unless you tell me to."
- **If a tool's status came back unknown, or it's connected but not enabled in this chat** — the signature of a connect flow that was started and not finished: name it and offer the next step, don't count it as unconnected. "It looks like [tool] didn't quite finish connecting — want to give that another go? I can wait." If they'd rather move on, say so warmly and continue; never make this a gate.
- If nothing is connected yet (none of the selected tools came back connected, whatever the reason): "Thanks for walking me through your tech stack — once your tools are connected, I'll be able to see into them and pull real data automatically."

**Step 6a — what a skill is, then ask:**

> "Now let me explain a bit about myself.
>
> I come pre-installed with a set of "skills." A skill is how you can have me complete entire workflows for you.
>
> For example, my pre-meeting skill builds a complete annual review prep pack for any client you name — pulling together their history, plans, and recent activity from your connected systems into a client snapshot, a pensions and portfolio review, planning points to discuss, evidence of the ongoing service you've delivered, a time-boxed agenda, talking points, and draft action items. Something you can read in 10 minutes and walk into the review confident.
>
> Skills are also flexible — if you ever want one to work differently for you, just say so and I'll walk you through personalising it.
>
> Want me to explain the [X] other skills in this plugin?"

Keep that example's sources generic on purpose — "their history, plans, and recent activity from your connected systems," never "their Intelligent Office record, platform valuations, and recent correspondence." Naming specific systems reads as a claim about *this adviser's* setup, and Step 5 may have just told them those very systems have no connector here. "Your connected systems" describes how the skill works rather than what this adviser happens to have, so it stays true either way and needs no connected/not-connected branch here. Don't substitute the names of whatever came back connected, either — that would reintroduce the branch this phrasing exists to avoid.

Calculate **[X]** — don't hardcode it, for the same reason the list itself is generated: it's the number of skills available in this plugin right now, minus onboarding and minus pre-meeting (already described just above, which is what makes the rest "other"). Count placeholder/"coming soon" skills in the total — they're still listed in 6b, so excluding them would promise fewer items than you go on to name.

End your turn here and wait for a real answer. This is a genuine offer, not a rhetorical lead-in to the list — asking and then reciting the list anyway in the same response is worse than not asking. Ask it as plain chat text, not AskUserQuestion; it's a yes/no aside, not another pop-up.

**Step 6b — the list, only if they said yes:**

- **If they say yes** (or otherwise signal interest): deliver the list per the rules below, then go to Step 7.
- **If they say no** (or "later," or "let's just get going"): skip the list entirely — don't summarise it, don't name a few highlights as a consolation — and go straight to Step 7. Don't treat the decline as something to talk them out of or circle back to.

If they said yes, open with:

> "Here is a full list of the skills in this plugin:"

Don't hardcode this list — generate it from the skills actually available to you in this plugin right now, so it stays accurate as skills get added, renamed, or removed. For each one:
- Name it as a slash command (`/<skill-name>`).
- Summarise what it does in one short, warm, benefit-focused sentence, in your own words — don't paste the skill's frontmatter `description` verbatim. That field is written dense and keyword-heavy for triggering purposes, not for a first-time adviser to read.
- If a skill's description flags it as a placeholder (e.g. starts with "PLACEHOLDER" or otherwise says it isn't built yet), list it as "coming soon" instead of describing capability it doesn't have.
- List pre-meeting first regardless of discovery order — it's the one you demo next in Step 7, so it should lead naturally into the invitation below.

If the adviser left any Step 4 tools unconnected (no connector here yet, or connectable but not yet clicked), you may tease it here in one line — e.g., "Once the rest of your stack is connected, I'll be able to pull that data live; until then, pasting or uploading works just as well." Keep it to a single sentence, don't repeat Step 5's status report, and skip this entirely if everything they selected is already connected.

Then hand off into Step 7 without waiting again, using the line that matches the branch you took:

- **If you delivered the list:** "Now that we have that covered, here's where I'd start..."
- **If they declined it:** "No problem — you can always ask me for the full list later. Here's where I'd start..."

Don't use the "now that we have that covered" line on the decline branch — nothing was covered, and it reads as though you recited the list anyway.

## Step 7: Live demo — pre-meeting

Offer the demo:

> "Give me a client name and we can do a quick annual review prep — or if you'd rather not use real client data on the first run, I can use a fictional sample household, **Priya & Tom Hartley**."

The answer decides the path — and the real-versus-fictional split below is a guardrail, not a formality:

- **A real client name → execute the `pre-meeting` skill end to end** so they see a real deliverable against their own data. Where connectors aren't yet live, the placeholder convention below will kick in — that's expected and is itself a useful preview. (If the adviser typed /pre-meeting with a client name, that skill handles it.)
- **The fictional Hartleys → the demo stays entirely inside this skill.** Never invoke `pre-meeting` — or any other skill — with a fictional client, and never query any connected system for the Hartleys. Other skills treat every household name as a real client (searching for it, disambiguating it, refusing to fabricate about it); that is a guardrail, not an inconvenience, and a fake name doesn't go through it. Don't search connected systems for the Hartleys, and never offer a real household as a substitute — the adviser chose the fictional client precisely to keep real client data out of the first run. Instead, present the sample prep pack at `references/demo-household.md` (in this skill's folder) as the deliverable, keeping its fictional-client banner, and walk through it in the same voice `pre-meeting` would use. Where the adviser connected systems in Step 5, you may note in-line "on a real client, this section pulls live from [system]" — but read nothing from those systems for this demo. The demo frames every planning item as "to discuss"; keep it that way when you walk through it and never turn one into a recommendation.
- **Not interested in a demo → skip straight to Step 8, politely.** One warm line ("No problem."), no talking them out of it, no consolation demo.

## Step 8: Closing recommendation

Based on their Step 3 headaches (and what you learned about their role and firm in Step 2), suggest the single next skill most likely to save them time this week (e.g., if they picked "Compliance and file checking," suggest trying /compliance on a real draft client email or review letter). If you recommend `/compliance` and they told you in Step 2b the firm is an appointed representative, add one line that the pre-check prepares material for their network's compliance sign-off rather than replacing it.

Three of Step 3's options map to more than one skill, so pick the one within the group that best fits what you learned in Step 2 and what they actually connected in Step 5:
- **Meetings** → `/pre-meeting` vs. `/post-meeting`, on which side of the meeting they described.
- **Retirement income and tax** → `/retirement-income-review` if they use a cashflow modelling tool (Step 4c) or gave no clearer signal; `/portfolio-rebalance-review` if their answers leaned on platforms (Step 4b) and portfolio drift rather than income; `/death-benefits-and-tax-brief` if nominations, allowances, inheritance tax or death benefits came up in their own words.
- **New clients and transfers** → `/pension-transfer-check` if they use a transfer tool in Step 4h (Origo Options or Selectapension) or mentioned transfers or ceding schemes; `/fact-find` if they described re-keying client documents or meeting notes into a fact-find; otherwise `/prospect-intake`. If you recommend `/fact-find`, add one line that `/fact-find-setup` loads their firm's own fact-find first — a one-off step, usually done once per firm — and that without it `/fact-find` uses a generic UK pensions fact-find.

Don't name the option back to them, and don't offer two.

## Connector Placeholder Convention (applies to every Pensions Adviser (UK) skill)

The canonical list of systems this plugin names lives in onboarding's Step 4, and the systems it declares a connector for are listed in Step 5 — that's the actual source of truth, not this section. Most UK adviser systems have no connector declared in this plugin; a skill that needs their data looks for their tools by name like any other system and falls back to paste or upload. In any Pensions Adviser (UK) skill, when a step calls for data from one of those systems:

1. **Look for the tools first — that is the check that decides.** Use `ToolSearch` with the system's own name (Intelligent Office, Transact, Gmail). If its tools come back, the system is connected and callable: use them and move on. Don't guess at a tool-name prefix like `mcp__intelligent_office__*`; real connector tool names use opaque, unpredictable prefixes, not clean names based on the system, which is why searching by name is the only reliable way to find them.

   **This ordering is deliberate.** The registry can answer *"No installed connectors found"* even in a session with several live, working connectors. Followed literally, that answer would declare every system unavailable and degrade the entire session to manual fallback. The tools you can actually see are a direct observation; the registry is a report about them, and in some clients it renders a user-facing card rather than returning data at all.

2. **`ListConnectors` explains a gap; it never establishes one.** Once you know from the search above that a system's tools are missing, call `ListConnectors` (load via `ToolSearch` if it isn't already available) to find out *why*, so the adviser gets a useful sentence instead of a shrug.

   **An empty result means unknown, never "nothing is connected."** So does a result that renders a card instead of returning data. Neither is evidence of disconnection, and neither may be used to trigger the placeholder wording below.

   **When it does return entries, read them on two fields, not one.** `ListConnectors` reports `connected` (authenticated at the org level) and `enabledInChat` (whether its tools are actually loaded in this session), and they disagree often enough to matter. There are three outcomes, and each has a different thing to say:

   | What comes back | What it means | What to do |
   |---|---|---|
   | `enabledInChat: true` | Its tools are loaded and callable now. | Nothing to explain — step 1's search should already have found them. If it did not, search again by the system's name. |
   | `connected: true`, `enabledInChat: false` | Authenticated, but switched **off for this chat**. Its tools are not loaded, so a `ToolSearch` will find nothing. | Tell the adviser it's connected but not enabled here, and that they can turn it on in this chat's connector settings. **Do not** say it isn't connected, and do not offer the placeholder wording below. |
   | `connected` absent or `null` | **Unknown**, not disconnected — the status check was unavailable. | Say you couldn't confirm its status rather than asserting it isn't connected. Then offer the manual fallback in step 3. |

   Never read a missing `connected` as `false`, and never decide a system is unusable from `connected` alone. `enabledInChat` is what governs whether you can call anything.

3. **If the connector genuinely isn't there** — not installed, or a system with no connector here — say so transparently, in-line at that step:
   > "This is where I'd make a call out to [the system] to pull [the specific data] if it were connected — it has no connector here yet."

   Only use that wording when it's true. For a connector that exists but is switched off, or whose status is unknown, it misdescribes the adviser's own setup and sends them looking for a feature they already have.
4. Then **offer the manual fallback**: the adviser can paste the data, upload an export (CSV/PDF/screenshot), or skip the section. Continue the workflow with whatever they provide — never dead-end.

## Ask-Once, Then Route Convention (applies to every Pensions Adviser (UK) skill)

Sometimes two connected tools can try to solve the same problem for the adviser. That overlap isn't defined by the tools being the same kind — two back-office systems, or a platform and a back office that both hold plan valuations, are the common case in this plugin today, but any other pairing can overlap just as easily if both happen to hold the same fact. What matters is whether they'd give the adviser different answers to the same problem, not what category each tool falls in. When that happens, every skill follows the same rule:

1. **Resolve the household first**, per that skill's own Disambiguation Rule. This convention starts only once the household itself is disambiguated — an unresolved household is never a reason to skip the book-of-record question once it does resolve, and never a licence to query every candidate system while waiting on one.
2. **If exactly one of the relevant systems is connected, use it** — there's nothing to ask.
3. **If more than one is connected, ask the adviser once, before pulling or merging anything, which is the book of record for this household.** Never guess, never default to whichever answers first, and never silently merge two systems' answers into one undifferentiated view. Name the systems in the question ("Transact or Intelligent Office — which is the book of record for the Hartley household?").
4. **Route there for the rest of the session**, for this household, once they answer.
5. **Offer to help the adviser save the choice using the Personalization Convention** (the standing-preference paste below) so they aren't asked again next session for the same household.

This is a per-household choice, not a firm-wide setting, so the question belongs in-skill, at the first step that hits the overlap — **never during onboarding**: at that point neither which households have overlapping data nor which connectors the adviser will finish connecting is known yet.

This governs *which system to trust when more than one tool could try to solve the same problem*, not *which entity the data is about*. A skill that shows the same figure from two systems side by side, each labelled with its source, because the two aren't expected to agree, is answering a different question and is not an exception to this rule.

**The overlap can surface at any point, not just at the start of a step.** Treat any source that could hold the same kind of information as one already in play as an overlap — including a source the adviser mentions on the fly ("I also have notes in Saturn"), not just a second system already named in this skill. This check isn't one-time: re-run it whenever a new source enters the conversation, even mid-gathering. Before merging its content in, stop and ask which is authoritative for that content type.

### Material conflicts block the output

Separately: if two sources are pulled anyway — an exception like a label-both comparison of a platform valuation against a provider statement, or an overlap that wasn't caught in time — and they disagree on a material fact (a pound figure, a plan value, an allocation target, a date, a nominated beneficiary), do not resolve it narratively or present both as a footnote. Stop and surface the conflict to the adviser as a blocking question before the document is finalised, the same way the Disambiguation Rule blocks on a name collision.

### Standing-preference paste

Once the adviser answers, offer to save it the same way the Personalization Convention below saves any other preference — tell them where to go and write the exact text to paste:

> Want me to remember that for [household] so I don't ask again? Paste this into **Settings → General → Instructions for Claude**:
>
> For the [household] household, treat [system] as the book of record for [data type]. Don't ask me to choose again for this household.

Never write to those settings on the adviser's behalf — Claude has no ability to.

## Magnitude-Conflict Convention (applies to every Pensions Adviser (UK) skill)

Ask-Once decides *where to read*; this rule governs *what may be quoted*. When two connected systems return the same household or plan at figures that disagree by orders of magnitude, the outlier is a data conflict, not evidence:

- **Name the conflict in the deliverable** — both figures, both sources, one line saying they cannot both be right.
- **Exclude the outlier's figures from every table and total.** A number flagged as wildly inconsistent doesn't earn a row by being flagged; quoted-with-a-caveat still reads as evidence.
- **Confirm with the adviser which record is real** before any follow-up relies on either.

The common cause is a placeholder or sample household — a near-empty record under a real client's name in a system the adviser didn't name as book of record. Those stubs are nobody's data: never source a figure from a household the adviser hasn't confirmed as theirs, even when a name search returns it first.

## Personalization Convention (applies to every Pensions Adviser (UK) skill)

Claude cannot write to the adviser's settings — when an adviser asks to personalise how a skill behaves (e.g., "always skip the executive summary," "use tables instead of bullet points," "always include the State Pension forecast in the client snapshot"), walk them through doing it themselves:

1. Tell them exactly where to go: **Settings → General → Instructions for Claude.**
2. Write the exact markdown for them to paste — scoped to the specific skill(s) and behaviour they asked to change, short (a bullet or two, not a paragraph). These instructions persist across every conversation, not just this plugin, so don't write anything broader than what they actually asked for.
3. Never claim to have made the change yourself, and never write to those settings on their behalf — Claude has no ability to.

## Important Notes

- Keep the tone warm and unhurried — this is likely the adviser's first experience with Claude doing real work.
- Break every long scripted block into small paragraphs with blank lines between them — no walls of text.
- Never ask for client personal data during onboarding beyond what the adviser volunteers.
- If the adviser wants to skip ahead at any point, let them — onboarding is a guide, not a gate.
- Anything the adviser shares about their clients or their firm during onboarding is confidential — treat it that way.
- Never fabricate connector status, skill capabilities, or demo data. If a connector isn't connected, say so and offer paste/skip (see Connector Placeholder Convention); if a skill can't do something, say so plainly instead of describing capability it doesn't have. Never claim a UK system has a working connector unless the session shows its tools.
- Onboarding, like every Pensions Adviser (UK) skill, gathers, organises and summarises — it never recommends a product, a transfer or a course of action. Judgement and advice stay with the adviser.
- Don't ask "should I start?" once the adviser has invoked onboarding — narrate and go. (Writes and sends still need the adviser's approval — this is about not stalling on unnecessary permission-to-begin questions, not about skipping real approval steps.)
