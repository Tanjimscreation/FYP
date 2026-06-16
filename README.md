# FYP

This repository supports a final year project using public health survey data. NHANES is the primary analysis dataset, with BRFSS planned as an external validation dataset and MIDUS III planned for cross-study comparison.

Raw datasets are not committed to Git because they are large and should be downloaded from their official sources.

## Research Data Plan

| Dataset | Role | Source | Local Path |
|---|---|---|---|
| NHANES | Primary analysis dataset | https://wwwn.cdc.gov/nchs/nhanes/ | `data/nhanes/` |
| BRFSS | Validation dataset | https://www.cdc.gov/brfss/annual_data/annual_data.htm | `data/brfss/` |
| MIDUS III | Cross-study comparison | https://www.icpsr.umich.edu/web/NACDA/studies/36346 | `data/midus/` |

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Download the NHANES baseline files:

```bash
python scripts/download_nhanes.py
```

Read [Dataset Download Instructions](docs/dataset-download-instructions.md) before downloading BRFSS or MIDUS files, because MIDUS requires ICPSR account access and BRFSS file naming may vary by release format.

## Repository Structure

| Path | Purpose |
|---|---|
| `data/` | Local-only raw datasets and data notes. Large source files are ignored by Git. |
| `docs/` | Dataset instructions, variable notes, and project documentation. |
| `models/` | Trained model outputs and small model metadata. Large model binaries are ignored. |
| `notebooks/` | Exploratory analysis notebooks. |
| `reports/` | Generated summaries, report drafts, and figures. |
| `scripts/` | Reproducible data download, cleaning, and analysis scripts. |
| `src/fyp/` | Reusable Python package code. |
| `tests/` | Automated tests for project code. |

## NHANES Analysis Notes

Use `SEQN` as the participant-level merge key across NHANES modules.

For population-level NHANES estimates, use the survey design variables and the correct weights for the variables being analyzed. Typical two-year public-use files include design variables such as `SDMVSTRA` and `SDMVPSU`, with interview or MEC weights depending on the analysis. The 2017-March 2020 pre-pandemic files require their own CDC analytic guidance and should not be treated as ordinary 2019-2020 files.

See [NHANES Data Dictionary](docs/nhanes-data-dictionary.md) for variable planning notes.

## Reproducibility

- Keep raw `.XPT`, `.xpt`, `.csv`, and `.sas7bdat` files out of Git.
- Keep generated or large model binaries out of Git unless they are intentionally small.
- Prefer scripts in `scripts/` for repeatable preprocessing over notebook-only transformations.
- Record important derived variables and exclusion rules in `docs/`.

## Project Status

- [x] Repository structure created
- [x] Raw data ignore rules added
- [x] Dataset download documentation added
- [x] NHANES baseline downloader added
- [ ] Raw datasets downloaded locally
- [ ] NHANES preprocessing pipeline implemented
- [ ] Exploratory analysis completed
- [ ] Modeling and validation completed
- [ ] Final report generated

## Data Use And Citation

This project uses publicly available datasets from CDC/NCHS NHANES, CDC BRFSS, and ICPSR/NACDA MIDUS III. Cite each dataset according to its official data-use and citation guidance in the final report.
