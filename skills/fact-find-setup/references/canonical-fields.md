# Canonical fact-find fields

Every field in a firm's fact-find schema is mapped to one of these keys, or to `custom`. The keys are what `/fact-find` recognises: a firm's "Name of pension provider", "Scheme / insurer" and "Provider" all map to `pension.provider`, so the same extracted fact fills all three.

Keys are grouped by the **section repeat** they normally sit in (`per_client`, `per_item`, `once`), but a firm's form decides the real structure — map by meaning, not by where the key is listed here.

When no key fits, use `custom` and keep the firm's label. Don't stretch a key to cover something it doesn't mean: a wrong mapping fills a field with the wrong fact, which is worse than a blank.

Keys marked **(SC)** are special category data under UK GDPR. Keys marked **(never filled)** are left blank by `/fact-find` in every case — see `schema-format.md`.

## Person — per client

| Key | Meaning |
|---|---|
| `person.title` | Title |
| `person.full_name` | Full name in a single box (forenames and surname together) |
| `person.forenames` | Forename(s) |
| `person.surname` | Surname |
| `person.previous_names` | Previous or maiden names |
| `person.preferred_name` | Known as |
| `person.dob` | Date of birth |
| `person.gender` | Gender, as the form asks it |
| `person.ni_number` | National Insurance number |
| `person.nationality` | Nationality |
| `person.domicile` | Domicile |
| `person.tax_residence` | Country of tax residence |
| `person.marital_status` | Marital or civil partnership status |
| `person.address` | Current address |
| `person.postcode` | Postcode |
| `person.time_at_address` | Time at address |
| `person.phone` | Telephone |
| `person.email` | Email |
| `person.contact_preference` | Preferred contact method and times |

## Health and lifestyle — per client

| Key | Meaning |
|---|---|
| `health.state` | General state of health **(SC)** |
| `health.conditions` | Medical conditions **(SC)** |
| `health.smoker` | Smoker status **(SC)** |
| `health.life_expectancy_notes` | Anything bearing on life expectancy or enhanced annuity eligibility **(SC)** |

## Vulnerability and accessibility — per client

| Key | Meaning |
|---|---|
| `vulnerability.indicators` | Possible vulnerability indicators noted (health, life events, resilience, capability), for the adviser to assess — never a label |
| `vulnerability.support_needs` | Support or adjustments the client has asked for |
| `vulnerability.third_party` | Trusted contact, attorney or third party authorised to act |

## Dependants — per item

| Key | Meaning |
|---|---|
| `dependant.name` | Name |
| `dependant.relationship` | Relationship |
| `dependant.dob` | Date of birth |
| `dependant.financially_dependent` | Financially dependent? |
| `dependant.dependent_until` | Dependent until |

## Employment and income — per client

| Key | Meaning |
|---|---|
| `employment.status` | Employed, self-employed, director, retired, not working |
| `employment.occupation` | Occupation |
| `employment.employer` | Employer or business name |
| `employment.start_date` | Start date |
| `employment.intended_retirement_age` | Intended retirement age |
| `income.gross_salary` | Gross basic salary |
| `income.bonus` | Bonus, commission, overtime |
| `income.benefits_in_kind` | Benefits in kind |
| `income.self_employed_profit` | Self-employed or company profit |
| `income.dividends` | Dividend income |
| `income.rental` | Rental income |
| `income.pension_income` | Pension income in payment |
| `income.state_pension` | State Pension in payment |
| `income.other` | Other income |
| `income.net_monthly` | Net monthly income |
| `income.tax_rate` | Highest marginal rate of income tax |

## Expenditure — once or per client

| Key | Meaning |
|---|---|
| `expenditure.essential_monthly` | Essential monthly outgoings |
| `expenditure.discretionary_monthly` | Discretionary monthly outgoings |
| `expenditure.planned_changes` | Expected changes to spending |
| `expenditure.emergency_fund` | Emergency fund held or required |

## Property — per item

| Key | Meaning |
|---|---|
| `property.description` | Main residence, second home, buy-to-let |
| `property.owner` | Owner(s) and tenure (joint tenants, tenants in common) |
| `property.value` | Estimated value |
| `property.value_date` | Date of valuation |

## Liabilities — per item

| Key | Meaning |
|---|---|
| `liability.type` | Mortgage, loan, credit card, other |
| `liability.lender` | Lender |
| `liability.owner` | Whose liability |
| `liability.balance` | Outstanding balance |
| `liability.monthly_payment` | Monthly payment |
| `liability.rate` | Interest rate |
| `liability.end_date` | End or redemption date |
| `liability.repayment_type` | Repayment or interest-only |

## Cash and investments — per item

| Key | Meaning |
|---|---|
| `investment.type` | Cash, cash ISA, stocks and shares ISA, GIA, onshore/offshore bond, NS&I, shares, VCT/EIS |
| `investment.provider` | Provider or platform |
| `investment.reference` | Account or policy reference |
| `investment.owner` | Owner(s) |
| `investment.value` | Current value |
| `investment.value_date` | Valuation date |
| `investment.regular_contribution` | Regular contribution |
| `investment.base_cost` | Base cost / amount invested |
| `investment.funds` | Funds or holdings |
| `investment.charges` | Charges |

## Pensions — per item

| Key | Meaning |
|---|---|
| `pension.owner` | Whose pension |
| `pension.type` | Workplace DC, personal pension, SIPP, stakeholder, RAC, section 32, DB, AVC/FSAVC, annuity |
| `pension.provider` | Provider or scheme name |
| `pension.reference` | Plan or member reference |
| `pension.employer` | Employer, for a workplace scheme |
| `pension.status` | Active, deferred, in drawdown, in payment |
| `pension.value` | Fund value |
| `pension.transfer_value` | Transfer value (CETV for DB), where different from fund value |
| `pension.value_date` | Valuation date |
| `pension.crystallised_value` | Crystallised amount |
| `pension.uncrystallised_value` | Uncrystallised amount |
| `pension.contribution_personal` | Personal contribution |
| `pension.contribution_employer` | Employer contribution |
| `pension.contribution_basis` | Relief at source, net pay, salary sacrifice |
| `pension.selected_retirement_age` | Selected or normal retirement age |
| `pension.funds` | Funds or investment strategy (incl. lifestyling) |
| `pension.charges` | Charges |
| `pension.db_pension_at_nra` | DB: scheme pension at normal retirement age |
| `pension.db_nra` | DB: normal retirement age |
| `pension.db_spouse_pension` | DB: spouse's or dependant's pension |
| `pension.income_in_payment` | Income currently being taken |
| `pension.death_benefits` | Death benefits (lump sum, dependant's pension, beneficiary drawdown) |
| `pension.nomination` | Expression of wish or nomination on file, and its date |
| `pension.safeguarded_benefits` | Safeguarded benefits present (DB, GAR, GMP) |
| `pension.gar` | Guaranteed annuity rate |
| `pension.gmp` | Guaranteed minimum pension |
| `pension.protected_tfc` | Protected tax-free cash above 25% |
| `pension.protected_pension_age` | Protected pension age |
| `pension.mvr` | Market value reduction terms |
| `pension.exit_charges` | Exit or transfer charges |
| `pension.bonuses` | Loyalty or terminal bonuses |
| `pension.life_cover` | Life cover or waiver attached |

## Pension tax position — per client

| Key | Meaning |
|---|---|
| `pension_tax.aa_used` | Pension input amounts / annual allowance used, by tax year |
| `pension_tax.carry_forward` | Carry forward available, as recorded |
| `pension_tax.mpaa_triggered` | MPAA triggered, and the date |
| `pension_tax.lsa_used` | Lump sum allowance used |
| `pension_tax.lsdba_used` | Lump sum and death benefit allowance used |
| `pension_tax.protections` | Protections held (fixed, individual, enhanced, primary) and references |
| `pension_tax.ttfac` | Transitional tax-free amount certificate |

## State Pension — per client

| Key | Meaning |
|---|---|
| `state_pension.forecast` | Forecast amount, per the client's forecast |
| `state_pension.forecast_date` | Date of forecast |
| `state_pension.age` | State Pension age |
| `state_pension.ni_gaps` | NI record gaps noted on the forecast |

## Protection — per item

| Key | Meaning |
|---|---|
| `protection.type` | Life, critical illness, income protection, family income benefit, PMI |
| `protection.provider` | Provider |
| `protection.life_assured` | Life or lives assured |
| `protection.sum_assured` | Sum assured or benefit |
| `protection.premium` | Premium |
| `protection.end_date` | End date |
| `protection.in_trust` | Written in trust? |

## Estate planning — per client

| Key | Meaning |
|---|---|
| `estate.will` | Will in place, and date |
| `estate.lpa_financial` | Lasting power of attorney (property and financial affairs), registered? |
| `estate.lpa_health` | Lasting power of attorney (health and welfare), registered? |
| `estate.gifts` | Gifts made in the last seven years |
| `estate.inheritance_expected` | Expected inheritances |
| `estate.iht_notes` | Anything the client said about inheritance tax |

## Objectives and retirement — once or per client

| Key | Meaning |
|---|---|
| `objectives.summary` | The client's objectives, in their words where possible |
| `objectives.priorities` | Order of priority |
| `retirement.target_date` | Target retirement date or age |
| `retirement.income_need` | Income wanted in retirement, and whether in today's terms |
| `retirement.lump_sum_need` | Lump sums wanted, and when |
| `retirement.income_flexibility` | Preference for secure vs flexible income, as the client expressed it |
| `retirement.legacy_wishes` | Wishes to leave money to others |

## Risk, capacity and experience — per client

| Key | Meaning |
|---|---|
| `atr.questionnaire` | Risk-profiling tool used and date completed |
| `atr.client_comments` | What the client said about risk, in their words |
| `atr.result` | Assessed attitude to risk **(never filled)** |
| `capacity_for_loss.facts` | Facts bearing on capacity for loss (reliance on the pot, other secure income) |
| `capacity_for_loss.result` | Assessed capacity for loss **(never filled)** |
| `experience.investments` | Investment knowledge and experience |
| `preferences.sustainability` | Sustainability or ethical preferences |
| `preferences.exclusions` | Investments the client wants to avoid |

## Adviser and declarations

| Key | Meaning |
|---|---|
| `meta.meeting_date` | Date of the fact-find meeting |
| `meta.meeting_type` | Face to face, video, phone |
| `meta.others_present` | Others present |
| `adviser.name` | Adviser name |
| `adviser.signature` | Adviser signature **(never filled)** |
| `adviser.date_signed` | Adviser date signed **(never filled)** |
| `declaration.client_confirmation` | Client confirmation of accuracy **(never filled)** |
| `declaration.client_signature` | Client signature **(never filled)** |
| `declaration.date_signed` | Client date signed **(never filled)** |
| `declaration.data_consent` | Consent to process special category data **(never filled)** |
