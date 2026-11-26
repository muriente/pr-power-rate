"""Per-app flows: type the rate in force into an Android app, then read it back after an app restart.

Mapped on 2026-11-26 against the apps on the Pixel 11 Pro (serial 66160DLKX004F1):
- FranklinWH 2.x: Settings tab > Tariff Settings shows Juan's custom fixed tariff "Tarifa Fija (Trimestral)" with one
  season per quarter (Season 1 Jan-Mar ... Season 4 Oct-Dec), each with a Buy and a Sell rate (equal: 1:1 net
  metering). The flow edits only the season of the quarter in force, walks the wizard through the other seasons
  unchanged, and answers "No" to "Switch the operating mode?" so the mode (Self-Consumption) never changes.
  The rate fields accept 5 decimals; the price is rounded half-up to 5 decimals.
- Emporia: not signed in on any reachable Android (Pixel or DroidFuse); nothing to apply until someone signs in.
  Its Manual Rate Entry takes cents/kWh (Menu > Home > Utility Plan, or Manage Devices > device > Location &
  Utility Info > Utility Rate).
- Tuya / Smart Life: signed in, but its devices (Mini Plug, Smart Bulb) have no energy metering, so there is no
  electricity-price setting to apply.
"""
from __future__ import annotations

import datetime as dt
import time
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

FRANKLIN = "com.Franklinwh.FamilyEnergy"
QUARTER_LABEL = {1: "Jan-Mar", 2: "Apr-Jun", 3: "Jul-Sep", 4: "Oct-Dec"}


def _franklin_open_tariff(d) -> None:
    d.force_stop(FRANKLIN)
    d.launch(FRANKLIN)
    time.sleep(3)
    # A location-permission prompt can appear on launch; dismiss it without granting anything.
    if d.find(regex=r"^Don.t allow$"):
        d.key("KEYCODE_BACK")
        time.sleep(2)
    d.tap(d.wait(desc="Settings, Tab 3 of 4", timeout=40))
    d.tap(d.wait(regex=r"^Tariff Settings", timeout=20))
    d.wait(regex=r"^Summary$", timeout=20)


def _franklin_open_season(d, label: str) -> None:
    for _ in range(4):
        nodes = d.dump()
        row = next((n for n in nodes if n.label.startswith("Season") and n.label.endswith(label)), None)
        if row:
            edit = min((n for n in nodes if n.label == "Edit" and n.bounds[1] >= row.bounds[3]),
                       key=lambda n: n.bounds[1], default=None)
            if edit:
                d.tap(edit)
                d.wait(regex=rf"^Season \d: {label}$", timeout=20)
                return
        d.swipe_up()
    raise RuntimeError(f"Franklin tariff has no season row for {label}")


def apply_franklin(d, price: float, evidence: Path, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    label = QUARTER_LABEL[(today.month - 1) // 3 + 1]
    value = str(Decimal(str(price)).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP))
    _franklin_open_tariff(d)
    _franklin_open_season(d, label)
    fields = [n for n in d.dump() if n.cls.endswith("EditText")]
    if len(fields) != 2:
        raise RuntimeError(f"expected Buy and Sell fields, found {len(fields)}")
    for f in fields:
        d.clear_and_type(f, value)
    d.key("KEYCODE_BACK")  # hide the keyboard
    typed = [n.text for n in d.dump() if n.cls.endswith("EditText")]
    if typed != [value, value]:
        raise RuntimeError(f"typed {typed}, expected {value}")
    # Walk the wizard: Next/Save through every season (others untouched) until the mode question appears.
    for _ in range(12):
        nodes = d.dump()
        no = d.find(nodes, desc="No") or d.find(nodes, text="No")
        if no and any("operating mode" in n.label for n in nodes):
            d.tap(no)  # keep the current operating mode
            break
        btn = d.find(nodes, regex=r"^(Next|Save)$")
        if not btn:
            raise RuntimeError("Franklin wizard: no Next/Save and no mode question")
        d.tap(btn)
        time.sleep(1.5)
    else:
        raise RuntimeError("Franklin wizard did not finish")
    # Read back from the server: restart the app and reopen the season.
    _franklin_open_tariff(d)
    _franklin_open_season(d, label)
    shown = [n.text for n in d.dump() if n.cls.endswith("EditText")]
    evidence.mkdir(parents=True, exist_ok=True)
    d.screenshot(str(evidence / f"franklin-{today.isoformat()}.png"))
    d.key("KEYCODE_BACK")
    time.sleep(1)
    d.key("KEYCODE_BACK")
    d.force_stop(FRANKLIN)
    if shown != [value, value]:
        raise RuntimeError(f"Franklin read back {shown}, expected {value}")
    return f"{label} buy/sell {value}"


APPS = {
    "franklin": {"route": "mba", "serial": "66160DLKX004F1", "apply": apply_franklin},
}
