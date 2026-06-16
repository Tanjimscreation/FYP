"""Download NHANES public-use XPT files for the project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from urllib.request import Request, urlopen


BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"

BASELINE_FILES = [
    ("2015", "DEMO_I.XPT"),
    ("2015", "DPQ_I.XPT"),
    ("2015", "PAQ_I.XPT"),
    ("2015", "HOQ_I.XPT"),
    ("2017", "DEMO_J.XPT"),
    ("2017", "DPQ_J.XPT"),
    ("2017", "PAQ_J.XPT"),
    ("2017", "HOQ_J.XPT"),
]

PREPANDEMIC_FILES = [
    ("2017", "P_DEMO.XPT"),
    ("2017", "P_DPQ.XPT"),
    ("2017", "P_PAQ.XPT"),
]


def download(url: str, destination: Path, overwrite: bool = False) -> None:
    if destination.exists() and not overwrite:
        print(f"skip existing: {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "FYP NHANES downloader"})

    print(f"download: {url}")
    with urlopen(request) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    print(f"saved: {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download NHANES XPT files.")
    parser.add_argument(
        "--output-dir",
        default="data/nhanes",
        help="Folder where NHANES XPT files will be saved.",
    )
    parser.add_argument(
        "--include-prepandemic",
        action="store_true",
        help="Also download optional 2017-March 2020 pre-pandemic files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-download files that already exist.",
    )
    args = parser.parse_args()

    files = list(BASELINE_FILES)
    if args.include_prepandemic:
        files.extend(PREPANDEMIC_FILES)

    output_dir = Path(args.output_dir)
    for cycle_path, filename in files:
        url_filename = f"{Path(filename).stem}.xpt"
        url = f"{BASE_URL}/{cycle_path}/DataFiles/{url_filename}"
        download(url, output_dir / filename, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
