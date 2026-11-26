# Official sources: LUMA residential (GRS) rate, Oct–Dec 2026

Researched 2026-11-26. Every value below is tied to a primary document (text extracted with pdfplumber).

## Bottom line

| Item | Value | Source |
|---|---|---|
| GRS customer charge (FY2027, from 2026-07-01) | **$8.00 / month** | Tariff book p.5 (sheet 4); Final Rate Order App. B p.773 |
| GRS energy charge (FY2027) | **$0.08648 / kWh, flat** (first 425 kWh and excess have the same price) | same |
| Oct–Dec 2026 FCA | **$0.173576 / kWh** | NEPR R&O 2026-09-30, pp.8, 10, 27 |
| Oct–Dec 2026 PPCA | **$0.045090 / kWh** | same, pp.9, 10, 28 |
| Oct–Dec 2026 FOS | $0.020822 / kWh (a **credit** for qualifying subsidized customers only, not a charge) | same, pp.9–10, 27 |
| Annual riders Jul 2026–Jun 2027 | CILTA 0.007386; SUBA-HH 0.014338; SUBA-NHH 0.000865; EE 0.000853 | NEPR R&O 2026-06-30, pp.6–9, 14; repeated in 2026-09-30 Anejo 4 p.29 |
| Pension rider / Provisional rider | 0 from 2026-07-01 (folded into base rates) | NEPR R&O 2026-07-22 (NEPR-MI-2026-0005) |
| **All-in variable rate, standard GRS, Oct–Dec 2026** | **$0.328588 / kWh** (32.8588 ¢) | computed below |
| **Effective average at 800 kWh incl. $8 fixed charge** | **$0.338588 / kWh = 33.86 ¢** ($270.87; NEPR prints $270.86 and $0.33858) | NEPR R&O 2026-09-30 Table 2 p.11 and Anejo 4 p.29 |

The press figure of 33.86 ¢/kWh is NEPR's own number: the effective average for a non-subsidized GRS customer using 800 kWh/month, with the $8.00 customer charge included. The 18.0736 ¢ FCA was **LUMA's proposal**. NEPR cut it to 17.3576 ¢ in the same resolution.

---

## 1. Base tariff (FY2027, in effect from 2026-07-01)

### 1a. LUMA tariff book FY2027 (Spanish)
- Official PDF: https://lumapr.com/wp-content/uploads/2026/07/FY2027-Tariff-Book-Modifications_Spanish.pdf (85 pages, SHA-256 `cccf3fb5…d678172`).
- The flipbook https://lumapr.aflip.in/FY2027-Tariff-Book-Spanish is a Heyzine viewer. Its embedded PDF, https://cdnm.heyzine.com/files/uploaded/a5457abee101a4c56b0422db6fab9fa0a09b8a25.pdf (also served at `/flip-book/pdf/<hash>.pdf`), is **byte-identical** to the lumapr.com PDF (same SHA-256).
- The header reads "Revision: 2, Amendment: 1". The "Fecha de entrada en vigor" fields are blank on every sheet. The effective date comes from the orders in 1b and 1c.

| Rate | Customer charge | Energy charge | PDF page (sheet) |
|---|---|---|---|
| **GRS** (General Residential) | $8.00/mo; minimum bill $8.00 | $0.08648/kWh first 425 kWh; $0.08648/kWh additional | p.5–6 (sheets 4–5) |
| LRS (Lifeline, nutrition-assistance eligible) | $5.00/mo; minimum $5.00 | $0.03002 first 425 kWh; $0.08648 additional | p.7 (sheet 6) |
| RH3 (public-housing projects) | $4.00/mo | $0.03170 first 425 kWh; $0.08648 additional | p.9 (sheet 8) |
| RFR (fixed rate, PHA public housing) | $30 / $40 / $50 per month (1 / 2–3 / 4–5 rooms) | $0.08648/kWh above 600 / 800 / 1,000 kWh | p.11 (sheet 10) |

For GRS the 425 kWh block still exists in the tariff text, but both blocks are priced at $0.08648. **There is no effective consumption tier for standard GRS in FY2027.**

Riders listed as applicable to GRS (p.6): FCA, PPCA, FOS, CILTA, SUBA-HH, SUBA-NHH, EE, NM, SC (securitization), LP, DD, TUP. Application notes from the rider sheets:
- **FCA, PPCA, CILTA, SUBA-HH, SUBA-NHH, EE**: "A todas las tarifas excepto el bloque fijo de la tarifa RFR" (pp.54, 56, 60, 62, 64, 70). All of them apply per kWh to every standard GRS customer. SUBA-HH and CILTA are therefore charged to residential customers.
- **FOS** (p.58–59): applies only to *subsidized* GRS customers (disabled, elderly, university students), LRS and RH3 with monthly use of 500 kWh or less. It is a **credit**: FOS × kWh up to 400 kWh, FOS × 400 for 401–425 kWh, and FOS × (500 − kWh) × 400/75 for 426–500 kWh. Its cost is recovered through SUBA-HH ("Subsidio de Combustible Residencial", p.62). **Do not add FOS to the standard residential rate.**
- **SC – Cargo Titulización** (p.72): "PLACEHOLDER PARA CARGO TITULIZACIÓN". Not in effect, no factor.
- **TUP** (p.83): 0 in the LUMA table.
- **DD** (p.82): 10% discount on the base-rate portion for residential customers on direct debit. This is optional and not in the default rate.
- **NM** (p.66–67): net-metering exports are credited at base energy + FCA + PPCA + SUBA-HH + SUBA-NHH + CILT + EE.
- The FY2027 book has no Pension or Provisional rider.

### 1b. Permanent rate case final order
- **NEPR-AP-2023-0003, "Final Resolution and Order on Electricity Rates", 2026-04-15.** PDF: https://energia.pr.gov/wp-content/uploads/sites/7/2026/04/20260415-AP20230003-Final-Resolution-and-Order.pdf (881 pages, 56 MB).
  - Appendix B "Energy Bureau's adopted rates", PDF p.773:

    | GRS | FY2026 | **FY2027** | FY2028 |
    |---|---|---|---|
    | Customer charge /mo | $4.00 | **$8.00** | $16.00 |
    | Energy first 425 kWh | $0.08249 | **$0.08648** | $0.06275 |
    | Energy >425 kWh | $0.08869 | **$0.08648** | $0.06275 |

    LRS FY2027: $5.00, $0.03002 / $0.08648. RH3 FY2027: $4.00, $0.03170 / $0.08648. RFR FY2027 excess energy: $0.08648.
  - Implementation schedule, Ch. 7, PDF p.727: "July 1, 2026: Implement FY27 Rates based on FY27 target revenue … July 1, 2027: Implement FY28 Rates …", subject to revenue decoupling with a 3% cap on surcharges. **FY2028 base rates ($16.00, $0.06275) are due on 2027-07-01.**
  - Ch. 2, PDF p.56: the FY26 reconciliation amount ($98,747,153) is recovered over FY27 starting 2026-07-01, and the FY27 target revenue is $1,881,309,272.
- **NEPR-MI-2026-0005, Resolution and Order of 2026-07-22**, approving the revised tariff book. PDF: https://energia.pr.gov/wp-content/uploads/sites/7/2026/07/20260722-MI20260005-Resolution-and-Order.pdf (2 pages). It says the provisional rate "was reconciled with the approved rates and incorporated into the FY-2027 revenue requirement, while the pension rider is now integrated into the base rate, thereby eliminating the need for the pension rider". This is why Pension (0.019191) and Provisional (0.014931) fall to 0 from July 2026. The same order moves the LRS/RH3 discount from SUBA-HH into base rates.
- LUMA's 2026-09-15 motion (p.2) also cites both orders and names the FY2027 book as "the approved and currently effective PREPA Tariff Book for Fiscal Year 2027".
- NEPR's own bill calculations confirm $8.00 + $0.08648 flat. The Jul–Sep 2026 bill of $228.59 at 800 kWh (R&O 2026-06-30, p.15 and Anejo 4 p.21) works out exactly with those base values (see section 4).

---

## 2. NEPR quarterly factors, Oct–Dec 2026

**Case NEPR-MI-2020-0001** ("In re: Tarifa Permanente de la AEE"). This case holds both the quarterly reconciliations/factors and the annual riders. Verified on every document below.

### 2a. Resolución y Orden, 2026-09-30
- PDF: https://energia.pr.gov/wp-content/uploads/sites/7/2026/09/20260930-MI20200001-Resolucion-y-Orden.pdf (29 pages, SHA-256 `ab26070f…c6c14649a`).
- p.1 (Introduction): "La propuesta presentada por LUMA … contempla un aumento en la [FCA] de 11.4070 a 18.0736 centavos por kWh … el Negociado de Energía ha determinado diferir la cantidad de $17,649,888.46 asociados a las deficiencias en el suministro de gas natural, y la exclusión, por el momento, de las cantidades propuestas por concepto de bad debt … el 'FCA' propuesto se reduce de 18.0736 a 17.3576 centavos por kWh."
- p.8 FCA: ($196,982,605.76 + $189,272,913.71 + $184,887,981.25 − $17,649,888.46) = $553,493,612.26 projected fuel, plus a $131,650,334.94 Jun–Aug reconciliation, gives $685,143,947.20. Dividing by 3,947,236,226 kWh gives **$0.173576/kWh**.
- p.9 PPCA: $180,464,322.68 projected (including CBES $10,780,675 and ASAP $370,000) − $2,484,637.34 reconciliation = $177,979,685.34. Divided by 3,947,236,226 kWh this gives **$0.045090/kWh**.
- p.9–10 FOS: $30 × 2,739,581 bbl (non-gas) / 3,947,236,226 kWh = **$0.020822/kWh**.
- p.10 summary table: FCA 0.173576, PPCA 0.045090 and FOS 0.020822, effective 2026-10-01 to 2026-12-31 "o hasta tanto el Negociado de Energía los modifique".
- p.11 Table 1: FCA +0.059506, PPCA −0.006658, net **+0.052848 $/kWh**. Table 2 (non-subsidized GRS, 800 kWh): **$228.59 ($0.28574) → $270.86 ($0.33858), +$42.27 (+18.5%)**.
- Anejo 2 p.27 (FCA and FOS line items), Anejo 3 p.28 (PPCA), Anejo 4 p.29. Anejo 4 restates the annual riders (CILT 0.007386, SUBA-HH 0.014338, SUBA-NHH 0.000865, EE 0.000853, Pension 0, Provisional 0) and bills for GRS, GSS, GSP and GST.
- It orders LUMA to file Jan–Mar 2027 factors **by 12:00 p.m. on 2026-12-14** (p.11).

### 2b. LUMA table vs NEPR resolution

| Factor | NEPR 2026-09-30 | LUMA XLSX row 5 | Match |
|---|---|---|---|
| FCA | 0.173576 | 0.173576 | yes |
| PPCA | 0.045090 | 0.04509 | yes |
| FOS | 0.020822 | 0.020822 | yes |
| CILTA | 0.007386 | 0.007386280454… | yes (the XLSX is unrounded) |
| SUBA-HH / NHH | 0.014338 / 0.000865 | same | yes |
| EE | 0.000853 | 0.000853363929… | yes (unrounded) |
| Pension / Provisional | 0 / 0 | 0 / 0 | yes |

**Caveat on the LUMA XLSX "Parámetros" block (row 47, Oct–Dec 2026):** the inputs do not reproduce the published factor. C47 ($627,151,977.11) is the **Jun–Aug actual** fuel cost used in the reconciliation (R&O p.6), not the Oct–Dec projection ($553,493,612.26). Likewise, E47 ($208,198,256.38) is not the approved PPCA projection ($180,464,322.68). Using row 47 gives FCA 0.1922 instead of 0.1736. The Jul–Sep row (48) does reproduce its factors exactly. **An automated pipeline should take factor values from rows 5+ or from the NEPR PDF and must not recompute them from the parameter block.**

### 2c. Origin of 18.0736
LUMA's 2026-09-15 motion asked for **FCA $0.180736, PPCA $0.045771, FOS $0.021136** (PDF p.15). PDF: https://energia.pr.gov/wp-content/uploads/sites/7/2026/09/20260915-MI20200001-Motion-Submitting-FCA-and-PPCA-Reconciliations-for-June-August-2026-and-Calculated-FCA-PPCA-and-FOS-Factors-for-October-December-2026-and-Memorandum-of-Law.pdf. Section XI (p.16–17) asks NEPR to apply the Final Rate Order's 1.51% bad-debt factor to the quarterly riders.

The approved values reproduce LUMA's requests exactly once the two items NEPR removed are added back:
- FCA: (0.173576 + 17,649,888.46/3,947,236,226) × 1.0151 = (0.173576 + 0.004471) × 1.0151 = **0.180736**
- PPCA: 0.045090 × 1.0151 = **0.045771**
- FOS: 0.020822 × 1.0151 = **0.021136**

So 18.0736 is neither a typo nor a different definition. It is LUMA's requested FCA: NFE natural-gas shortfall costs plus a 1.51% bad-debt gross-up. NEPR deferred the first and excluded the second, which leaves 17.3576. Press items that print "11.4070 → 18.0736" are quoting the request (as the resolution's own p.1 does). Metro PR reports both numbers correctly.

### 2d. Later resolutions (October–November 2026): none changed the factors
I found these by probing `…/uploads/sites/7/2026/{10,11}/YYYYMMDD-MI20200001-{Resolucion-y-Orden|Resolucion-y-Orden-1|Resolution-and-Order}.pdf`. A non-existent date returns 404, so these hits are real:

| Date | URL | Subject | Effect on factors |
|---|---|---|---|
| 2026-10-04 | https://energia.pr.gov/wp-content/uploads/sites/7/2026/10/20261004-MI20200001-Resolucion-y-Orden.pdf | PREPA motion of Oct 2 (NFE letter) | p.4: "no procede … modificar la Resolución de 30 de septiembre … permanece en pleno vigor" |
| 2026-10-07 | …/2026/10/20261007-MI20200001-Resolucion-y-Orden.pdf | NFE audit information request | none |
| 2026-10-10 | …/2026/10/20261010-MI20200001-Resolution-and-Order.pdf | NFE reading of the Sep 30 / Oct 4 orders | "REAFFIRMS" Sep 30 |
| 2026-10-15 | …/2026/10/20261015-MI20200001-Resolucion-y-Orden.pdf | NFE technical conference request | none |
| 2026-10-30 | …/2026/10/20261030-MI20200001-Resolucion-y-Orden.pdf | Natural gas availability, November | none |
| 2026-11-06 | …/2026/11/20261106-MI20200001-Resolucion-y-Orden.pdf | SME (PYMES) consumption/billing information request | none |
| 2026-11-10 | …/2026/11/20261110-MI20200001-Resolucion-y-Orden.pdf | Intervention request (Innovation Force Solar) | none (restates the Sep 30 factors) |
| 2026-11-24 | …/2026/11/20261124-MI20200001-Resolucion-y-Orden.pdf | SME information compliance and confidentiality | none |

Also checked: LUMA's 2026-10-13 compliance motion (https://energia.pr.gov/wp-content/uploads/sites/7/2026/10/20261013-MI20200001-Mocion-en-Cumplimiento-con-las-Resoluciones-y-Ordenes-de-7-de-Octubre-de-2026-y-9-de-Octubre-de-2026.pdf), which covers NFE invoices only. The probe only covers those three filename patterns; see Limitations.

### 2e. Annual riders, Jul 2026–Jun 2027 (R&O 2026-06-30)
- PDF: https://energia.pr.gov/wp-content/uploads/sites/7/2026/06/20260630-MI20200001-Resolucion-y-Orden.pdf. This order also set Jul–Sep 2026 FCA 0.114070, PPCA 0.051748 and FOS 0.016650.
- CILTA 0.007386 (p.6), SUBA-HH 0.014338 (p.8), SUBA-NHH 0.000865 (p.9), EE 0.000853 (p.9, unchanged). Summary and Table 1 on p.14.
- Table 2 / Anejo 4 (pp.15, 21), GRS at 800 kWh: Apr–Jun 2026 **$217.84 ($0.27230)** → Jul–Sep 2026 **$228.59 ($0.28574)**, +4.9%.

---

## 3. Press coverage, Oct–Dec 2026

| Outlet | URL | Numbers | Definition |
|---|---|---|---|
| El Nuevo Día (M. Guillama Capella, **2026-09-30 6:26 pm**) | https://www.elnuevodia.com/noticias/locales/notas/nueva-tarifa-record-alza-de-18-lleva-el-costo-del-kilovatio-hora-a-336-centavos/ | 33.86 ¢/kWh "tarifa récord"; +18% (headline); +$42.27/month | "cliente residencial promedio no subsidiado". The article does not state 800 kWh or the fixed charge. The fetched text does **not** contain 18.0736, 17.3576 or 11.4070. |
| Metro PR (2026-09-30) | https://www.metro.pr/noticias/2026/09/30/negociado-de-energia-aprueba-aumento-de-42-en-la-factura-de-luz-de-un-cliente-residencial/ | Net +5.28 ¢/kWh; FCA requested 11.4070 → 18.0736, set at 17.3576; PPCA 5.1748 → 4.5090; 800 kWh bill $228.59 → $270.86 (+$42.27, 18.5%) | 800 kWh, non-subsidized (NEPR Table 2) |
| NotiUno (2026-09-30) | https://www.notiuno.com/noticias/gobierno-y-politica/5-centavos-por-kilovatio-hora-golpetazo-al-presupuesto-boricua-tras-alza-de-18-5-en/article_06b6c7d7-7b3f-483d-9a6c-d076216c700a.html | +$0.05284/kWh; +$42.27 on an 800 kWh bill; 18.5% | 800 kWh (search snippet only) |
| abc.pr | https://abc.pr/articulo/negociado-de-energia-aprueba-aumento-de-42-en-factura-de-luz | 800 kWh → $270.86 | snippet only |
| El Vocero (LUMA proposal, Sep) | https://www.elvocero.com/economia/luma-propone-alza-que-sumar-a-48-mensuales-a-la-factura-de-luz/article_f03076e0-86cb-4e73-b526-5f9c829b586a.html | about $48/month (the proposal, not the approval) | not read in full |
| NotiCel (2026-09-16, proposal) | https://noticel.com/en/ultima-hora/20260916/factura-de-luz-podria-aumentar-unos-48-mensuales-desde-octubre-segun-presidenta-de-luma/ | about $48/month (the proposal) | not read in full |

All outlets use NEPR's Table 2 definition: **effective average = (customer charge + all per-kWh charges × 800) / 800 for a non-subsidized GRS customer.** The "≈$48/month" proposal figure fits LUMA's 18.0736 / 4.5771 request.

---

## 4. All-in reconstruction (standard non-subsidized GRS)

Components that apply: base energy + FCA + PPCA + CILTA + SUBA-HH + SUBA-NHH + EE, plus the $8.00 customer charge.
Components that do not apply: FOS (a credit for qualifying customers only), Pension and Provisional (0 from July 2026), SC (placeholder), TUP (0), DD (optional discount).

| $/kWh | Jul–Sep 2026 | Oct–Dec 2026 |
|---|---|---|
| Base energy (GRS FY27) | 0.086480 | 0.086480 |
| FCA | 0.114070 | 0.173576 |
| PPCA | 0.051748 | 0.045090 |
| CILTA | 0.007386 | 0.007386 |
| SUBA-HH | 0.014338 | 0.014338 |
| SUBA-NHH | 0.000865 | 0.000865 |
| EE | 0.000853 | 0.000853 |
| **Variable total** | **0.275740** | **0.328588** |

Bill = $8.00 + variable × kWh, at NEPR's 6-decimal factors. With the XLSX's unrounded CILTA/EE values the variable total rises by about 0.000001 $/kWh, which is not material.

| kWh/month | Jul–Sep bill | Jul–Sep effective | Oct–Dec bill | Oct–Dec effective |
|---|---|---|---|---|
| 400 | $118.30 | 29.574 ¢ | $139.44 | 34.859 ¢ |
| 425 | $125.19 | 29.456 ¢ | $147.65 | 34.741 ¢ |
| **800** | **$228.59** | **28.574 ¢** | **$270.87** | **33.859 ¢** |
| 1000 | $283.74 | 28.374 ¢ | $336.59 | 33.659 ¢ |

Reconciliation to the anchors:
- Jul–Sep: 8 + 800 × 0.275740 = **$228.592**, matching NEPR's $228.59 / $0.28574 exactly.
- Oct–Dec: 8 + 800 × 0.328588 = **$270.8704**, which gives **33.8588 ¢/kWh**. That rounds to the press 33.86 ¢ and matches NEPR's $0.33858 (truncated). NEPR prints $270.86 because it computes $228.59 + 800 × 0.05284 (the rounded difference) = $228.59 + $42.27. The 1-cent gap is NEPR's rounding, not a missing component.
- Of the 33.86 ¢, 1.0 ¢ is the $8 customer charge spread over 800 kWh. The marginal (per-kWh) price is **32.8588 ¢**.
- Wrong treatments: adding FOS gives 35.94 ¢ at 800 kWh. Using LUMA's 18.0736 FCA gives 34.57 ¢. Neither matches the published number.
- Older quarter, for history: Apr–Jun 2026 riders summed to 0.214965 $/kWh, including Pension 0.019191 and Provisional 0.014931. NEPR's $217.84 at 800 kWh implies $45.87 of pre-rate-case base charges. I did not pull the pre-July tariff book to split that into customer and energy charges.

---

## 5. Publication mechanics, for automated detection

- **Cadence (tariff book, FCA/PPCA sheets p.55, 57):** LUMA files proposed FCA/PPCA/FOS by the end of the 2nd week of the 3rd month of each quarter. Factors take effect with the first billing cycle of the next quarter. If no new factor is approved, the old one stays in force. Annual riders (CILTA, SUBA-HH/NHH, EE) are filed by the end of the 11th month and take effect July 1. There is also an "Ajuste Acelerado": a mid-quarter re-estimate if fuel plus purchased-power cost deviates by more than $20M. A mid-quarter change is therefore possible (it happened in 2025: Jul, then Aug–Sep, then Sep).
- **Next event:** LUMA must file Jan–Mar 2027 factors by **2026-12-14 12:00** (R&O 2026-09-30 p.11). NEPR historically rules around Dec 19–30.
- **NEPR documents:** `https://energia.pr.gov/wp-content/uploads/sites/7/YYYY/MM/YYYYMMDD-MI20200001-Resolucion-y-Orden.pdf`. Variants: `-Resolution-and-Order.pdf` and `-Resolucion-y-Orden-1.pdf`. LUMA filings use `YYYYMMDD-MI20200001-Motion-Submitting-…`. NEPR also posts HTML "orden" pages at `https://energia.pr.gov/orden/<slug>/`. Factor resolutions so far: 2025-09-30, 2025-12-19, 2026-03-27, 2026-06-30, 2026-09-30. The WordPress media REST search (`/wp-json/wp/v2/media?search=MI20200001`) is unreliable: it returned only 3 items. Probing the URL pattern by date returns a clean 404 for non-existent files, so it is reliable.
- **LUMA:** the rates page https://lumapr.com/tarifas-vigentes-del-servicio-electrico-en-puerto-rico/ links the factor table XLSX, currently https://lumapr.com/wp-content/uploads/2026/10/Tabla-de-Factores-1.xlsx. The `/YYYY/MM/` folder is the upload month, and the `-1` suffix is a WordPress de-duplication suffix, so the filename is not stable. Detect new versions by scraping the page for `Tabla-de-Factores*.xlsx`, then read row 5 (newest period first, column C = NEPR resolution date). The tariff book is linked from the same page (flipbook) and stored at `/wp-content/uploads/2026/07/FY2027-Tariff-Book-Modifications_Spanish.pdf`.

---

## Limitations / not verified
- The NEPR probe for later orders covered only three filename suffixes for 2026-10-01 to 2026-11-26. An order filed under an unusual name would be missed. No resolution found says the Sep 30 factors were modified, and the Oct 4 and Oct 10 orders expressly reaffirm them.
- The El Nuevo Día text was read through a fetch tool. I did not see the claim that ENDI (Oct 1) gave "FCA 11.4070 → 18.0736". The fetched article did not contain those numbers, and they may be in a different ENDI piece. Either way the number is the LUMA request, as shown above.
- I did not open the English tariff book. The Spanish book and Final Rate Order Appendix B agree on every residential value.
- Primera Hora, News is my Business and NotiCel coverage of the *approval* was not read in full. Only search snippets were seen.
- The pre-July 2026 GRS base (customer and energy split) was not taken from a primary document.

## Local files (SHA-256)
- `dl/research/20260930-MI20200001-Resolucion-y-Orden.pdf` ab26070f47f8e98fe3eb18a30a8f2941cb3fa10f9e6e85b43c95e34c6f14649a
- `dl/research/20260630-MI20200001-Resolucion-y-Orden.pdf` 81192bf45bb0ca56459075bc5f98a3e2e28e230386521317713aea19e35c609d
- `dl/research/20260415-AP20230003-Final-Resolution-and-Order.pdf` ee213cd120e28c99d9bec88e62e0d16b819dea41ee34bf6c2d8d8b0bc12e0da5
- `dl/research/20260722-MI20260005-Resolution-and-Order.pdf` f5fa3445da05e921d9dbba2885ac20ae5429e1e119121440ccee310c8807b66c
- `dl/research/20260915-MI20200001-Motion-Submitting-…pdf` 9014940fa3ce22ffb1d60e924bdd1a68c910d577f66a0e25ddbbabb5a5d2800c
- `dl/research/FY2027-Tariff-Book-Modifications_Spanish.pdf` cccf3fb5cc4a42e302320eca29480953316f11bc5dad21162f06c5a87d678172
- `dl/tabla.xlsx` 63334ef24aee9d566891b28706b445a8d74d7e86c305ca936a0061eef3558cb1
- Later MI-2020-0001 orders, Oct–Nov 2026: `dl/research/2026100*`, `202610[13]*`, `202611*`
