# UK pensions advice — maintainer context

This is the shared context this fork was built from. It is for people editing the plugin, not a file the skills load at run time. The run-time references live inside each skill's own `references/` folder, because a subagent's working directory is the session's and a shared path outside the skill will not resolve.

**Status of the figures below.** A snapshot taken for the 2026/27 tax year (6 April 2026 – 5 April 2027). Rules and figures change at every fiscal event. Anything a skill quotes to a client must come from the firm's own current technical source, the connected system, or the adviser. The skills are written to **cite, never compute** a constant they were not given, except where a skill says otherwise and marks the figure as needing verification.

## Who the plugin is for

UK financial advisers and paraplanners at FCA-authorised firms (directly authorised, or appointed representatives of a network) who give pensions and retirement advice: accumulation, consolidation and transfers, retirement income (drawdown and annuities), and death-benefit and tax planning around pensions.

Language: UK English ("adviser", "authorised", "organise"), pounds sterling, UK tax years (6 April to 5 April), day-month-year dates.

## The regulatory frame (FCA Handbook, unless stated)

| Area | Where it lives | What the skills do with it |
|---|---|---|
| **Consumer Duty** | PRIN 2A (in force 31 July 2023; closed products 31 July 2024). Cross-cutting rules: act in good faith, avoid foreseeable harm, enable and support customers to pursue their financial objectives. Four outcomes: products and services, price and value, consumer understanding, consumer support. | Every client-facing draft is checked against consumer understanding. Review prep collects evidence that the ongoing service was delivered and represents fair value. |
| **Financial promotions and client communications** | COBS 4: fair, clear and not misleading (COBS 4.2.1R); retail communication rules (COBS 4.5 / 4.5A); past performance (COBS 4.6): at least five complete 12-month periods or since inception, not the most prominent feature, the "not a reliable indicator" warning; simulated past performance and future performance (COBS 4.6.6R–4.6.8R). Social media guidance FG24/1. | `/compliance` rewrites these as its pass structure. |
| **Suitability** | COBS 9 / 9A: suitability report content, client's objectives, attitude to risk, capacity for loss, knowledge and experience. | Skills gather facts and draft; they never state that something is suitable. |
| **Pension transfers and conversions** | COBS 19.1. Transfers involving safeguarded benefits (DB, guaranteed annuity rates): starting assumption that a DB transfer is unsuitable (COBS 19.1.6G); appropriate pension transfer analysis (APTA) and transfer value comparator (TVC); advice given or checked by a pension transfer specialist; contingent charging banned from 1 October 2020 (with narrow carve-outs); abridged advice. Pension Schemes Act 2015: a member with safeguarded benefits worth more than £30,000 must take appropriate independent advice before transferring or converting. | `/pension-transfer-check` identifies safeguarded benefits and the advice requirement. It never assesses the transfer itself. |
| **Retirement income** | COBS 19 (retirement risk warnings, investment pathways, the "stronger nudge" to Pension Wise guidance from June 2022). FCA thematic review of retirement income advice (TR24/1, 2024): expectations on sustainable withdrawal rates, cashflow modelling, capacity for loss, and tax-efficient income. | `/retirement-income-review` lays out sustainability evidence and gaps. |
| **Ongoing advice** | FCA's 2024–25 review of ongoing advice services: firms must be able to show that the reviews clients pay for actually happened. | `/pre-meeting` and `/post-meeting` record what was delivered. |
| **Vulnerable customers** | FG21/1. Drivers: health, life events, resilience, capability. | Skills flag possible vulnerability indicators for the adviser. They never label a client "vulnerable". |
| **Record keeping** | SYSC 9; COBS 9.5 / 9A.4 (suitability records); COBS 4.11 (financial promotion records); COBS 11.8 (recording of telephone and electronic communications for MiFID business). Retention for pension transfer, conversion and opt-out records is **indefinite**. Other periods vary by business type. | `/compliance` keeps a scratch pad toward the firm's own records, with retention stated as "per firm policy; indefinite for pension transfer, conversion and opt-out material". |
| **Pension scams** | Occupational and Personal Pension Schemes (Conditions for Transfers) Regulations 2021 (from 30 November 2021): red flags stop a statutory transfer; amber flags require a MoneyHelper pensions safeguarding guidance appointment. FCA ScamSmart; Pension Scams Industry Group code. | `/pension-transfer-check` lists observable red and amber indicators for the adviser to evaluate. |
| **Advice / guidance boundary** | Pension Wise (MoneyHelper) free guidance for people aged 50+. FCA targeted support regime (introduced 2026). | Skills never recommend. Adviser-facing only. |

## Tax constants snapshot (2026/27, verify before use)

| Item | Figure |
|---|---|
| Annual allowance (AA) | £60,000 |
| Money purchase annual allowance (MPAA) | £10,000 |
| Tapered AA | threshold income £200,000; adjusted income £260,000; £1 reduction per £2 over; minimum £10,000 |
| Carry forward | unused AA from the three previous tax years, if a member of a registered scheme in each year; current year used first |
| Lifetime allowance | abolished from 6 April 2024 |
| Lump sum allowance (LSA) | £268,275 (higher with protection or a transitional tax-free amount certificate) |
| Lump sum and death benefit allowance (LSDBA) | £1,073,100 (higher with protection) |
| Normal minimum pension age | 55, rising to 57 from 6 April 2028 (protected pension ages exist) |
| Death benefits | death before 75: generally free of income tax within the LSDBA if paid within two years; death at or after 75: taxed at the recipient's marginal rate |
| Pensions and inheritance tax | from 6 April 2027 most unused pension funds and death benefits come into the estate for IHT (death-in-service benefits excluded; spouse/civil partner exemption applies). Check final legislation and HMRC guidance before relying on detail. |
| State Pension age | 66, rising to 67 between 2026 and 2028 |
| CGT annual exempt amount | £3,000; share-matching "30-day rule" (bed and breakfasting) applies to disposals and reacquisitions |
| ISA subscription limit | £20,000 |

## UK adviser tech stack (for onboarding and fallbacks)

None of these is assumed to have an MCP connector. The skills look for tools by name and fall back to paste or upload.

- **Back office / CRM:** Intelligent Office and Xplan (Iress), Curo, Plannr, Salesforce Financial Services Cloud
- **Platforms / wraps:** Transact, Quilter, AJ Bell Investcentre, Aviva, Fidelity Adviser Solutions, Nucleus, Parmenion, Standard Life, aberdeen Wrap
- **Cashflow modelling:** Voyant, CashCalc, Truth, Timeline
- **Research, risk profiling and due diligence:** FE Analytics, Defaqto Engage, Dynamic Planner, Synaptic, Morningstar
- **Meeting notes:** Aveni Assist, Saturn, Zocks, Microsoft Copilot
- **Pension transfers and tracing:** Origo Options, Selectapension, the Pension Tracing Service
- **Email, calendar and documents:** Microsoft 365 (Outlook, SharePoint), Gmail, Google Calendar, Google Drive, Box, Dropbox
