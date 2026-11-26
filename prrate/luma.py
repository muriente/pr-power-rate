"""Discover, download and parse LUMA's official "Tabla de Factores de Ajustes" workbook.

LUMA publishes the quarterly reconciliation factors (FCA, PPCA, FOS, CILTA, SUBA, EE, ...) as an XLSX linked
from https://lumapr.com/tarifas-vigentes-del-servicio-electrico-en-puerto-rico/ . The header says "¢/kWh" but the
cells hold $/kWh (e.g. FCA 0.173576 = 17.3576 ¢/kWh); this module returns $/kWh.
"""
from __future__ import annotations

import calendar
import datetime as dt
import hashlib
import re
import unicodedata
import urllib.request
from pathlib import Path

TARIFF_PAGE = "https://lumapr.com/tarifas-vigentes-del-servicio-electrico-en-puerto-rico/"
USER_AGENT = "pr-power-rate/1.0 (+https://github.com/muriente/pr-power-rate)"

MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

# Normalized (lower-case) header text -> factor key.
HEADER_EXACT = {
    "fca": "FCA", "ppca": "PPCA", "fos": "FOS", "cilta": "CILTA", "suba-hh": "SUBA_HH", "suba-nhh": "SUBA_NHH",
    "ee": "EE", "pension costs": "PENSION", "provisional rider": "PROVISIONAL",
}
HEADER_PREFIX = {"suba (": "SUBA"}  # the 2019-20 TUP column is historical with ambiguous units: not parsed


def clean(value):
    """Strip zero-width spaces, NBSP and stray whitespace from a cell value."""
    if isinstance(value, str):
        value = value.replace("​", "").replace("\xa0", " ").replace("﻿", "")
        value = re.sub(r"\s+", " ", value).strip()
    return value


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def discover_workbook_url(page_html: str) -> str:
    """Return the factor-table XLSX URL linked from the LUMA tariffs page (newest upload folder wins)."""
    urls = re.findall(r"https://lumapr\.com/wp-content/uploads/\d{4}/\d{2}/[^\"'<>\s]*Factores[^\"'<>\s]*\.xlsx", page_html)
    if not urls:
        raise ValueError("no Tabla de Factores .xlsx link found on the LUMA tariffs page")
    return sorted(set(urls), key=lambda u: re.search(r"/uploads/(\d{4}/\d{2})/", u).group(1))[-1]


def parse_period(label: str) -> tuple[dt.date, dt.date]:
    """'octubre a diciembre 2026' -> (2026-10-01, 2026-12-31); 'julio 2025' -> (2025-07-01, 2025-07-31)."""
    text = unicodedata.normalize("NFKD", clean(label).lower()).encode("ascii", "ignore").decode()
    text = text.replace("*", "").strip()
    year_m = re.search(r"(\d{4})", text)
    if not year_m:
        raise ValueError(f"no year in period label {label!r}")
    year = int(year_m.group(1))
    months = [MONTHS[w] for w in re.findall(r"[a-z]+", text) if w in MONTHS]
    if not months:
        raise ValueError(f"no month in period label {label!r}")
    first, last = months[0], months[-1]
    start = dt.date(year, first, 1)
    end = dt.date(year, last, calendar.monthrange(year, last)[1])
    if end < start:
        raise ValueError(f"period crosses a year boundary, unsupported: {label!r}")
    return start, end


def parse_date(value) -> dt.date | None:
    value = clean(value)
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", value)
        if m:
            return dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    return None


def to_number(value) -> float | None:
    value = clean(value)
    if value in (None, "", "-"):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def header_key(text: str) -> str | None:
    t = clean(text or "").lower()
    if t in HEADER_EXACT:
        return HEADER_EXACT[t]
    return next((k for prefix, k in HEADER_PREFIX.items() if t.startswith(prefix)), None)


def parse_workbook(path: Path) -> list[dict]:
    """Parse the first factor table (rows under the 'Periodo' header) into a list of period dicts, newest first."""
    import openpyxl  # imported lazily so the rest of the package works without it

    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.worksheets[0]
    rows = [[clean(c) for c in r] for r in ws.iter_rows(values_only=True)]
    header_idx = None
    for i, r in enumerate(rows):
        if any(isinstance(c, str) and c == "Periodo" for c in r) and any(isinstance(c, str) and c.upper() == "FCA" for c in r):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("factor table header (Periodo ... FCA) not found")
    header = rows[header_idx]
    col_period = header.index("Periodo")
    col_order = next(i for i, c in enumerate(header) if isinstance(c, str) and c.startswith("Resoluci"))
    cols = {}
    for i, c in enumerate(header):
        k = header_key(c) if isinstance(c, str) else None
        if k and k not in cols:
            cols[k] = i
    for required in ("FCA", "PPCA", "CILTA", "SUBA_HH", "SUBA_NHH"):
        if required not in cols:
            raise ValueError(f"factor table is missing column {required}; header={header}")

    periods = []
    for r in rows[header_idx + 1:]:
        label = r[col_period] if col_period < len(r) else None
        if not isinstance(label, str) or not label or label.startswith("*") or not re.search(r"\d{4}", label):
            break  # end of the first table (footnote or blank row)
        start, end = parse_period(label)
        factors = {k: to_number(r[i]) if i < len(r) else None for k, i in cols.items()}
        periods.append({
            "label": label,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "order_date": (d.isoformat() if (d := parse_date(r[col_order])) else None),
            "factors_usd_per_kwh": factors,
        })
    if not periods:
        raise ValueError("factor table has no data rows")
    return periods


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def select_current(periods: list[dict], day: dt.date) -> dict | None:
    """The row whose period covers `day`; when rows overlap, the latest NEPR order wins."""
    hits = [p for p in periods if p["start"] <= day.isoformat() <= p["end"]]
    if not hits:
        return None
    return max(hits, key=lambda p: (p["order_date"] or "", p["start"]))
