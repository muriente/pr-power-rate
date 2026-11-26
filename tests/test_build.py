"""Offline tests against archived official LUMA workbooks; values cross-checked by hand with NEPR orders."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from prrate import build, luma, nepr  # noqa: E402

WORKBOOK = ROOT / "data/luma/archive/63334ef24aee9d56.xlsx"  # Tabla-de-Factores-1.xlsx, uploaded 2026-10


class PeriodParsing(unittest.TestCase):
    def test_quarter(self):
        self.assertEqual(luma.parse_period("octubre a diciembre 2026"), (dt.date(2026, 10, 1), dt.date(2026, 12, 31)))

    def test_single_month_and_noise(self):
        self.assertEqual(luma.parse_period("​junio 2020*"), (dt.date(2020, 6, 1), dt.date(2020, 6, 30)))
        self.assertEqual(luma.parse_period("mayo y junio 2019"), (dt.date(2019, 5, 1), dt.date(2019, 6, 30)))


class Workbook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.periods = luma.parse_workbook(WORKBOOK)

    def test_rows(self):
        self.assertGreaterEqual(len(self.periods), 37)
        self.assertEqual(self.periods[0]["label"], "octubre a diciembre 2026")

    def test_oct_dec_2026_factors_match_nepr_2026_09_30(self):
        f = self.periods[0]["factors_usd_per_kwh"]
        self.assertEqual(self.periods[0]["order_date"], "2026-09-30")
        self.assertAlmostEqual(f["FCA"], 0.173576, places=6)   # not LUMA's proposed 0.180736
        self.assertAlmostEqual(f["PPCA"], 0.045090, places=6)
        self.assertAlmostEqual(f["FOS"], 0.020822, places=6)

    def test_overlapping_rows_latest_order_wins(self):
        self.assertEqual(luma.select_current(self.periods, dt.date(2025, 9, 15))["label"], "septiembre 2025")

    def test_annual_row(self):
        cur = luma.select_current(self.periods, dt.date(2026, 11, 26))
        self.assertEqual(nepr.annual_row_for(self.periods, cur)["order_date"], "2026-06-30")


class Price(unittest.TestCase):
    def run_build(self, today):
        args = type("A", (), {"xlsx": str(WORKBOOK), "workbook_url": "test", "offline": True, "today": today})()
        return build.build(args)["current"]

    def test_oct_dec_2026(self):
        cur = self.run_build("2026-11-26")
        self.assertEqual(cur["price_usd_per_kwh"], 0.328588)
        self.assertEqual(cur["fixed_charge_usd_per_month"], 8.0)
        # NEPR 2026-09-30 Table 2: 800 kWh GRS bill $270.86 ($0.33858/kWh; NEPR rounds the $42.27 delta down)
        self.assertAlmostEqual(8.0 + 800 * cur["price_usd_per_kwh"], 270.87, places=2)
        self.assertEqual(round(cur["average_usd_per_kwh_including_fixed_charge"]["800"] * 100, 2), 33.86)

    def test_jul_sep_2026_matches_nepr_table_to_the_cent(self):
        cur = self.run_build("2026-08-15")
        self.assertEqual(cur["price_usd_per_kwh"], 0.27574)
        self.assertEqual(round(8.0 + 800 * cur["price_usd_per_kwh"], 2), 228.59)  # NEPR 2026-09-30 Table 2

    def test_stale(self):
        with self.assertRaises(build.BuildError) as ctx:
            self.run_build("2027-01-05")
        self.assertEqual(ctx.exception.code, 2)

    def test_site_files(self):
        args = type("A", (), {"xlsx": str(WORKBOOK), "workbook_url": "test", "offline": True, "today": "2026-11-26"})()
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "site"
            build.write_site(build.build(args), out)
            self.assertEqual((out / "api/v1/price.txt").read_text().strip(), "0.328588")
            self.assertEqual(json.loads((out / "api/v1/current.json").read_text())["effective_end"], "2026-12-31")


class NeprMatching(unittest.TestCase):
    def test_check_values_six_decimals(self):
        text = "Cláusula de Ajuste PCA = $0.173576kWh ... $0.045090/kWh ... FOS = $0.020822/kWh"
        got = nepr.check_values(text, {"FCA": 0.1735760001, "PPCA": 0.04509, "FOS": 0.020822}, nepr.QUARTERLY)
        self.assertEqual(got, {"FCA": True, "PPCA": True, "FOS": True})

    def test_docket_urls(self):
        h = ('<a href="https://energia.pr.gov/wp-content/uploads/sites/7/2026/09/20260930-MI20200001-Resolucion-y-Orden.pdf">'
             '<a href="https://energia.pr.gov/wp-content/uploads/sites/7/2026/10/20261007-MI20200001-Resolucion-y-Orden-carta-3PPO.pdf">')
        self.assertEqual(list(nepr.docket_order_urls(h)), ["20260930"])


if __name__ == "__main__":
    unittest.main()
