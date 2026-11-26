"""Cross-check LUMA's factor table against the Energy Bureau (NEPR/PREB) Resolution and Order that set it.

The quarterly factors (FCA, PPCA, FOS) are ordered in docket NEPR-MI-2020-0001 a few days before each quarter;
the annual riders (CILTA, SUBA-HH, SUBA-NHH, EE) are ordered once a year for July-June in the same docket.
LUMA's table names the order date of every row, so we locate that order's PDF on the docket page and require
every factor, printed to six decimals, to appear in the order's text.
"""
from __future__ import annotations

import io
import re

DOCKET_PAGE = "https://energia.pr.gov/numero_orden/nerp-mi-2020-0001/"
BROWSER_UA = "Mozilla/5.0 (compatible; pr-power-rate/1.0; +https://github.com/muriente/pr-power-rate)"
QUARTERLY = ("FCA", "PPCA", "FOS")
ANNUAL = ("CILTA", "SUBA_HH", "SUBA_NHH", "EE")


def docket_order_urls(docket_html: str) -> dict[str, list[str]]:
    """Map YYYYMMDD -> Resolution-and-Order PDF URLs in docket MI-2020-0001 (attachments/letters excluded)."""
    pattern = (r"https://energia\.pr\.gov/wp-content/uploads/sites/7/\d{4}/\d{2}/"
               r"(\d{8})-MI20200001-(?:Resolucion-y-Orden|Resolution-and-Order)(?:-\d+)?\.pdf")
    out: dict[str, list[str]] = {}
    for m in re.finditer(pattern, docket_html):
        out.setdefault(m.group(1), [])
        if m.group(0) not in out[m.group(1)]:
            out[m.group(1)].append(m.group(0))
    return out


def pdf_text(data: bytes) -> str:
    from pypdf import PdfReader  # lazy import

    reader = PdfReader(io.BytesIO(data))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def fetch_docket() -> str:
    import urllib.request

    req = urllib.request.Request(DOCKET_PAGE, headers={"User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def fetch_pdf(url: str) -> bytes:
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def check_values(text: str, factors: dict[str, float], keys: tuple[str, ...]) -> dict[str, bool]:
    """True per key when the factor, formatted to six decimals, appears in the order text."""
    flat = re.sub(r"\s+", "", text)
    return {k: (f"{factors[k]:.6f}" in flat) for k in keys if factors.get(k) is not None}


def verify_period(period: dict, annual_period: dict | None, docket_html: str, fetch=fetch_pdf) -> dict:
    """Verify one LUMA period row (and its fiscal year's annual riders) against the NEPR orders it cites."""
    orders = docket_order_urls(docket_html)
    result = {"quarterly": None, "annual": None}

    def one(row: dict, keys: tuple[str, ...]) -> dict:
        date = (row.get("order_date") or "").replace("-", "")
        urls = orders.get(date, [])
        if not urls:
            return {"order_date": row.get("order_date"), "url": None, "matched": {}, "ok": False,
                    "note": "order PDF for this date not found on the NEPR docket page"}
        last_err = None
        for url in urls:
            try:
                matched = check_values(pdf_text(fetch(url)), row["factors_usd_per_kwh"], keys)
            except Exception as exc:  # network/PDF errors are reported, never hidden
                last_err = f"{type(exc).__name__}: {exc}"
                continue
            if matched and all(matched.values()):
                return {"order_date": row["order_date"], "url": url, "matched": matched, "ok": True}
            last_err = f"values not all found in {url}: {matched}"
        return {"order_date": row.get("order_date"), "url": urls[0], "matched": {}, "ok": False, "note": last_err}

    result["quarterly"] = one(period, QUARTERLY)
    if annual_period is not None:
        result["annual"] = one(annual_period, ANNUAL)
    return result


def annual_row_for(periods: list[dict], period: dict) -> dict | None:
    """The row that set this fiscal year's annual riders: the earliest row of the same July-June year whose
    annual riders equal this row's (LUMA repeats them every quarter)."""
    start = period["start"]
    fy_start_year = int(start[:4]) if int(start[5:7]) >= 7 else int(start[:4]) - 1
    fy_lo, fy_hi = f"{fy_start_year}-07-01", f"{fy_start_year + 1}-06-30"
    same = [p for p in periods if fy_lo <= p["start"] <= fy_hi
            and all(abs((p["factors_usd_per_kwh"].get(k) or 0) - (period["factors_usd_per_kwh"].get(k) or 0)) < 1e-9
                    for k in ANNUAL)]
    return min(same, key=lambda p: p["start"]) if same else None

