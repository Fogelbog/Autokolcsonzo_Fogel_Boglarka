import csv
from pathlib import Path

from data.basic.handler.autokolcsonzo_common import SCHEMAS, build_dataset, to_rows
from data.basic.model_autokolcsonzo import Dataset


def write(dataset: Dataset, folder: Path) -> None:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for name, fields in SCHEMAS.items():
        with (folder / f"{name}.csv").open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
            writer.writeheader()
            writer.writerows(to_rows(dataset, name))


def read(folder: Path) -> Dataset:
    folder = Path(folder)
    records = {}
    for name, fields in SCHEMAS.items():
        with (folder / f"{name}.csv").open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            if reader.fieldnames != list(fields):
                raise ValueError(f"Hibás CSV-fejléc: {name}.csv")
            records[name] = list(reader)
    return build_dataset(records)
