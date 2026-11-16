import json
from pathlib import Path

from data.basic.handler.autokolcsonzo_common import SCHEMAS, build_dataset, to_rows
from data.basic.model_autokolcsonzo import Dataset


def write(dataset: Dataset, folder: Path) -> None:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for name in SCHEMAS:
        with (folder / f"{name}.json").open("w", encoding="utf-8") as file:
            json.dump(to_rows(dataset, name), file, ensure_ascii=False, indent=2)


def read(folder: Path) -> Dataset:
    folder = Path(folder)
    records = {}
    for name in SCHEMAS:
        with (folder / f"{name}.json").open("r", encoding="utf-8") as file:
            value = json.load(file)
        if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
            raise ValueError(f"A JSON-nak dokumentumok listáját kell tartalmaznia: {name}")
        records[name] = value
    return build_dataset(records)
