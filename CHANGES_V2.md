# V2 changes (Kareem) — entries for "Changes post handover"

Base: Haseeb's handover of 17-Nov-26 (spec v0.25 + post-handover decisions, update date Oct-26, 43/43).
V2 keeps every locked decision except where a row below says it replaces one. All V2 rules live in the pipeline
(`pipeline/config.yaml`, `pipeline/build.py`, `pipeline/control.json`); `index.html` only reads what the build writes.
Build: 51/51 checks (43 engine + 8 V2 regression checks), 2024–25 lock intact.

## Locked decisions (V2)

| Area | Rule | Replaces / why |
|---|---|---|
| Naming | New Model is shown as **HeyMoon.ai** everywhere (business line). "ROAS" stays for the pricing itself: ROAS Ladder, level, factor. | Labels only. |
| ARPA | **ARR ÷ average active accounts over the same 3 months**, every page (commission, HeyMoon.ai, blended). Blended ARR includes unallocated commission. | Replaces "TTM revenue ÷ active at period end" / "ARR ÷ active at period end". ARR is built from 3 months of revenue, so the denominator uses the same 3 months; brands signed in the last month barely contribute. |
| ROAS churn | Churn = ladder Churn month only (as locked 13-Nov). **New:** active brands with 6+ months without payment are listed on Control as "update the ladder" (`flag_after_months_without_payment: 6`). Not a churn rule. | Keeps the ladder as the single source; catches stale ladder entries (Sahseh, last paid Mar-26). |
| Touche Prive | Nov-25 pre-launch test: **out of HeyMoon.ai brand counts, churn and unit economics from 2026** (`exclude_from_new_model`). 2024–25 values stay frozen, so its Nov–Dec 25 ROAS revenue and active months remain in the 2025 history. | Replaces "counted" (39 since launch at Sep). HeyMoon.ai launched Jan 2026; the Investor Metrics file excludes it. |
| CAC | **CAC sheet spend** (source of truth) ÷ **HeyMoon.ai brands first paid, excluding brands migrated from commission** (refunded brands and Jetour count). Series `cac_new_brands`. **No fallback**: a month without spend shows CAC as —. KPI tiles: same rule for the selected period. Investor: since launch (Nov-25, incl. pre-launch spend). | Replaces sheet's own new-client count and the baked fallback. **To discuss with Haseeb** (see below). |
| Ounass buffer | Default **added back** on every page (one ARR). Investor page always adds it back, hides the switch and carries a "provisional" callout while months are unconfirmed. | Replaces default "held". With Sep and Oct provisional the add-back is +$325k ARR (≈10%). |
| Investor page | Mirrors the Summary sheet of the Investor Metrics file: HeyMoon.ai (ARR, YTD revenue, new brands, active, upgrade rate, NRR QoQ, logo churn/retention, customer retention L2+, CAC, ARPA, LTV, LTV/CAC, payback, gross margin), total company (ARR, YTD revenue), cash. **Point-in-time metrics at the latest month, growth vs 3 months earlier; NRR and upgrade rate on calendar quarters** (latest complete quarter vs the one before). Each growth cell names its comparison. | Answers the open point "New Model NRR / revenue churn window": calendar quarters. |
| Upgrade rate | Brands moving up 1+ level in the quarter ÷ brands active during it, **including brands that first paid in the quarter (from their L1 entry)**. | Matches the Investor Metrics file. |
| Customer retention (L2+) | Logo retention for brands that reached ladder level 2+, plus **Izil as direct entry at L5** (`direct_l2`). | New metric from the Summary sheet. |
| Plan | YE of the update year calculated on dashboard actuals with the v7.1 method (Q4 revenue = Q3 × average of last two quarterly NRRs + new brands × first-quarter revenue per new brand; new brands grow at the last QoQ rate); 2027–2030 = v7.1 inputs (`config.yaml plan`). | Answers the open point "YE 2026 / Y5 projection columns". |
| Cash | `control.json cash`: $208,034, burn $38,279/month, as at 31 Oct 2026 (to be linked). | Fills the open point. |

## Change log

| Date | Area | Change | Effect (Oct-26) |
|---|---|---|---|
| 17-Nov-26 | Pipeline | `config.yaml`: `exclude_from_new_model`, `flag_after_months_without_payment`, `direct_l2`, `cac`, `investor`, `plan` sections. `build.py`: Touche Prive out of 2026 churn events; series `cac_new_brands`; brand fields `hm_excluded`, `last_paid`; review list `payment_gap`; 8 V2 checks (V01–V08). `control.json`: cash. | Since launch: 43 paid, 13 churned (was 44 / 14). 51/51 checks; 2024–25 locked. |
| 18-Nov-26 | Investor tab · unit economics and plan | Unit economics on calendar quarters (Q3-26 vs Q2-26) with change chips. New "Path to $100M ARR by 2030" section (below Company and funding): funnel plan, option B. Phase 1 starts = acquisition spend ÷ CAC per start (2027–30 spend $0.72M / $3.0M / $7.2M / $14.6M; CAC $2.0k–2.6k incl. sales salaries); 30% conversion to scaled; 12% scaled churn; ARR per scaled brand $24k → $35k; $1,000 Phase 1 price; gross margin = company YTD. Inputs overridable in `config.yaml investor.path`. Shows a bridge of where 2030 ARR comes from and a today-vs-2030 key metrics table. Replaces the v7.1 plan on the investor view (v7.1 plan still in the management table). | 2030 HeyMoon.ai ARR $100.1M; 2,700 scaled brands; LTV/CAC 4.0x; $25.5M acquisition spend 2027–30. |
| 18-Nov-26 | Dashboard · Investor tab | Investor tab rebuilt to the v6 design and calculated live each month (no client names). "Download investor page" saves a standalone, name-free copy for investors; full Summary-sheet table and cash inputs moved to a "Management only" area that the download leaves out. Investor CAC now uses the rule C count (41). Gross margin from the data-pack P&L. Separate `investor.html` removed (the tab is the single source). | Upgrade rate 21% = 7 of 34 brands (the removed page said 4 of 19, wrong). Gross margin 52% (data pack) vs 51% (live P&L sheet, 18 Nov): to check with Haseeb. |
| 18-Nov-26 | Investor page v6 | Replaces v3: tiles ARR +231% QoQ, NRR 137% (GRR 61%, 11 brands), retention after Phase 1 88%, 7.9x spend per scaled brand; CAC by calendar quarter (Q3 $1.5k, -43% vs Q1) with fully loaded LTV/CAC; company section (total ARR, 2026 YTD revenue +38%, gross margin 51% from management P&L, cash, net burn, runway); raising $2M. | Figures fixed at Oct-26. |
| 18-Nov-26 | Investor page | New standalone `investor.html`: aggregate figures only, no client names, values fixed at Oct-26 (no live sheets). Not linked from the dashboard. | ARR +231% Q3 vs Q2; NRR 137% (GRR 61%); retention after Phase 1 88%; 7.9x spend per scaled brand. |
| 17-Nov-26 | Dashboard | Haseeb's 17-Nov `index.html` taken as the base; V2 page changes re-applied (3-way merge): naming, ARPA, CAC (`mtCacFor`), Investor page, Ounass default + provisional callout, data-gaps panel on Control, tier logo churn n/a, toggle hidden on Investor. In-page rules layer removed. | Contract check: no missing data fields; live-sheet links identical; changed contract functions are the V2 decisions above. |

## Kept as in the reference (not changed)

- Since-month rule: a brand whose ladder Churn month equals its Since month counts as active that month and churned the next (Lawni: Mar-26 → Apr-26). Kareem had asked for the ladder month to win; changing it would make the brand never appear as new. Left as spec, to confirm.
- S/M/L tiers on the model's CAC (parked), Ladder page "Fleet ARPA" (parked).

## To discuss with Haseeb

1. **CAC brand count.** The CAC sheet counts 44 new clients since launch at Oct-26; the dashboard uses 41 (rule C). The gap is Touche Prive (pre-launch test), DKNY and Izil (migrated from commission). Should the sheet take the dashboard's count? (Corrects an earlier note that said 39.)
2. **Hosting.** The repo is public and `data.json` / `pipeline/history_base.json` carry client revenue by name; the README marks the model confidential.
3. **Touche Prive 2025 history** stays in the frozen ROAS history (2024–25 lock); only 2026 metrics exclude it.
