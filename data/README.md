# Data

This directory is for local datasets used by the project.

The following source-data folders are intentionally ignored by Git:

- `nhanes/` - NHANES `.XPT` files
- `brfss/` - BRFSS LLCP validation files
- `midus/` - MIDUS III comparison files

Keep raw `.XPT`, `.xpt`, `.csv`, and `.sas7bdat` files out of version control. Add lightweight documentation in `docs/` if collection, preprocessing, or exclusion rules need to be described.

Detailed source links and placement instructions are in [`docs/dataset-download-instructions.md`](../docs/dataset-download-instructions.md).
