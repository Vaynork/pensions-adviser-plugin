# UK pension tax constants — snapshot

> **Snapshot for the 2026/27 tax year (6 April 2026 – 5 April 2027). Verify every figure against HMRC guidance or the firm's own current technical source before use.** Rules and figures change at every fiscal event. Any figure this skill derives from these constants is labelled *"illustrative, based on figures supplied — verify"* wherever it appears, and none of it is quoted to a client until the adviser has checked it.

| Item | Figure (2026/27 snapshot) |
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

## How the skill uses this file

- **Only for headroom arithmetic on figures the adviser or a source supplied** — for example, AA used in a year against the standard AA, or LSA used to date against the standard LSA. The constant and the supplied figure are both typed into `Bash` as numeric literals.
- **The standard figure is not the client's figure** where a protection, a transitional tax-free amount certificate, a tapered AA or a triggered MPAA applies. Where the file shows any of those, the skill says the standard constant may not apply and does not substitute its own figure for the client's.
- **Earlier tax years are not in this file.** Carry forward reaches back three years, and the AA for an earlier year is taken from the source or the adviser, never assumed to equal this year's figure.
