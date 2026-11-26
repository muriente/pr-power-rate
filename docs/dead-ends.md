# Dead ends: third-party PR rate source audit (2026-11-26)

Each entry gives what was tried, what it returned, and why it is a dead end. Do not retry these unless something changes.

## Rate databases and APIs
- **OpenEI URDB, by name and EIA ID.**
  - Queries tried: `ratesforutility=LUMA`, `LUMA Energy`, `Puerto Rico Electric Power Authority`; `eia=15376`; `address=San Juan, PR`; `lat=18.4655&lon=-66.1057`.
  - Result: all return `{"items":[]}`. PREPA is stored as "Puerto Rico Electric Pwr Authority" with eiaid 0, so only `country=PRI` or the exact abbreviated name finds it.
  - `country=PRI` returns 19 records. The newest residential record is from 2023-04-01.
- **OpenEI API v8 with DEMO_KEY**: HTTP 429 OVER_RATE_LIMIT, repeatedly. v7 worked once, and its output was byte-identical to the earlier cache.
- **NREL Developer API, `developer.nrel.gov`**: the host no longer resolves, even via public DNS. The NLR host `developer.nlr.gov` works.
- **NLR `utility_rates/v3`**: `residential: "no data"` for San Juan. The source is Ventyx 2012, and the `address` parameter has been removed.
- **EIA API v2 `electricity/retail-sales`, stateid=PR**: curl with DEMO_KEY timed out; the Firecrawl EIA provider returned 504. Use the bulk `eia861m/xls/sales_revenue.xlsx` instead, which worked.
- **EIA Electric Power Monthly Table 5.6.A**: Puerto Rico is not a row; only the 50 states, DC and census divisions are listed.
- **EIA state profile pages (`/state/print.php?sid=RQ`, `/states/RQ/analysis`)**: rendered with JS. Plain curl gets a shell page. Firecrawl rendered them, but they contain no price number, only "fifth-highest in 2024".
- **Arcadia / Genability public LSE search** (`api.genability.com/rest/public/lses?search=LUMA`): HTTP 401, credentials required. No public coverage list names LUMA or PREPA.
- **UtilityAPI**: LUMA is not in the supported-utilities list.
- **Electricity Maps**: has a PR zone but no price data (`has_day_ahead_price_license: false`). The API needs a token.
- **FindEnergyRates (MCP)**: ZIP 00926 is not mapped. PR is outside its coverage (13 deregulated states plus DC).

## LUMA / Mi LUMA
- **Mi LUMA SPA bundle (`miluma.lumapr.com/assets/index-*.js`)**:
  - All API bases and paths were enumerated. There is no tariff, rate or factor endpoint.
  - The public endpoints cover outages, location lists, service-call job types and certification document types only.
  - Bill data needs authentication and was not attempted.
- **`api.miluma.lumapr.com/miluma-outage-api/...` via plain curl**: Incapsula bot-challenge HTML. In any case it has no rate data.
- **LUMA Green Button / EDI / billing API**: none exists, according to Nectar Climate's May 2026 research. No first-party machine-readable rate feed was found other than the Tabla XLSX and the tariff-book PDF.

## GitHub / Home Assistant community
- **GitHub repo searches**: "LUMA Puerto Rico rate", "lumapr", "LUMA energy puerto rico", "puerto rico electricity rate", "PREPA tariff", "luma kwh", "aeepr", "mi luma". Results were outage trackers and unrelated "Luma" e-commerce QA projects only.
- **GitHub code searches**: "Tabla-de-Factores", "FCA PPCA LUMA", "CILTA SUBA", `"0.173576"`, `"0.114070"`, `"0.120158"`, `"0.04944" kwh`, `LUMA "PPCA"`, `"Puerto Rico" "cost_per_kwh"`, "lumapr tarifa kwh". None were relevant; the numeric hits are coincidental.
- **GitHub API rate limit**: hit once during code search (HTTP 403). Searches done after waiting returned no results either.
- **jotaele44/aguayluz-pr, jotaele44/spiderweb-pr**: reference lumapr.com uploads, but the projects are hydro, grid-status and OSINT, not rates.
- **JnSbstnRivera/LUMA-SCANNER**: the repo is now 404 or private, so its "validation against the LUMA tariff" could not be inspected.
- **community.home-assistant.io**:
  - Searched for "Puerto Rico" with LUMA or PREPA and energy cost. The only hit was an unrelated smart-lights thread.
  - Generic static-price recipes exist; nothing PR-specific.
- **HACS `firstof9/ha-openei`**: exists, but it is backed by URDB, so the data is stale (2023).

## Consumer apps
- **`community.emporiaenergy.com`**: the domain does not resolve. A search snippet mentioned a user whose OpenEI-sourced rate was dated 2018; it could not be opened.
- **FranklinWH US app manual** (`/document/download/franklinwh-app-user-manual-en`): 404. Only the AU edition (V2.23.0) was downloadable.
- **FranklinWH tariff catalog**: needs a login, so it was not attempted.
- **Tesla rate-plan catalog**: needs a login, so it was not attempted. No forum post shows LUMA in the list.
- **Arcadia docs `site:docs.arcadia.com` for Puerto Rico or territories**: 0 results.
- **Solar design tools (Aurora, OpenSolar, Solargraf) with PR tariffs**: nothing found.

## Aggregator sites (exist, but numbers stale or absent)
- **findenergy.com**: 23.59 c/kWh from 2023 EIA data, published 2025-01-24.
- **Solargrin calculator**: hard-coded $0.24/kWh.
- **Nectar Climate**: C&I only, no rider values, and it predates the FY2027 rates.
- **EnergySage, ChooseEnergy, ElectricChoice**: US-state tables built on EIA 5.6.A, so PR is excluded.

## Press
- **El Nuevo Día**: the article body is paywalled; only the headline and lede are readable.
- **Blocked or failed fetches**:
  - El Vocero: HTTP 429 on direct fetch. Firecrawl worked.
  - La Perla: HTTP 403 to WebFetch. Firecrawl worked.
  - NotiCel article of 2026-09-30: timed out.
- **No PR rate figures or quarterly tracker found at**: Sin Comillas, CB en Español, CPI, The Weekly Journal, Jornada, News is my Business, NotiUno, Telemundo PR, globalpetrolprices, Statista, IEEFA, Cambio PR, latestcost.com.
- **Metro PR, 2026-06-30 and 2026-11-18**: no rate figures.
- **Search-engine AI summaries**: one invented "5.01 c / 33.58 c" for El Nuevo Día. Never trust AI-generated search answers for rate figures.

## Scraping trap (not a dead end, but a hazard)
LUMA's quarterly motions filed at energia.pr.gov contain proposed factors that NEPR then changes:
- Oct-Dec 2026: proposed FCA 0.180736, approved 0.173576.
- Jul-Sep 2026: proposed FCA 0.125935, approved 0.114070.

A scraper must read only the NEPR Resolución y Orden ("APRUEBA los siguientes factores") or the LUMA Tabla XLSX, never the motion. The mission brief's "FCA 18.0736" is the rejected proposal.
