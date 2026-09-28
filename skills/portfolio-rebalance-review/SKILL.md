---
name: portfolio-rebalance-review
description: Run a portfolio review for a client or household across their pension, ISA, GIA and bond wrappers — performance net of charges against the benchmark or model, allocation drift against the client's risk-profile target or the firm's model portfolio (CIP) or DFM model, model-portfolio mapping, rebalance preparation with tax-aware options to consider (pension and ISA wrappers first, capital gains and the 30-day rule in the GIA, drawdown income protected), and a rebalance rationale memo for the client file. Triggers on "portfolio review", "/portfolio-rebalance-review", "drift analysis", "rebalance [client]", "how is [client]'s portfolio positioned", "rebalance rationale", "map [client] to our CIP", or "map [client] to a model".
---

# Portfolio Rebalance Review

Review a client portfolio end to end: performance → drift → model mapping → rebalance prep → rebalance rationale memo.

## Inputs

Required: **client/household name**. Optional: which wrappers and plans to include, the target allocation (the client's risk-profile target, the firm's model portfolio under its Centralised Investment Proposition (CIP), or a discretionary fund manager (DFM) model) if not on file, and whether the adviser wants analysis only or a full rebalance prep.

## Step 1: Pull Performance & Holdings

**Disambiguation rule:** confirm which client or household before pulling anything, the same as every other skill in this plugin — if a name search returns more than one match, show the adviser the candidates and ask which one before proceeding. Never proceed on a name match alone.

Query the household's connected portfolio-data system for:
- Wrappers and plans — SIPP, personal or workplace pension, ISA, GIA, onshore/offshore investment bond — with provider/platform and values
- Holdings with units, value, and, for GIA holdings, base cost and unrealised gain/loss
- Performance: 3-month / year-to-date / 1-year / 3-year / 5-year, net of all charges (fund, platform, and any adviser or DFM charge) vs. the assigned benchmark or model
- Assigned model / target allocation and cash balances, by wrapper
- Recent and planned flows — contributions, withdrawals, **regular drawdown income**, any planned UFPLS or tax-free cash, and whether the client has already flexibly accessed any pension (the MPAA position)

**Which system to query:** this data can live in Addepar (the plugin's declared portfolio connector), or on a platform or back office with no declared connector — Transact, Quilter, AJ Bell Investcentre, Aviva, Fidelity Adviser Solutions or Nucleus for the platform; Intelligent Office, Xplan, Curo or Plannr for valuation feeds held in the back office. Check `ListConnectors` (load via `ToolSearch` if not already available) to see which is actually connected — don't guess at tool-name prefixes, use `ToolSearch` by system name once you know which is live. For the platforms and back offices listed, `ToolSearch` by name is the only check: if nothing comes back, treat the system as not connected and never tell the adviser it has a working connector.

**Look for the tools before you trust the registry.** `ToolSearch` by the system's own name is the check that decides: if its tools come back, that system is connected and callable — use them. `ListConnectors` can answer "No installed connectors found" even in a session with several live, working connectors, and in some clients it renders a user-facing card rather than returning data at all. So it explains a gap, it never establishes one, and an empty result means **unknown**, never "nothing is connected". When it does return entries, read `enabledInChat`, not `connected`: `connected: true` with `enabledInChat: false` is authenticated but switched off for this chat, so tell the adviser they can enable it here rather than reporting it as unconnected; a missing or `null` `connected` is unknown, not disconnected.
- **If none is connected**: follow the Connector Placeholder Convention — say *"This is where I'd make a call out to [system] to pull [holdings/performance] once that connector is built,"* then offer the fallback. Before asking for a manual upload, offer to search Google Drive, SharePoint (Microsoft 365), Box or Dropbox (whichever is connected) for an existing platform valuation or export. If nothing turns up there either, ask the adviser to upload a platform valuation or export (CSV/PDF), a provider statement, or paste holdings. Continue with whatever's provided, and mark anything still missing "— pending [connector]" rather than leaving it blank — a missing source degrades only the section that depends on it, not the whole review.
- **If more than one connected tool could try to solve this for the household**, ask the adviser once which is the book of record — per the Ask-Once, Then Route Convention — rather than guessing or merging both, and use that system for the rest of this review. This applies even when the household name hasn't resolved against either system yet: ask before searching further, not after finding out neither recognises the name — an unresolved household is not an exception to this rule. Offer to help the adviser save the choice using the Personalization Convention so they aren't asked again next session. This check runs for the rest of the review, not just once up front — if the adviser brings up another source mid-review, ask before pulling from it too. And if a second system's figures get pulled anyway and disagree with the routed one on a material fact (a balance, a drift percentage), that's a blocking question for the adviser, not a note in the output. If they disagree by orders of magnitude, follow the Magnitude-Conflict Convention: name the conflict, and exclude the outlier's figures from every table and total rather than quoting them as evidence.

**Held-away plans:** ask the adviser whether the client has plans held away from this system (a workplace pension, a legacy personal pension, a GIA or ISA on another platform) relevant to the 30-day share-matching check or the overall allocation picture. If yes, request those holdings manually — there's no connector for outside plans.

**Addepar specifics:** call `get_portfolio_data` with `lookthrough=false` for drift purposes. Lookthrough decomposition (fund → underlying constituents) is a separate risk-review lens — a model portfolio names sleeves at the fund level, and lookthrough silently returns an incompatible set of buckets with no warning. Group by `direct_owner`, not `account` — the latter is not a valid grouping key and errors. For tax-lot detail, pass a tax-lot value in `groupings` only if the live tool schema actually documents one — cost basis and lot-level fields are not confirmed to exist on every Addepar deployment. If the schema doesn't support it or the returned columns don't include cost basis, say so explicitly rather than presenting fabricated lot data; this feeds the same "Completeness" gate below. Note too that UK capital gains on shares and fund units are worked out on a pooled average base cost per holding, not lot by lot — a lot-level feed built for another regime is a starting point for the pooled figure, not the figure itself, and the pooled base cost the platform or the client's records show takes precedence.

**Data-sanity gate — run before Step 2, don't skip.** Dispatch this to the `pensions-adviser:holdings-sanity` subagent — `Agent(pensions-adviser:holdings-sanity)` — rather than working through it inline: hand it the holdings data, the reported portfolio/household value, and the sleeve structure from the risk-profile target or model if one is on file. It returns a flag table with a `Contaminates` column naming which downstream figure each problem feeds, plus an explicit list of the checks that passed.

Act on what comes back before touching Step 2. A `BLOCKING` verdict means a flag would corrupt the drift table itself — resolve it with the adviser first. `FLAGS` means the review continues with the caveats carried into the output. The subagent never repairs data, drops a position, or estimates a missing field, so anything it raises is still yours to decide about.

The seven checks it runs, which are also the checks to run by hand if the subagent is unavailable:
- **Temporal:** flag any position whose valuation date precedes its first funding, contribution or transfer-in transaction.
- **Magnitude:** flag any position whose gain looks implausible for the asset type and time held (e.g. a property or private-markets fund up several multiples within months of purchase) and confirm the mark with the adviser before using it.
- **Aggregation:** flag any sleeve or household-level return that's materially inconsistent with the sum of its parts (one position driving the whole household return while everything else is flat/negative is a signal, not a fact).
- **Reconciliation:** reconcile the holdings total against the reported portfolio value.
- **Completeness:** flag any position missing a field a later step depends on — GIA base cost, quantity, wrapper, or an asset-class/sleeve tag — rather than silently excluding it from drift or tax calculations.
- **Staleness:** flag when a mark's as-of date is materially older than the rest of the portfolio it's being compared against (common for property, with-profits and illiquid holdings priced less often than daily dealt funds) — note the mismatch rather than treating all "Current %" figures as equally current.
- **Duplication:** flag if the same underlying exposure may be represented more than once — e.g. a fund-level position and its lookthrough decomposition both pulled into the same table, or a held-away plan that turns out to already be visible through the primary connector.
- If anything trips, say so explicitly and state which downstream conclusions (drift %, performance %) depend on the suspect figure — never let a bad mark flow silently into the drift table.

## Step 2: Drift Analysis

Compare current allocation to the client's target. **Sourcing the target:**

- **Client target on file — it governs.** The target comes from the client's agreed risk profile (attitude to risk, capacity for loss) mapped to the firm's model portfolio under its CIP, or to the DFM model the client is invested in. Prefer pulling it from the connected system of record if one exposes it as structured data; today no connected system reliably does (Addepar has target bands in-product but doesn't expose them over MCP yet, and risk-profiling tools such as Dynamic Planner, FE Analytics, Synaptic or Defaqto have no declared connector — `ToolSearch` by name, use them only if their tools come back), so ask the adviser for the target and bands or accept a pasted model factsheet or suitability report extract — this instruction upgrades automatically once a connector exposes target data.
- **No target on file:** ask the adviser which model the client is mapped to, and the client's recorded risk profile. Never select a model or a risk profile for them. If the adviser wants a comparison against a model the client isn't formally mapped to, label the drift table and every figure derived from it *"vs. adviser-selected illustrative model [name] — not the client's agreed target"*, and carry that label into the memo and the client-facing summary.

Source sleeve names, targets, and bands from whatever model you end up with — don't assume a fixed set of asset classes. Fall back to the table below only when no model sleeve structure is on file:

| Asset Class | Target % | Current % | Drift | £ Over/Under |
|------------|----------|-----------|-------|-------------|
| UK Equity | | | | |
| Overseas Developed Equity | | | | |
| Emerging Markets Equity | | | | |
| UK Gilts | | | | |
| Corporate / Global Bonds | | | | |
| High Yield / Credit | | | | |
| Property | | | | |
| Alternatives | | | | |
| Cash | | | | |

Show drift at household level and by wrapper — a household that is on target overall can still be badly placed across wrappers (all the equity in the GIA and all the bonds in the SIPP, say), which matters for Step 4.

Flag positions exceeding the rebalancing band (default ±5% absolute or the firm's stated band — ask if unknown). **Bands may differ by liquidity tier** — illiquid sleeves (property funds that can suspend dealing, private-markets funds, legacy with-profits) typically carry a wider band than liquid ones; use what the firm's policy specifies, ask if it doesn't distinguish. A breach in an illiquid sleeve is a pacing signal, not a trade instruction — it may not be tradeable back promptly — so surface it as context rather than generating a change against it.

Also flag: concentrated single positions (>10% of household), cash drag, and style drift within an asset class.

**Risk-profile review cadence:** check when the client's risk profile (attitude to risk and capacity for loss) was last assessed against the firm's stated review cadence. If none is on file, default to flagging anything not reviewed in the last 12 months (in line with an annual ongoing-advice review) and ask the adviser for the firm's actual policy — same pattern as the band default above. Note staleness alongside the drift table; don't block the rebalance on it.

**Analysis-only path:** if the adviser asked for analysis only (see Inputs), stop here — output the drift analysis and the plain-English summary from Step 6, and skip Steps 3–5.

## Step 3: Model-Portfolio Mapping

**Which model source:** the firm's own CIP model or the client's DFM model, as the adviser supplies it — a model factsheet, a platform model-portfolio export, or a pasted holdings list with weights. If a platform or DFM system holding the model is connected (`ToolSearch` by its name first; `ListConnectors` only to explain a gap, reading `enabledInChat` rather than `connected`), read the model from there. If no model definition is supplied or found, say so and skip the mapping rather than scoring against an assumed model. When Step 2 sourced the target from an assigned or adviser-selected model, score against that same model here, never a different one.

Morningstar or FactSet, if connected, can supply fund-level classification (asset class, sector, region) to help map a holding to a model sleeve — cite them as the source of the classification, and never as a source of a model or a fund recommendation. Never offer to create or update a model on any platform or DFM system — model maintenance is out of scope for this skill.

- If the household is mapped to a model, score current holdings against it: matched positions, close substitutes (e.g. a different share class or a legacy fund with a similar mandate), and orphan positions.
- If no model is mapped, ask the adviser for the firm's model lineup and which model corresponds to the client's recorded risk profile under the firm's own mapping — or, only if the adviser asks for it, use generic risk-graded sleeves labelled illustrative: Cautious 30/70 → Adventurous 90/10 — and show the gap analysis. The choice of model is the adviser's; present any mapping as an option for them to weigh, not as Claude's recommendation.
- Output a mapping table: current holding → model position → action (hold / substitute / sell).

## Step 4: Rebalance Prep

Identify the adjustments that would bring the household back to target, tax-aware:
- **Rebalance inside pension and ISA wrappers first** — switches inside a SIPP, personal or workplace pension, or ISA have no capital gains tax consequence. If the household has none, say so explicitly in the options list and memo rather than silently skipping this.
- **In the GIA:** estimate the gain or loss on any disposal from the pooled base cost, and set the total against the CGT annual exempt amount — take the figure from the firm's technical source or the adviser. If neither has given one, you may show £3,000 for 2026/27 labelled *"to verify with the firm's technical source before relying on it"*; never quote a CGT rate you weren't given. Consider whether realising available losses while rebalancing would help, and whether gains could be spread across tax years — as options for the adviser, not instructions.
- **The 30-day share-matching rule** (bed and breakfasting): a disposal from the GIA followed by a reacquisition of the same shares or units by the same person within 30 days is matched to the reacquisition, not the original holding, so the intended gain or loss may not crystallise. Check it across every plan belonging to that person whose holdings and transaction history you **actually gathered** — being connected is not the same as being gathered: a held-away GIA the adviser confirmed exists but never supplied holdings for sits outside that check, and so does a connected account whose feed returned no base cost or transaction detail, the gap Step 1's Addepar note and Completeness check already record. Where the check couldn't reach the whole household, say so plainly: name the plans it covered and the ones it didn't, and carry that same scope into the memo's 30-day-rule line rather than a bare "yes".
- **Bed & ISA and Bed & SIPP** — selling in the GIA and repurchasing inside the client's ISA (within the ISA subscription limit) or pension (within their available annual allowance, and subject to the MPAA if it applies) — are options for the adviser to consider, not recommendations. Show them only where the client appears to have unused ISA subscription or pension annual allowance, and mark both allowances "— pending adviser confirmation" unless they were confirmed from a source.
- **Investment bonds:** a fund switch inside a bond is not the same as taking money out of it; a withdrawal or part-surrender to fund something outside the bond may be a chargeable event. Flag it for the adviser to confirm with the provider — don't compute the tax.
- **Protect drawdown income before selling in a pension wrapper.** Check the regular drawdown income, and any planned UFPLS or tax-free cash, so the rebalance doesn't disrupt them: confirm the wrapper's cash account still covers the next income payments (and whatever cash reserve the firm's policy or the client's plan sets) after the proposed switches, and prefer funding the income from the sale of an overweight sleeve over an unrelated one.
- **Money purchase annual allowance (MPAA).** Switching funds inside a pension is not flexible access and does not trigger the MPAA. Taking income beyond tax-free cash — flexi-access drawdown income or an UFPLS — can. If any option in this review would involve taking money out of a pension rather than switching within it, flag the MPAA point for the adviser, especially if the client is still contributing; don't advise on it, and don't let a rebalance become the occasion for a withdrawal the client hasn't asked for.
- For a concentrated GIA position with a large embedded gain, weigh trimming against the client's likely holding horizon: gains on assets held outside a pension are generally not charged to CGT on death (the beneficiaries take them at market value), though the estate may face inheritance tax. For an elderly or terminally-ill client this is a real trade-off to reason through and document, not a default "trim because it's outside the band" — confirm the treatment with the firm's technical source.
- Prefer directing pending contributions/cash to underweights over selling
- Respect client restrictions (ethical or ESG preferences, legacy holdings the client wants kept, with-profits funds where an MVR could apply on a switch-out, funds with dealing suspended)

**Cash earmarked or committed:** if Addepar is the connected system, call its upcoming private-fund capital-activity tool before treating cash balances as available — net out committed-but-uncalled capital-call obligations from what counts as deployable cash, same as an illiquid-sleeve band breach is a pacing signal rather than a trade instruction. Surface any near-term call as a flag/context line next to the cash figures it affects, don't silently consume it into the options list. The same applies to cash held in a pension wrapper to pay upcoming drawdown income. No connected system currently supplies forward-looking call dates for platform-only households — note that gap rather than guessing.

**Zocks AI results as a rebalance-rationale input:** if Zocks is connected, pull its AI results/insights for the household and check whether the potential changes line up with what the client has actually expressed — stated attitude to risk, income needs, life events — and with the risk profile on file. Flag a mismatch inline against the specific change it bears on (e.g. a riskier change against an explicitly stated low tolerance for risk, or a life event suggesting the risk profile or capacity for loss may be out of date), not as a general blurb at the top of the output. Zocks is a sentiment/context source, never a portfolio book of record.

**Execution feasibility check** before finalising the options list — flag, don't silently assume:
- Fund minimums: flag that a switch may be subject to the fund's or platform's minimum investment or minimum holding — tell the adviser to confirm with the platform, don't assume a number.
- Dealing cut-offs and pricing: most funds are forward-priced at a daily valuation point, so a sell and the matching buy may not price on the same day; flag the out-of-market risk and tell the adviser to confirm the platform's dealing cut-off rather than assuming one.
- Platform switch or dealing charges, and any exit charge or MVR on a legacy or with-profits plan: flag that they may apply and should be confirmed with the platform or provider before the switch is costed.
- Exchange-traded holdings (ETFs, investment trusts): flag that the bid-offer spread and any premium or discount to NAV should be checked at time of trade.
- Rebalancing the same model across many clients at once (a bulk or model-level switch on the platform) is out of scope for this skill's single-household design — note it as a known limitation, don't attempt to aggregate.

**Discretionary management reporting.** Only where the firm itself runs the portfolio on a discretionary basis: MiFID rules generally require the client to be told when the overall portfolio value falls by 10% (and each further 10%) since the last periodic report. If the drift or performance figures suggest that threshold may have been reached, flag it to the adviser to check against the firm's own depreciation-reporting process — don't determine whether the duty applies. Where the portfolio is advisory, or run by an external DFM, say nothing on this beyond noting that the DFM owns its own reporting.

**Rebalancing options:**

| Wrapper / Plan | Action | Fund | Units/£ | Reason | Est. Tax Impact |
|---------|--------|----------|----------|--------|-----------------|

Include totals: estimated GIA gains/losses against the annual exempt amount (with its source), transaction and switch costs, and before/after drift.

**Execution note:** this skill *lays out rebalancing options*; it never executes anything. Once platform connectors support staging switches, offer to stage the instruction — until then say: *"This is where I'd stage these switches on [platform] once that connector is built"* and output the options list in the platform's bulk-switch upload format if known.

## Step 5: Rebalance Rationale Memo

Every rebalance gets a memo for the client file. Use `templates/rebalance-rationale-memo.md` in this skill's folder. It must state: the client's objective, attitude to risk and capacity for loss, and the model or target they are mapped to; the suitability report the current strategy rests on (date, if known); what drifted and why; what is being changed and why each adjustment serves the client's interest; tax impact considered; the effect on drawdown income; and alternatives considered. Whether the change falls within the client's existing agreed strategy or needs fresh advice and a new suitability report is the adviser's call — leave that line for them. Leave the template's Approval table empty — nothing in this review establishes who approved a change, and the adviser and any reviewer the firm requires sign for themselves. Never fill in a name or a date there, and never describe the memo as approved.

## Step 6: Output

Write everything to a markdown file first:
- Drift analysis table (household and by wrapper) + before/after allocation comparison
- Rebalancing options with tax impact summary
- Model mapping table (if Step 3 ran)
- Rebalance rationale memo (using `templates/rebalance-rationale-memo.md`)
- 3-sentence plain-English summary the adviser could relay to the client

Then ask the adviser whether they'd like the options list exported to Excel and/or the rationale memo converted to Word/PDF — don't create those formats unless they ask.

## Out of Scope (for now)

- **No trade execution.** This skill prepares options for adviser review; it never places a deal or a switch.
- **No fabricating holdings, base costs, or allowances.** When a connected source doesn't confirm a figure, say so — never fill the gap with an invented number.
- **No suitability or legal determination.** This skill surfaces drift, tax impact, and rationale for the adviser to weigh — it never states that a portfolio or a change is or isn't suitable.
- **No advice on pension withdrawals, the MPAA, or tax planning** — those points are flagged for the adviser, never decided.

## Important Notes

- This review can take a few minutes once portfolio data starts flowing across steps — say so up front rather than asking whether to proceed; invoking the skill is already the go-ahead.
- Don't rebalance for rebalancing's sake — drift within bands is fine; tax and dealing costs can exceed the benefit. Show the breakeven when it's close.
- Check pending cash flows (contributions, withdrawals, drawdown income, planned UFPLS or tax-free cash) before a sell appears in the options.
- All buy/sell output is **a draft for adviser review — options laid out for the adviser to weigh, not advice** — the adviser owns suitability and best execution.
- Document everything: the rationale memo belongs on the client file, kept per the firm's record-keeping policy (SYSC 9 and the COBS 9 suitability records); run any client-facing summary through **/compliance**, which also covers how past performance may be shown.
- Check the 30-day share-matching rule across every GIA plan whose holdings and transaction history you actually gathered — a held-away plan once the adviser supplies its holdings, a connected account once its feed actually returns base cost — and say so when the check couldn't cover them all.
- Treat client portfolio and plan data as confidential; only include what's needed for this review.
