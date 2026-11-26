# pr-power-rate

The current Puerto Rico (LUMA) residential electricity rate as a free public JSON endpoint. It is rebuilt every
hour from LUMA's official *Tabla de Factores de Ajustes*, and every factor is matched digit-for-digit against the
Energy Bureau (NEPR/PREB) Resolution and Order that set it.

| | |
|---|---|
| **Endpoint** | https://muriente.github.io/pr-power-rate/api/v1/current.json |
| Plain number | https://muriente.github.io/pr-power-rate/api/v1/price.txt |
| History (since May 2019) | https://muriente.github.io/pr-power-rate/api/v1/history.json |
| Human page | https://muriente.github.io/pr-power-rate/ |
| Schema | [docs/schema.md](docs/schema.md) |

Oct–Dec 2026, GRS (standard residential, non-subsidized): **$0.328588/kWh** plus **$8.00/month**.

| Component | $/kWh | Source |
|---|---|---|
| Base energy charge | 0.086480 | NEPR-AP-2023-0003 final rate order (2026-04-15), App. B |
| FCA (fuel) | 0.173576 | NEPR R&O 2026-09-30 |
| PPCA (purchased power) | 0.045090 | NEPR R&O 2026-09-30 |
| CILTA | 0.007386 | NEPR R&O 2026-06-30 |
| SUBA-HH | 0.014338 | NEPR R&O 2026-06-30 |
| SUBA-NHH | 0.000865 | NEPR R&O 2026-06-30 |
| EE | 0.000853 | NEPR R&O 2026-06-30 |
| **Total** | **0.328588** | |

Reconciliation to the press figure of 33.86 ¢/kWh: that number is the all-in average for an 800 kWh bill,
fixed charge included ($8 + 800 × $0.328588 = $270.87, or 33.86 ¢/kWh). NEPR's own Table 2 shows $270.86, a
one-cent difference from rounding its $42.27 delta. The "18.0736 ¢ FCA" in some reports was LUMA's *proposed*
value. NEPR cut it to 17.3576 in the same order, after deferring $17.65 M of gas-shortfall costs and disallowing
a 1.51% bad-debt markup. FOS (0.020822) is a credit for qualifying subsidized customers under 500 kWh, so it is
published in `not_included` and never added to the price. Full evidence: [docs/official-sources.md](docs/official-sources.md).

## Why this exists

No existing source was accurate. OpenEI URDB still lists 2023 PREPA factors on the old base rate, which comes
out 22.7% low for Oct–Dec 2026. The Home Assistant OpenEI integration, and Emporia's fallback, read that same
data. EIA lags by months and blends revenue. Mi LUMA has no rate API. See [docs/source-audit.md](docs/source-audit.md).

## Consumers

### Home Assistant

```yaml
rest:
  - resource: https://muriente.github.io/pr-power-rate/api/v1/current.json
    scan_interval: 3600
    sensor:
      - name: "PR electricity price"
        unique_id: pr_power_rate_price
        value_template: "{{ value_json.price_usd_per_kwh }}"
        unit_of_measurement: "USD/kWh"
        state_class: measurement
        availability: "{{ value_json is defined and value_json.effective_end >= now().date() | string }}"
        json_attributes: [fixed_charge_usd_per_month, effective_start, effective_end, period_label, upcoming, verification]
```

Use `sensor.pr_electricity_price` as the grid import price in the Energy dashboard ("Use an entity with current
price"). This was verified on a fresh Home Assistant 2026.11.3: the sensor read 0.328588 USD/kWh, and the Energy
cost sensor charged $3.28588 for 10 kWh. Juan's instance consumes it through `muriente/home-lab` PR #168
(`config/packages/tariff.yaml`), which writes the existing tariff helpers from this endpoint.

### Apps without a rate URL (Emporia, FranklinWH, Tuya)

These apps only take a typed number, so `host/apply-apps` types it in over ADB on the phone whenever the price
changes. See [Operations](#operations).

### Anything else

Read `price_usd_per_kwh` from `current.json`, or fetch `price.txt`. CORS is open (`Access-Control-Allow-Origin: *`).
After `effective_end`, treat the value as stale.

## How it works

```
LUMA tariffs page ──► Tabla-de-Factores*.xlsx ──► prrate/luma.py (parse; rows newest first, $/kWh)
                                                        │
NEPR docket NEPR-MI-2020-0001 ──► R&O PDFs ──► prrate/nepr.py (each factor, 6 decimals, must appear in the
                                                        │        order LUMA cites: quarterly FCA/PPCA/FOS,
data/tariff.json (base GRS tariff, by hand) ───────────►│        annual CILTA/SUBA/EE)
                                                        ▼
                         prrate/build.py ──► site/api/v1/{current,history}.json, price.txt, index.html
```

The build refuses to publish when no LUMA row covers today (exit 2), when any factor fails to match its NEPR order
(exit 3), when no base tariff covers today (exit 4), or when a sanity range fails (exit 5). The live site keeps the
last verified data and stays self-describing through `effective_end`.

## Operations

- **Publisher:** `host/publish` runs hourly on the Mac mini (launchd `com.muriente.pr-power-rate`, log
  `~/Library/Application Support/pr-power-rate/logs/publish.log`). It builds from live sources, pushes `site/` to the
  `gh-pages` branch (GitHub Pages serves it), archives each new LUMA workbook under `data/luma/archive/`, and
  opens a `pipeline` issue on failure, closing it on recovery. GitHub Actions cannot run on this account right now
  ("recent account payments have failed"). `.github/workflows/update.yml` is the drop-in replacement: when Actions
  works again, enable it, switch Pages to "GitHub Actions" and unload the launchd job. Never run both.
- **Quarterly cycle:** LUMA files proposed factors about two weeks before a quarter, and NEPR orders the final ones
  in the last days of the quarter (Jan, Apr, Jul, Oct). Next filing: Jan–Mar 2027, due 2026-12-14. No action is
  needed: the hourly job picks up the new workbook, verifies it against the new order, and the price switches
  at 00:00 America/Puerto_Rico on the first day of the quarter. Never use LUMA's proposed numbers or the
  workbook's lower "Parámetros" block.
- **Device apps:** after each publish, `host/apply-apps` compares the price in force with the last value applied
  to each app (`~/Library/Application Support/pr-power-rate/applied.json`). When they differ, it types the new rate into the
  apps on the Pixel. The Pixel is USB-attached to the MacBook Air, so adb runs there over SSH. While Hotplug
  holds `/private/tmp/hotplug-air-pixel-bench.lock` the run is skipped and retried the next hour.
- **Base tariff:** `data/tariff.json` holds the GRS base by fiscal year. FY2028 ($16.00 + $0.06275, from
  2027-07-01) is entered as ordered on 2026-04-15. Re-verify it against the FY2028 tariff book before July 2027.
- **Tests:** `python -m unittest discover -s tests` (offline; it reproduces NEPR's bill table for two quarters).
- **Local build:** `pip install -r requirements.txt && python -m prrate.build --out site`.

Unofficial and community-maintained. Every number links to the official LUMA or NEPR document it came from.
