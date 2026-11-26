# Third-party source audit: Puerto Rico (LUMA/PREPA) residential electricity rate

Audit date: 2026-11-26. Auditor: research agent (no logins, no contact with anyone).
Raw downloads were kept in the working directory of the audit session (not committed); every source is cited by URL below.

## 1. Official reference used for comparison

Source: LUMA "Tabla de Factores de Ajustes" XLSX (archived in `data/luma/archive/`, https://lumapr.com/wp-content/uploads/2026/10/Tabla-de-Factores-1.xlsx), values in $/kWh, cross-checked against NEPR Resolution and Order of 2026-09-30, case NEPR-MI-2020-0001
(https://energia.pr.gov/wp-content/uploads/sites/7/2026/09/20260930-MI20200001-Resolucion-y-Orden.pdf).

| Quarter | FCA | PPCA | FOS | CILTA | SUBA-HH | SUBA-NHH | EE | Pension | Provisional | Riders billed to GRS (all except FOS) |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct-Dec 2026 | 0.173576 | 0.045090 | 0.020822 | 0.007386 | 0.014338 | 0.000865 | 0.000853 | 0 | 0 | **0.242109** |
| Jul-Sep 2026 | 0.114070 | 0.051748 | 0.016650 | 0.007386 | 0.014338 | 0.000865 | 0.000853 | 0 | 0 | **0.189261** |
| Apr-Jun 2026 | 0.116349 | 0.045575 | 0.017577 | 0.004417 | 0.012558 | 0.001091 | 0.000853 | 0.019191 | 0.014931 | **0.214965** |
| Jan-Mar 2026 | 0.107627 | 0.044315 | 0.018546 | 0.004417 | 0.012558 | 0.001091 | 0.000853 | 0.019191 | 0.014931 | **0.204983** |
| Oct-Dec 2025 | 0.120158 | 0.044523 | 0.021510 | 0.004417 | 0.012558 | 0.001091 | 0.000853 | 0.019191 | 0.014931 | **0.217722** |

How the reference reconciles with NEPR's own bill example. NEPR R&O 2026-09-30, Table 2: an unsubsidized GRS customer using 800 kWh pays $228.59 ($0.28574/kWh) in Jul-Sep 2026 and $270.86 ($0.33858/kWh) in Oct-Dec 2026.
The base tariff in effect from 2026-07-01 is GRS $8.00/month plus $0.08648/kWh. It was since confirmed from the primary documents (NEPR-AP-2023-0003 final rate order, App. B p. 773; FY2027 tariff book), see official-sources.md, and it reproduces NEPR's Table 2 for two quarters.
With that base, the arithmetic gives:
- Jul-Sep 2026: 8 + 800 x (0.08648 + 0.189261) = **$228.59**
- Oct-Dec 2026: 8 + 800 x (0.08648 + 0.242109) = **$270.87**

Both match NEPR to the cent, rounding aside. This confirms three things:
- FOS is not billed to unsubsidized GRS customers.
- From Jul 2026 the Pension and Provisional riders are zero.
- The Oct-Dec 2026 marginal rate is **$0.328589/kWh** and the 800 kWh average is **$0.33858/kWh**.

The quarter-to-quarter change in FCA+PPCA is 0.052848, which NEPR Table 1 confirms. That is the "+5.28 c/kWh" in the press.

**Trap for scrapers.** LUMA's quarterly motions contain *proposed* factors that differ from what NEPR approves:
- Oct-Dec 2026: proposed FCA 0.180736, PPCA 0.045771, FOS 0.021136 (motion of 2026-09-15). Approved: 0.173576 / 0.045090 / 0.020822.
- Jul-Sep 2026: proposed FCA 0.125935, PPCA 0.051170, FOS 0.016063 (motion of 2026-06-15). Approved: 0.114070 / 0.051748 / 0.016650.

The "FCA 11.4070 -> 18.0736 c/kWh" sentence in the mission brief is from the NEPR R&O's *introduction*, which describes LUMA's proposal. The same paragraph says NEPR reduced it to **17.3576**. The 33.86 c/kWh headline figure is computed with the approved 17.3576, so the brief's anchor number is right and its FCA figure is the rejected proposal.

## 2. Verdict summary

| # | Source | Type | Latest period it reflects | Verdict |
|---|---|---|---|---|
| 1 | OpenEI URDB / IURDB (API v7, v8) | Rate database (machine-readable) | GRS: Apr-Jun 2023 factors, 2019 base tariff | **Stale** (wrong for every quarter audited) |
| 2 | NREL/NLR Utility Rates API v3 | Average-rate API | Ventyx 2012; returns "no data" for PR residential | **Not usable** |
| 3 | EIA Electric Power Monthly Table 5.6.A | Statistics | PR not included | **Not applicable** |
| 4 | EIA-861M monthly (sales_revenue.xlsx), PR rows | Statistics (revenue / kWh) | Through Sep 2026 (preliminary) | **Partial**: right order of magnitude, but a lagging blended average, not a rate. No Q4 2026 data |
| 5 | EIA Puerto Rico territory profile | Narrative | 2024 ranking only | **Not applicable** (no number) |
| 6 | findenergy.com PREPA page | Aggregator | 23.59 c/kWh, 2023 EIA data, published 2025-01-24 | **Stale** |
| 7 | Solargrin LUMA cost calculator | Calculator | Pre-filled $0.24/kWh "approximate average" | **Wrong/stale** for 2026 (-29% vs Q4 2026) |
| 8 | Nectar Climate PREPA C&I guide | Aggregator | C&I only, "effective Aug 28 2025", no rider values | **Partial/stale**, no residential |
| 9 | MyPRTools bill analyzer | Calculator | No stored rates (reads the user's own bill) | **Not applicable** |
| 10 | Mi LUMA web/app API (public, unauthenticated) | Utility portal | No rate/tariff endpoint exists | **Dead end** |
| 11 | GitHub / Home Assistant community | Code/configs | No project scrapes LUMA factors; ha-openei uses URDB | **None found** (ha-openei = stale) |
| 12 | Emporia (Vue) | App | "Verified" plans, else NREL/URDB fallback, else 13.2 c default | **Stale or wrong**; no PR coverage evidence |
| 13 | FranklinWH | App | Own tariff catalog (login-gated); no auto-update | **Unknown / manual**; never auto-updates |
| 14 | Tuya / Smart Life | App | Manual price per device | **Not applicable (manual)** |
| 15 | Arcadia (Genability) | Tariff API | Coverage of LUMA unverifiable without account (401) | **Unknown** |
| 16 | UtilityAPI | Data-access API | LUMA not supported | **Not applicable** |
| 17 | Electricity Maps | Carbon API | PR zone exists, no price data | **Not applicable** |
| 18 | Tesla, Enphase, Sense, SPAN, SolarEdge, HA Energy | Apps | Own catalogs, Arcadia, or manual | **Unknown / manual** |
| 19 | FindEnergyRates (MCP) | Aggregator | PR not covered (ZIP 00926 not mapped) | **Not applicable** |
| 20 | CallMePower (Selectra rate DB), https://callmepower.com/pr/utility/luma-energy | Aggregator web page | Oct-Dec 2026: GRS $8.00 + 32.86 c/kWh (updated 2026-11-26) | **Accurate for the current quarter**, but not reusable: HTML only, no breakdown, no history, first published 2026-11-17 (after the Oct 1 effective date) |
| 21 | AP / Fortune / US News (2026-10-01/02) | Press | Oct-Dec 2026: 33.86 c/kWh at 800 kWh, +5.28 c | **Accurate** (800 kWh average only) |
| 22 | PR press (El Nuevo Día, Metro, El Vocero, Primera Hora, La Perla, NotiCel, WAPA, ...) | Press | Every quarter Oct 2025 to Oct 2026 | **Mostly accurate** on totals; recurring unit errors and misattributions (section 4) |

**Conclusion: no third-party machine-readable source is accurate enough to reuse.**
- The only machine-readable rate database with PR entries is OpenEI URDB, and it is 3.5 years stale.
- The vendor apps either use URDB/NREL, use their own login-gated catalogs, or take manual entry. None auto-updates LUMA's quarterly factors.
- One aggregator page, CallMePower, matches Oct-Dec 2026 exactly: 8.648 base + 24.2109 riders = 32.859 c. It is HTML-only, gives no components or effective dates, and has no history or API. It only appeared on 2026-11-17, so there is no evidence it updates on the effective date. Use it only as an independent cross-check.
- Press articles match NEPR's own Table 2. They are copies of the resolution, so reading the NEPR resolution directly is strictly better.

The endpoint has to be built from the official LUMA XLSX, validated against the NEPR Resolución y Orden and the tariff book.

## 3. Per-source detail

### 3.1 OpenEI Utility Rate Database (URDB / IURDB)
- What: DOE/NREL-funded crowd-curated tariff DB; API `https://api.openei.org/utility_rates?version=7|8`; web `https://apps.openei.org/IURDB/`.
- Query evidence:
  - `country=PRI` returns 19 items, all under utility "Puerto Rico Electric Pwr Authority", eiaid 0 (`raw/urdb_country_PRI.json`, `raw/urdb_prepa_full.json`).
  - A live v7 re-fetch today with DEMO_KEY (`dl/audit/urdb_v7_country_PRI_live.json`) is byte-identical to the cached file. Nothing has been added since.
  - v8 returned HTTP 429 (DEMO_KEY rate limit).
  - Queries for "LUMA", "LUMA Energy", the full PREPA name, `eia=15376`, an address or a lat/lon all return `{"items":[]}`. PREPA is filed with eiaid 0, so lookups by EIA ID or location fail.
- Entries and latest startdate:
  - 2018-11-01 set (14 entries: GRS, LRS, RH3, RFR 105/106/107, GSS, GSP, GST, TOU-P, TOU-T, LIS, GAS, USSL). Base energy 0.16086 (GRS) with a single "adj" 0.147252. The 2018 GRS ended 2021-09-30; others have no enddate, so they are still flagged current.
  - 2021-10-01: GSS, GSP, GST with adj 0.160975 (Oct-Dec 2021 factors).
  - **2023-04-01: General Residential Service (GRS), label 615e10085457a34b401742b2. This is the latest residential entry.** Energy tiers: 0.04944 for the first 425 kWh, then 0.05564, each with adj 0.204473, plus a $4 fixed charge. The comment reads "Adjustments (April to June 2023) = FCA (0.146236) + PPCA (0.035997) + CILTA (0.007362) + SUBA-HH (0.014129) + SUBA-NHH (0.000749)". That matches the official Apr-May 2023 row exactly. Last revision 2023-05-17. No enddate.
  - 2025-08-01: GSP only (commercial), adj 0.198083. Its comment still describes Oct-Dec 2021 factors.
- Structure: `adj` is a single static number per tier. URDB has no quarterly time series, so every quarter needs a new rate record, and nobody has created one for residential since May 2023.
- Comparison with official:
  - URDB marginal: 0.260113 (above 425 kWh). Official marginal is 0.275741 for Jul-Sep 2026 and 0.328589 for Oct-Dec 2026.
  - URDB 800 kWh bill: $209.46, or 26.18 c/kWh. That is **-8.4%** vs Jul-Sep 2026 (28.57 c) and **-22.7%** vs Oct-Dec 2026 (33.86 c).
  - Fixed charge: $4 vs the current $8.
  - Base structure: URDB has two tiers; the current tariff is a flat 0.08648 per the FY2027 tariff book excerpt.
  - Missing components: EE (from 2024), Pension and Provisional (2025-Q2 2026).
- Verdict: **Stale/wrong.** It reflects Apr-Jun 2023 only and does not update on the effective date. Any app that pulls PR rates from URDB (ha-openei, the Emporia fallback) shows wrong numbers.

### 3.2 NREL (now NLR) Utility Rates API v3
- `developer.nrel.gov` no longer resolves (NREL was renamed). The working host is `developer.nlr.gov`.
- `GET /api/utility_rates/v3.json?lat=18.4655&lon=-66.1057` returns `utility_name: "Puerto Rico Electric Power Authority"` with `residential: "no data"`. Source: "Ventyx Research (2012)". The `address` parameter is no longer supported. Saved as `dl/audit/nlr_utility_rates_v3_*.json`.
- Verdict: **Not usable.** No PR residential value, and the data is from 2012.

### 3.3 EIA
- **Electric Power Monthly Table 5.6.A** (`dl/audit/eia_epm_5_6_a.html`, data for September 2026): rows are census divisions and the 50 states plus DC. **Puerto Rico is not in the table.** Not applicable.
- **EIA-861M monthly** (`dl/audit/eia861m_sales_revenue.xlsx`, sheet Monthly-States, state "PR"). Residential price, i.e. revenue divided by kWh, in c/kWh:

  | Month | Price (c/kWh) | Status |
  |---|---|---|
  | Sep 2026 | 25.15 | preliminary |
  | Aug 2026 | 26.36 | preliminary |
  | Jul 2026 | 25.19 | preliminary |
  | Jun 2026 | 28.99 | preliminary |
  | May 2026 | 26.49 | preliminary |
  | Apr 2026 | 25.98 | preliminary |
  | Mar 2026 | 24.37 | preliminary |
  | Feb 2026 | 24.69 | preliminary |
  | Jan 2026 | 23.74 | preliminary |
  | Dec 2025 | 25.41 | final |
  | Nov 2025 | 24.26 | final |
  | Oct 2025 | 27.36 | final |

  Comparison: in Jul-Sep 2026 EIA shows 25.2-26.4 c, vs the official unsubsidized 800 kWh average of 28.57 c and the official marginal of 27.57 c. EIA runs 2-3 c lower because it blends:
  - subsidized classes (LRS, RH3, RFR);
  - net-metering customers;
  - billing-cycle lag, since bills straddle quarters;
  - fixed charges spread over different consumption levels.

  It lags about 2 months: no Oct-Dec 2026 value yet. Verdict: **Partial.** Useful as a plausibility check, not as a tariff.
- **EIA PR territory profile** (https://www.eia.gov/states/RQ/analysis, last updated 2026-05-21): only says PR's 2024 average price ranked fifth-highest. No number. Not applicable.
- **EIA API v2** (`electricity/retail-sales`, stateid=PR): DEMO_KEY requests timed out, and the Firecrawl EIA provider returned 504. The bulk 861M file above holds the same data.

### 3.4 Rate aggregators and calculators
- **findenergy.com**, https://findenergy.com/providers/puerto-rico-electric-power-authority/
  - Reports "average residential electricity rate of 23.59 c/kWh" (PR average 24.54 c), with "sold ... in 2023". Published 2025-01-24.
  - This is an EIA-861 2023 annual average, under the obsolete PREPA name.
  - Verdict: **Stale.** -30% vs Oct-Dec 2026.
- **Solargrin**, https://solargrin.com/tools/ppco-puerto-rico-electricity-rates-cost-calculator.html
  - Pre-filled "LUMA Energy rate ($/kWh) 0.24", labelled "approximate average... planning estimate". No period, no components.
  - Verdict: **Wrong/stale** for 2026: -16% vs Jul-Sep, -29% vs Oct-Dec 2026.
- **Nectar Climate**, https://nectarclimate.com/rates/puerto-rico-electric-power-authority-prepa
  - C&I schedules only (GSS/GSP/GST/TOU/LIS), "Effective: August 28, 2025". Rider values are not given; it shows "the published tariff" placeholders.
  - It still says "Base rates have been largely unchanged since 2017" and that new FY2027 rates are "expected". The rate case is now decided and took effect 2026-07-01.
  - Verdict: **Partial/stale**, no residential. Its useful finding is confirmation that LUMA has no Green Button, EDI or billing API (as of May 2026).
- **MyPRTools**, https://myprtools.com/analizar-factura-luma
  - Client-side bill-PDF analyzer. It states it stores no tariffs ("La herramienta no tiene tarifas guardadas"); its example rates are explicitly invented.
  - Verdict: **Not applicable.** The FCA/PPCA/CILTA/SUBA/EE component model matches LUMA's bill.
- **FindEnergyRates** (MCP connector): PR is not covered; ZIP 00926 returns `no_data_for_scope`. Not applicable.
- **EnergySage, ChooseEnergy, ElectricChoice**: search snippets show only US-state tables built on EIA 5.6.A, which excludes PR. No PR value was found. Not applicable.

### 3.5 Mi LUMA (public, unauthenticated only)
- `https://miluma.lumapr.com/` is a Vite SPA bundle, `assets/index-Cft0n0UU.js`, saved under `dl/audit/miluma/`.
- API bases in the bundle: `api.miluma.lumapr.com/miluma-{api, app-config-api, bill-api, bill-objection-api, certification-api, email-api, notification-api, outage-api, payment-api, report-outage-api, servicecall-api}`.
- Every path found was extracted. The only unauthenticated data paths are:
  - `outage/regionsWithoutService`
  - `outage/municipality/towns`
  - `location/towns`, `location/sectors/{id}`
  - `serviceCall/jobTypes`
  - `certification/documentTypes`
- **There is no tariff, rate, factor or kWh-price endpoint.** Bill data sits behind `api/bill/*`, which needs auth. The only rate-related items are links to `lumapr.com/revision-tarifa-2025/` and `/rate-case-2025`.
- Plain curl to the outage API gets an Incapsula bot challenge.
- Verdict: **Dead end** for rates.

### 3.6 GitHub and Home Assistant community
- GitHub repo search finds nothing for: "LUMA Puerto Rico rate", "lumapr", "LUMA energy puerto rico", "puerto rico electricity rate", "PREPA tariff", "luma kwh", "aeepr", "mi luma". The only hits are outage trackers (jpadilla/tracking-luma-outages, williamrodz/luma_scrape, britok30/luma-outages-puerto-rico, etc.) and unrelated "Luma" e-commerce test projects.
- GitHub code search finds nothing for: "Tabla-de-Factores", "FCA PPCA LUMA", "CILTA SUBA", `"0.173576"`, `"0.114070"`, `"0.120158"`, `"0.04944" kwh`, `LUMA "PPCA"`, `"Puerto Rico" "cost_per_kwh"`. The numeric hits are all coincidental (game assets, datasets).
- jotaele44/aguayluz-pr references lumapr.com uploads, but it is a hydro/grid-status monitor, not rates.
- JnSbstnRivera/LUMA-SCANNER (a Windmar Home solar sizing tool, "validación cruzada contra la tarifa de LUMA") is now 404 or private, so it could not be audited.
- Home Assistant forum searches turned up only generic static-price recipes, nothing PR-specific. HA core has no PR price integration.
- The HACS integration `firstof9/ha-openei` pulls from URDB, so for PR it would show the stale 2023 GRS record (section 3.1).
- Verdict: **No community source exists to reuse.**

### 3.7 Consumer apps (from the vendor sub-agent, evidence URLs inline)
- **Emporia Vue**:
  - Rates come from "Emporia Verified" plans. Until a utility is verified, "the app may use rate data from the National Renewable Energy Laboratory (NREL) database ... may not reflect the most recent rate changes" (https://help.emporiaenergy.com/en/articles/14660606-emporia-verified-utility-plans, 2026-08-20).
  - The manual default is 13.2 c/kWh, the US national average (https://help.emporiaenergy.com/en/articles/9084323-cost-rate-settings).
  - For PR, the NREL/NLR API returns "no data" (3.2) and URDB is stale (3.1).
  - Verdict: **stale or wrong** unless the rate is set by hand. No evidence that LUMA is Emporia Verified.
- **FranklinWH**:
  - Uses its own predefined tariff catalog (endpoints `hes-gateway/terminal/tou/getTouCompanyListPageV2`, `getTariffListByCompanyId`, `getTariffDetailByIdV2`, seen in the reverse-engineered `franklinwh-cloud` client), with a custom-tariff fallback (https://www.franklinwh.com/support/overview/tariff-settings).
  - The manual (V2.23.0) says switching tariff with the utility "does not automatically update the tariff in your FranklinWH App".
  - Whether LUMA is in the catalog needs a login.
  - Verdict: **unknown coverage, no auto-update.** The quarterly value has to be pushed in by hand or by automation.
- **Tuya / Smart Life**: per-device price that the user configures (normal, tiered or peak-valley; Tuya MiniApp `getPeakValleyPrice` docs). No database. **Manual.**
- **Arcadia (Genability)**:
  - Covers the US, Canada and Mexico, and only "rates that appear in utility tariff books". LUMA publishes its quarterly factors outside the tariff book.
  - The public LSE search returned 401 without credentials.
  - Enphase's app uses Arcadia.
  - Verdict: **unknown**, and it would likely lag the quarterly factors.
- **UtilityAPI**: 15 supported utilities, none of them LUMA (https://utilityapi.com/coverage). Not applicable.
- **Electricity Maps**: PR zone exists (`TIER_C`); `has_day_ahead_price_license: false`. Carbon and generation mix only. Not applicable.
- **Tesla**: its own catalog (State -> Utility -> Plan), custom fallback, no tiered support, no auto-update.
- **Sense**: manual, from-bill, or an unnamed "location-based average".
- **SPAN**: utility list by ZIP, or manual.
- **SolarEdge**: no US rate DB found.
- All of the above are **unknown/manual** for PR.

## 4. Press and trackers

Gathered by the press sub-agent. NEPR resolution PDFs and their extracted text are saved in `dl/audit/press/nepr/`.

Official 800 kWh unsubsidized GRS figures from the NEPR resolutions (Table 2), used as the yardstick:

| Quarter | Bill | Avg c/kWh |
|---|---|---|
| Oct-Dec 2025 | $220.05 | 27.506 |
| Jan-Mar 2026 | $209.85 | 26.231 |
| Apr-Jun 2026 | $217.84 | 27.230 |
| Jul-Sep 2026 | $228.59 | 28.574 |
| Oct-Dec 2026 | $270.86 | 33.858 |

Before Jul 2026, the base works out to about $45.87 at 800 kWh, plus the Pension and Provisional riders. From Jul 2026 it is $8 + 0.08648/kWh, or $77.18 at 800 kWh.

### Oct-Dec 2026
- **El Nuevo Día** (Manuel Guillama Capella; published 2026-09-30 18:26, not Oct 1):
  - "Nueva tarifa récord: alza de 18% lleva el costo del kilovatio hora a 33.86 centavos". https://www.elnuevodia.com/noticias/locales/notas/nueva-tarifa-record-alza-de-18-lleva-el-costo-del-kilovatio-hora-a-336-centavos/
  - The visible text gives 33.86 c and +$42.27. The rest is paywalled, so the FCA figures cannot be checked in the article.
  - The URL slug says "336", which suggests an edited headline.
  - Verdict: **accurate** on the visible numbers.
  - The brief's "11.4070 -> 18.0736" comes from the NEPR R&O's introduction and other outlets. It is LUMA's *proposal*.
- **Metro PR, 2026-09-30**: LUMA asked 18.0736, NEPR set 17.3576; PPCA 5.1748 -> 4.5090; net +5.28; $228.59 -> $270.86. **Accurate.**
- **El Vocero, 2026-09-30**: net 5.2848, +18.5%. **Accurate.**
- **El Vocero, 2026-10-30 and 2026-11-21**: 33.85 c. **Accurate**; the figure is truncated, not rounded.
  - The 11-21 piece reports the NEPR president warning of about 37 c and +$24 in Jan 2027. That is a projection, not an approved factor.
- **Primera Hora, 2026-10-01**: +5.284 c, "about 33.8" from 28.57, $228.59 -> $270.86. **Accurate.** Its "LUMA asked 6.66" is the FCA-only request.
- **Presencia PR, 2026-10-01**: compares 5.28 approved with "6.666 solicitados". **Partial**: it sets a net figure against an FCA-only figure.
- **La Perla (Omar Alfonso), 2026-10-01**: 33.858 c, LUMA's 6.07 request cut by 0.78, FCA 11.4070 -> 18.0736 requested and 17.3576 approved. **Accurate**; the best breakdown found.
- **AP / Fortune / US News, 2026-10-01/02**: 33.86 c; $229 -> $271 at 800 kWh; +5.28. **Accurate.**
- **San Juan Daily Star, 2026-10-02**: FCA proposed 18.0736, approved 17.3576; "close to 34 c". **Accurate.**
- **LUMA press release, 2026-09-16**: +6.07 c, about $48/month. **Accurate as a proposal** (6.0689 x 800 = $48.55). It is not what was approved.
- **puertorico.com** cost-of-living page: $8 + $0.08648/kWh base; 33.86 c credited to "El Nuevo Día, October 1". **Numbers correct, date off by one day.** This is the likely origin of the brief's wording.
- **caborojo.com/luz**: $228.59 -> $270.86 is right, but it calls the July $10.75 a fuel adjustment. **Partial.**
- **CallMePower**, updated 2026-11-26: GRS $8 + 32.86 c/kWh.
  - Checks: 500 kWh = 8 + 500 x 0.32859 = $172.29, shown as $172. 1000 kWh = $336.59, shown as $337. 2000 kWh = $665.18, shown as $665.
  - This is the only tracker carrying the full marginal rider stack. **Accurate**, with the reuse caveats in section 2.

### Jul-Sep 2026
- **Primera Hora / El Nuevo Día / WAPA, 2026-06-30**: 27.23 -> 28.57 c, +1.34 c, +$10.75, +4.9%. **Totals accurate.**
- **Misattribution in El Nuevo Día's caption, CoquiList (2026-07-20, "28.5 c") and caborojo**: they credit the +1.34 c to fuel and purchased-power. **Partial/wrong.**
  - FCA+PPCA actually moved only +0.39 c, and the annual riders +0.45 c.
  - Pension (-1.9191 c) and Provisional (-1.4931 c) were removed.
  - The new permanent base ($8 + 8.648 c) added about $31 at 800 kWh.
- **LUMA's "2.34 c" request** is not confirmed. LUMA's 2026-06-15 filing (FCA 0.125935, PPCA 0.051170) implies about 2.47 c.

### Apr-Jun 2026
- **NotiCel / WAPA / TeleOnce, 2026-03-27**: $209.85 -> $217.84, +$0.00999/kWh. **Accurate.**
- **El Nuevo Día, 2026-03-27**: "+1 c". LUMA proposed FCA 0.116944; NEPR approved 0.116349. **Accurate.**

### Jan-Mar 2026
- **NotiCel / Primera Hora, 2025-12-20**: -$0.012739/kWh, $220.05 -> $209.85, -4.6%. **Accurate**, though the unit is garbled ("$0.26 centavos").
- **El Nuevo Día, 2025-12-20**: "-1.28 c". The factors give 1.2739 and NEPR's bill table 1.275. **Minor rounding error.**

### Oct-Dec 2025
- **NotiCel, 2025-09-30**: FCA 0.120158, PPCA 0.044523, FOS 0.021510; $0.27507/kWh. **Accurate.**
- **Metro PR, 2025-09-30**: same factors but "0.27507 centavos". **Unit error.**
- **La Perla, 2025-10-01**: 25.48 -> 27.51 c; Pension 1.9 c and Provisional 1.4 c. **Accurate.**
- **Inconsistency inside NEPR's own 2025-09-30 R&O**: Table 2 gives Aug-Sep 2025 as 0.25475, while its history table gives 0.2206. Do not rely on NEPR history tables without recomputing.

### Not found or no numbers
Sin Comillas, CB en Español, CPI, The Weekly Journal, News is my Business, NotiUno, Telemundo (no figures), globalpetrolprices (no PR), Statista, IEEFA and Cambio PR (no quarterly tracker).

Warning: one search tool's AI summary invented "5.01 c / 33.58 c" for El Nuevo Día, apparently from the "336" slug. Ignore it.

## 5. Implications for the endpoint
1. Source of truth: the LUMA Tabla XLSX for the riders. Validate it against the "APRUEBA los siguientes factores" table in the NEPR R&O (FCA/PPCA/FOS) and the annual-rider order (CILTA/SUBA/EE).
2. Never ingest LUMA motions ("Calculated/Proposed Factors"). Their values are not approved.
3. The residential (GRS) marginal rate is base energy plus FCA + PPCA + CILTA + SUBA-HH + SUBA-NHH + EE (+ Pension + Provisional while nonzero). FOS is excluded. Publish the $8 customer charge separately.
4. Self-test every quarter: recompute NEPR Table 2 (800 kWh unsubsidized GRS) and require a match to the cent. Today that is 8 + 800 x 0.328589 = $270.87 vs NEPR's $270.86 (rounding).
5. Optional cross-checks: the CallMePower page (current-quarter marginal) and EIA-861M (lagging blended average, expected 2-4 c lower).
