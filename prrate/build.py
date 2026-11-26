"""Build the public endpoint (site/api/v1/*.json) from LUMA's factor table, the base tariff and NEPR orders.

Usage:
  python -m prrate.build [--xlsx PATH] [--offline] [--today YYYY-MM-DD] [--out site]

Without --xlsx it discovers the workbook on LUMA's tariffs page and archives a copy under data/luma/archive/.
Exit codes: 0 built and verified; 2 no factor row covers today (stale source); 3 NEPR cross-check failed;
4 no base tariff covers today; 5 sanity check failed. On any non-zero exit nothing is written to --out.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import shutil
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from . import luma, nepr

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("America/Puerto_Rico")
SCHEMA = "https://github.com/muriente/pr-power-rate/blob/main/docs/schema.md"
PUBLIC_BASE = "https://muriente.github.io/pr-power-rate"

COMPONENT_NAMES = {
    "base_energy": "Base energy charge (cargo por energía, GRS)",
    "FCA": "Fuel Charge Adjustment (Cláusula de Compra de Combustible)",
    "PPCA": "Purchased Power Charge Adjustment (Cláusula de Compra de Energía)",
    "CILTA": "CILT adjustment (Contribución en Lugar de Impuestos, municipios)",
    "SUBA_HH": "Subsidies adjustment, households (SUBA-HH)",
    "SUBA_NHH": "Subsidies adjustment, non-households (SUBA-NHH)",
    "EE": "Energy Efficiency rider (Cláusula de Eficiencia Energética)",
    "PENSION": "Pension costs rider",
    "PROVISIONAL": "Provisional rate rider",
    "FOS": "Fuel subsidy clause (Cláusula de Subsidio de Combustible)",
}


class BuildError(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code


def r6(x: float) -> float:
    return round(x + 0.0, 6)


def base_for(tariff: dict, day: dt.date) -> dict:
    for b in tariff["base_tariffs"]:
        if b["effective_start"] <= day.isoformat() <= (b["effective_end"] or "9999-12-31"):
            return b
    raise BuildError(4, f"no base tariff in data/tariff.json covers {day}")


def price_for(period: dict, base: dict, tariff: dict) -> dict:
    f = period["factors_usd_per_kwh"]
    comps = {"base_energy": base["energy_charge_usd_per_kwh"]}
    for k in tariff["residential_components"]:
        # NEPR orders state factors to six decimals; LUMA's workbook sometimes carries unrounded formulas
        # (e.g. CILTA 0.00738628...). Bills use the ordered six-decimal value.
        comps[k] = r6(f.get(k) or 0.0)
    marginal = sum(comps.values())
    fixed = base["fixed_charge_usd_per_month"]
    averages = {str(k): r6(marginal + fixed / k) for k in tariff["benchmark_kwh"]}
    return {"components": comps, "marginal": marginal, "fixed": fixed, "averages": averages}


def sanity(period: dict, price: dict) -> None:
    f = period["factors_usd_per_kwh"]
    for k, v in f.items():
        if v is not None and not (-0.2 < v < 1.0):
            raise BuildError(5, f"factor {k}={v} outside the plausible $/kWh range")
    if f.get("SUBA") is not None and abs(f["SUBA"] - (f["SUBA_HH"] + f["SUBA_NHH"])) > 1e-6:
        raise BuildError(5, f"SUBA {f['SUBA']} != SUBA-HH + SUBA-NHH")
    if not (0.10 < price["marginal"] < 0.80):
        raise BuildError(5, f"marginal price {price['marginal']} $/kWh is implausible")


def component_block(price: dict, period: dict, base: dict, verification: dict, workbook_url: str) -> dict:
    out = {}
    for k, v in price["components"].items():
        if k == "base_energy":
            src = base["sources"][0]["url"]
        elif k in nepr.QUARTERLY:
            src = (verification.get("quarterly") or {}).get("url") or workbook_url
        elif k in nepr.ANNUAL:
            src = (verification.get("annual") or {}).get("url") or workbook_url
        else:
            src = workbook_url
        out[k] = {"name": COMPONENT_NAMES.get(k, k), "usd_per_kwh": r6(v), "source": src}
    return out


def build(args) -> dict:
    tariff = json.loads((ROOT / "data/tariff.json").read_text())
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(TZ).date()
    now_iso = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    # 1. LUMA factor table
    if args.xlsx:
        xlsx_path = Path(args.xlsx)
        data = xlsx_path.read_bytes()
        workbook_url = args.workbook_url or luma.TARIFF_PAGE
    else:
        page = luma.fetch(luma.TARIFF_PAGE).decode("utf-8", errors="ignore")
        workbook_url = luma.discover_workbook_url(page)
        data = luma.fetch(workbook_url)
        archive = ROOT / "data/luma/archive" / f"{luma.sha256(data)[:16]}.xlsx"
        if not archive.exists():
            archive.write_bytes(data)
        xlsx_path = archive
    digest = luma.sha256(data)
    periods = luma.parse_workbook(xlsx_path)

    current = luma.select_current(periods, today)
    if current is None:
        newest = periods[0]
        raise BuildError(2, f"LUMA table has no row covering {today}; newest row is {newest['label']} "
                            f"({newest['start']}..{newest['end']}). Waiting for LUMA/NEPR to publish.")
    base = base_for(tariff, today)
    price = price_for(current, base, tariff)
    sanity(current, price)

    # 2. NEPR cross-check (the order cited by LUMA must state the same factors)
    if args.offline:
        verification = {"quarterly": None, "annual": None, "status": "not-checked (offline build)"}
    else:
        annual = nepr.annual_row_for(periods, current)
        verification = nepr.verify_period(current, annual, nepr.fetch_docket())
        ok = verification["quarterly"]["ok"] and (verification["annual"] or {}).get("ok", False)
        if not ok:
            raise BuildError(3, "NEPR cross-check failed: " + json.dumps(verification))
        verification["status"] = "verified"

    # 3. History (every LUMA row, with a price wherever a base tariff covers that row's start)
    history = []
    for p in periods:
        start = dt.date.fromisoformat(p["start"])
        try:
            b = base_for(tariff, start)
            pr = price_for(p, b, tariff)
            priced = {"price_usd_per_kwh": r6(pr["marginal"]), "fixed_charge_usd_per_month": pr["fixed"]}
        except BuildError:
            priced = {"price_usd_per_kwh": None, "fixed_charge_usd_per_month": None,
                      "note": "base tariff for this period not modeled; factors only"}
        history.append({"label": p["label"], "effective_start": p["start"], "effective_end": p["end"],
                        "nepr_order_date": p["order_date"], **priced,
                        "factors_usd_per_kwh": {k: (r6(v) if v is not None else None)
                                                for k, v in p["factors_usd_per_kwh"].items()}})

    upcoming = None
    later = [p for p in periods if p["start"] > current["end"]]
    if later:
        nxt = min(later, key=lambda p: p["start"])
        try:
            nb = base_for(tariff, dt.date.fromisoformat(nxt["start"]))
            npr = price_for(nxt, nb, tariff)
            upcoming = {"effective_start": nxt["start"], "effective_end": nxt["end"], "period_label": nxt["label"],
                        "nepr_order_date": nxt["order_date"], "price_usd_per_kwh": r6(npr["marginal"]),
                        "fixed_charge_usd_per_month": npr["fixed"],
                        "note": "Already published by LUMA; becomes current on effective_start."}
        except BuildError:
            upcoming = None

    fos = current["factors_usd_per_kwh"].get("FOS")
    doc = {
        "schema": SCHEMA,
        "utility": "LUMA Energy, Puerto Rico",
        "rate_class": tariff["rate_class"],
        "rate_class_name": tariff["rate_class_name"],
        "currency": "USD",
        "price_usd_per_kwh": r6(price["marginal"]),
        "price_cents_per_kwh": round(price["marginal"] * 100, 4),
        "price_note": "Marginal price of one more kWh: base energy charge plus every per-kWh rider. "
                      "The monthly fixed charge is separate (fixed_charge_usd_per_month).",
        "fixed_charge_usd_per_month": price["fixed"],
        "average_usd_per_kwh_including_fixed_charge": price["averages"],
        "effective_start": current["start"],
        "effective_end": current["end"],
        "period_label": current["label"],
        "upcoming": upcoming,
        "components": component_block(price, current, base, verification, workbook_url),
        "not_included": {
            "FOS": {"name": COMPONENT_NAMES["FOS"], "usd_per_kwh": r6(fos) if fos is not None else None,
                    "why": tariff["excluded_components"]["FOS"]},
            "other": "Optional discounts (e.g. direct debit) and riders without an ordered factor are not included.",
        },
        "sources": {
            "luma_factor_table": {"url": workbook_url, "sha256": digest, "page": luma.TARIFF_PAGE},
            "nepr_quarterly_order": (verification.get("quarterly") or {}).get("url"),
            "nepr_annual_riders_order": (verification.get("annual") or {}).get("url"),
            "base_tariff": base["sources"],
        },
        "verification": verification,
        "generated_at": now_iso,
        "checked_on": today.isoformat(),
        "endpoints": {
            "current": f"{PUBLIC_BASE}/api/v1/current.json",
            "history": f"{PUBLIC_BASE}/api/v1/history.json",
            "plain_text_price": f"{PUBLIC_BASE}/api/v1/price.txt",
        },
    }
    return {"current": doc, "history": history}


def write_site(result: dict, out: Path) -> None:
    tmp = out.with_name(out.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    api = tmp / "api/v1"
    api.mkdir(parents=True)
    cur = result["current"]
    (api / "current.json").write_text(json.dumps(cur, indent=2, ensure_ascii=False) + "\n")
    (api / "history.json").write_text(json.dumps({"schema": SCHEMA, "generated_at": cur["generated_at"],
                                                  "periods": result["history"]}, indent=2, ensure_ascii=False) + "\n")
    (api / "price.txt").write_text(f"{cur['price_usd_per_kwh']:.6f}\n")
    (tmp / "index.html").write_text(render_html(cur))
    (tmp / ".nojekyll").write_text("")
    if out.exists():
        shutil.rmtree(out)
    tmp.rename(out)


def render_html(cur: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(k)}</td><td>{html.escape(c['name'])}</td><td class=n>{c['usd_per_kwh']*100:.4f}</td>"
        f"<td><a href=\"{html.escape(c['source'])}\">source</a></td></tr>"
        for k, c in cur["components"].items())
    avgs = " · ".join(f"{k} kWh: {v*100:.2f}¢" for k, v in cur["average_usd_per_kwh_including_fixed_charge"].items())
    v = cur["verification"]
    vq, va = v.get("quarterly") or {}, v.get("annual") or {}
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Puerto Rico electricity rate (LUMA): {cur['price_cents_per_kwh']:.2f}¢/kWh</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#111}}
.big{{font-size:3rem;font-weight:700}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:.3rem .5rem;text-align:left}}
.n{{text-align:right;font-variant-numeric:tabular-nums}}code{{background:#f3f3f3;padding:.1rem .3rem}}small{{color:#555}}</style></head><body>
<h1>Puerto Rico residential electricity rate (LUMA, GRS)</h1>
<p class=big>{cur['price_cents_per_kwh']:.4f}¢ / kWh</p>
<p>Effective <b>{cur['effective_start']}</b> to <b>{cur['effective_end']}</b> ({html.escape(cur['period_label'])}).
Plus a fixed charge of <b>${cur['fixed_charge_usd_per_month']:.2f}/month</b>. All-in average including the fixed charge: {avgs}.</p>
<table><tr><th>Key</th><th>Component</th><th class=n>¢/kWh</th><th>Official source</th></tr>
{rows}
<tr><td></td><td><b>Total per kWh</b></td><td class=n><b>{cur['price_cents_per_kwh']:.4f}</b></td><td></td></tr></table>
<p><small>Not included: FOS {(cur['not_included']['FOS']['usd_per_kwh'] or 0)*100:.4f}¢/kWh — {html.escape(cur['not_included']['FOS']['why'])}</small></p>
<h2>Verification</h2>
<p>Factors parsed from LUMA's <a href="{html.escape(cur['sources']['luma_factor_table']['url'])}">Tabla de Factores</a>
(sha256 <code>{cur['sources']['luma_factor_table']['sha256'][:16]}…</code>) and matched digit-for-digit against the Energy Bureau orders:
quarterly <a href="{html.escape(vq.get('url') or '#')}">{html.escape(vq.get('order_date') or 'n/a')}</a>,
annual riders <a href="{html.escape(va.get('url') or '#')}">{html.escape(va.get('order_date') or 'n/a')}</a>.
Status: <b>{html.escape(v.get('status', 'unknown'))}</b>. Checked {cur['checked_on']}, generated {cur['generated_at']}.</p>
<h2>API</h2><ul>
<li><a href="api/v1/current.json"><code>/api/v1/current.json</code></a> — current price, components, sources</li>
<li><a href="api/v1/history.json"><code>/api/v1/history.json</code></a> — every quarter LUMA has published since 2019</li>
<li><a href="api/v1/price.txt"><code>/api/v1/price.txt</code></a> — just the $/kWh number</li></ul>
<p><small>Unofficial, community-maintained; updated automatically from official LUMA and NEPR publications.
Code: <a href="https://github.com/muriente/pr-power-rate">github.com/muriente/pr-power-rate</a></small></p>
</body></html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xlsx")
    ap.add_argument("--workbook-url")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--today")
    ap.add_argument("--out", default=str(ROOT / "site"))
    args = ap.parse_args(argv)
    try:
        result = build(args)
    except BuildError as exc:
        print(f"build: {exc}", file=sys.stderr)
        return exc.code
    write_site(result, Path(args.out))
    cur = result["current"]
    print(f"build: {cur['price_usd_per_kwh']:.6f} USD/kWh ({cur['period_label']}), "
          f"verification={cur['verification'].get('status')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
