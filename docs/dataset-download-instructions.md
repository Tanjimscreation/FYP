# Dataset Download Instructions

Raw data files are not included in this repository due to file size. Download each dataset from its official source and place the files in the local `data/` folders listed below.

## Local Data Layout

| Dataset | Local Folder | Git Status |
|---|---|---|
| NHANES | `data/nhanes/` | Ignored |
| BRFSS | `data/brfss/` | Ignored |
| MIDUS III | `data/midus/` | Ignored |

Keep raw `.XPT`, `.xpt`, `.csv`, and `.sas7bdat` files out of version control.

---

## 1. NHANES (Primary Dataset)

**Source:** https://wwwn.cdc.gov/nchs/nhanes/

### Recommended Baseline Files

Use the 2015-2016 and 2017-2018 cycles as the baseline NHANES dataset because the same four modules are available across both cycles.

| Cycle | File | Module | Purpose | Required | Local Path |
|---|---|---|---|---|---|
| 2015-2016 | `DEMO_I.XPT` | Demographics | Age, sex, race/ethnicity, survey weights, design variables | Yes | `data/nhanes/DEMO_I.XPT` |
| 2015-2016 | `DPQ_I.XPT` | Depression Screener | PHQ-9 depression symptoms | Yes | `data/nhanes/DPQ_I.XPT` |
| 2015-2016 | `PAQ_I.XPT` | Physical Activity | Activity and sedentary behavior variables | Yes | `data/nhanes/PAQ_I.XPT` |
| 2015-2016 | `HOQ_I.XPT` | Housing | Housing and household environment variables | Yes | `data/nhanes/HOQ_I.XPT` |
| 2017-2018 | `DEMO_J.XPT` | Demographics | Age, sex, race/ethnicity, survey weights, design variables | Yes | `data/nhanes/DEMO_J.XPT` |
| 2017-2018 | `DPQ_J.XPT` | Depression Screener | PHQ-9 depression symptoms | Yes | `data/nhanes/DPQ_J.XPT` |
| 2017-2018 | `PAQ_J.XPT` | Physical Activity | Activity and sedentary behavior variables | Yes | `data/nhanes/PAQ_J.XPT` |
| 2017-2018 | `HOQ_J.XPT` | Housing | Housing and household environment variables | Yes | `data/nhanes/HOQ_J.XPT` |

Download with:

```bash
python scripts/download_nhanes.py
```

Or download manually:

| File | Link |
|---|---|
| `DEMO_I.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT |
| `DPQ_I.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DPQ_I.XPT |
| `PAQ_I.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/PAQ_I.XPT |
| `HOQ_I.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/HOQ_I.XPT |
| `DEMO_J.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT |
| `DPQ_J.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DPQ_J.XPT |
| `PAQ_J.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/PAQ_J.XPT |
| `HOQ_J.XPT` | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/HOQ_J.XPT |

### Optional 2017-March 2020 Extension

CDC released 2017-March 2020 pre-pandemic files because NHANES 2019-2020 field operations were suspended during the COVID-19 pandemic. Do not analyze partial 2019-2020 data alone as a nationally representative cycle. If extending the project beyond the baseline files, use CDC's 2017-March 2020 pre-pandemic guidance and check module availability carefully.

Candidate optional files:

| File | Module | Link |
|---|---|---|
| `P_DEMO.XPT` | Demographics and sample weights | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2020/P_DEMO.XPT |
| `P_DPQ.XPT` | Mental Health - Depression Screener | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2020/P_DPQ.XPT |
| `P_PAQ.XPT` | Physical Activity | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2020/P_PAQ.XPT |

Download these optional files with:

```bash
python scripts/download_nhanes.py --include-prepandemic
```

Note: a directly matching `P_HOQ.XPT` housing file is not listed in the 2017-March 2020 questionnaire data page. Keep the 2015-2018 baseline if housing variables are central to the analysis.

### NHANES Merge And Analysis Rules

- Merge modules within each cycle using `SEQN`.
- Stack cycles only after harmonizing variable names, coding, and eligibility rules.
- Use `SDMVSTRA`, `SDMVPSU`, and the correct interview or MEC weights for survey-weighted population estimates.
- Treat special missing values such as refused, do not know, and not ascertained as missing before deriving scores.
- Document every derived variable in `docs/nhanes-data-dictionary.md`.

---

## 2. BRFSS (Validation Dataset)

**Source:** https://www.cdc.gov/brfss/annual_data/annual_data.htm

Download 2020 and 2021 LLCP data files in `.XPT` format, then place them in:

```text
data/brfss/
```

Suggested local names:

```text
data/brfss/LLCP2020.XPT
data/brfss/LLCP2021.XPT
```

Record any downloaded codebooks or variable layout files in `docs/` rather than committing raw data.

---

## 3. MIDUS III (Cross-study Comparison)

**Source:** https://www.icpsr.umich.edu/web/NACDA/studies/36346

MIDUS III requires free ICPSR account registration and acceptance of the study terms. Place downloaded files in:

```text
data/midus/
```

Record the exact ICPSR package version, download date, and citation information in the final report.
