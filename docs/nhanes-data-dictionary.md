# NHANES Data Dictionary Notes

This file tracks the NHANES modules, key variables, and derived features planned for the project. Confirm exact variable coding in the CDC codebooks before final analysis.

## Core Merge Fields

| Variable | Meaning | Notes |
|---|---|---|
| `SEQN` | Participant identifier | Use as the merge key across NHANES modules. |
| `SDMVSTRA` | Masked variance pseudo-stratum | Required for survey-weighted variance estimation. |
| `SDMVPSU` | Masked variance pseudo-PSU | Required for survey-weighted variance estimation. |
| `WTINT2YR` | Interview weight | Use for interview/questionnaire-only analyses in regular two-year cycles. |
| `WTMEC2YR` | MEC examination weight | Use when analyses include MEC examination variables. |

For 2017-March 2020 pre-pandemic files, use the weights and guidance provided in the corresponding CDC documentation rather than assuming ordinary two-year cycle weights.

## Baseline Modules

| Module | Files | Role In Project |
|---|---|---|
| Demographics | `DEMO_I.XPT`, `DEMO_J.XPT` | Age, sex, race/ethnicity, socioeconomic variables, weights, and survey design variables. |
| Depression Screener | `DPQ_I.XPT`, `DPQ_J.XPT` | PHQ-9 symptom items and derived depression severity measures. |
| Physical Activity | `PAQ_I.XPT`, `PAQ_J.XPT` | Activity, sedentary behavior, and exercise-related predictors. |
| Housing | `HOQ_I.XPT`, `HOQ_J.XPT` | Household and housing environment predictors. |

## Candidate Derived Variables

| Derived Variable | Source Module | Construction Notes |
|---|---|---|
| `phq9_total` | DPQ | Sum PHQ-9 symptom items after converting refused, do not know, and not ascertained responses to missing. |
| `depression_binary` | DPQ | Common screening threshold is PHQ-9 total score >= 10; confirm final threshold in the methodology. |
| `age_group` | DEMO | Group `RIDAGEYR` into analysis-ready age bands. |
| `sex` | DEMO | Recode sex/gender variable into readable labels. |
| `race_ethnicity` | DEMO | Recode race/ethnicity categories using the cycle-specific codebook. |
| `income_poverty_ratio` | DEMO | Use family income-to-poverty ratio where available. |
| `physical_activity_level` | PAQ | Derive from activity frequency, duration, and intensity variables after harmonization. |
| `sedentary_time` | PAQ | Use self-reported sedentary behavior where available. |
| `housing_context` | HOQ | Derive from selected housing and household environment variables after codebook review. |

## Cleaning Rules To Confirm

- Apply age eligibility rules before deriving adult-only measures.
- Convert special missing codes to missing values before scoring or modeling.
- Keep cycle labels so pooled analyses can audit source years.
- Harmonize variable coding before stacking cycles.
- Use survey-weighted methods for descriptive statistics intended to represent the U.S. civilian non-institutionalized population.

## Open Decisions

- Final outcome definition: continuous PHQ-9 score, binary depression screen, or multi-class severity.
- Minimum age range for primary analysis.
- Whether housing variables are required in the final model.
- Whether to keep analysis limited to 2015-2018 or add 2017-March 2020 pre-pandemic optional files.
