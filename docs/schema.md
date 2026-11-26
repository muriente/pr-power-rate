# Endpoint schema (v1)

Base URL: `https://muriente.github.io/pr-power-rate/api/v1/`

| File | Content |
|---|---|
| `current.json` | The rate in force today (America/Puerto_Rico), its components and sources |
| `history.json` | Every period in LUMA's factor table since May 2019 (factors; price where the base tariff is modeled) |
| `price.txt` | Just `price_usd_per_kwh`, six decimals, newline-terminated |

## `current.json`

| Field | Type | Meaning |
|---|---|---|
| `price_usd_per_kwh` | number | **The rate to configure in apps.** Marginal price of one more kWh for a standard residential (GRS, non-subsidized) customer: base energy charge + FCA + PPCA + CILTA + SUBA-HH + SUBA-NHH + EE (+ Pension/Provisional riders when non-zero). Six decimals, the precision NEPR orders use. |
| `price_cents_per_kwh` | number | Same, in cents. |
| `fixed_charge_usd_per_month` | number | Monthly customer charge (not per kWh). |
| `average_usd_per_kwh_including_fixed_charge` | object | All-in average at 400/800/1000 kWh/month (`price + fixed/kWh`). The 800 kWh value is the number the press and NEPR's bill-impact table quote. |
| `effective_start`, `effective_end` | date | Period the price is in force (inclusive). After `effective_end` the data is stale; consumers should treat it as unavailable. |
| `period_label` | string | LUMA's own label for the row, e.g. `octubre a diciembre 2026`. |
| `upcoming` | object or null | The next period's price when LUMA has already published it. |
| `components` | object | Each component: `name`, `usd_per_kwh`, `source` (URL of the controlling document). |
| `not_included` | object | FOS (a credit for qualifying low-use subsidized customers) and other items deliberately left out. |
| `sources` | object | LUMA workbook URL + sha256, NEPR quarterly order, NEPR annual riders order, base-tariff documents. |
| `verification` | object | Result of matching every factor digit-for-digit against the NEPR orders (`status: verified`). |
| `generated_at`, `checked_on` | timestamp, date | When the pipeline built and last checked the data. |

Stability: fields are only added in v1, never renamed or removed. A breaking change ships as `/api/v2/`.
