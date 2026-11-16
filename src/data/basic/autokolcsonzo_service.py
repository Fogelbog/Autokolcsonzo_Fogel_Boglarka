from pathlib import Path

from data.basic.handler import autokolcsonzo_csv, autokolcsonzo_json, autokolcsonzo_xlsx
from data.basic.model_autokolcsonzo import Dataset


def save(dataset: Dataset, format_name: str, output_folder: Path) -> Path:
    dataset.validate()
    folder = Path(output_folder)
    if format_name == "csv":
        destination = folder / "csv"
        autokolcsonzo_csv.write(dataset, destination)
    elif format_name == "json":
        destination = folder / "json"
        autokolcsonzo_json.write(dataset, destination)
    elif format_name == "xlsx":
        destination = folder / "autokolcsonzo.xlsx"
        autokolcsonzo_xlsx.write(dataset, destination)
    else:
        raise ValueError("Csak csv, json és xlsx formátum választható.")
    return destination


def load(format_name: str, output_folder: Path) -> Dataset:
    folder = Path(output_folder)
    if format_name == "csv":
        return autokolcsonzo_csv.read(folder / "csv")
    if format_name == "json":
        return autokolcsonzo_json.read(folder / "json")
    if format_name == "xlsx":
        return autokolcsonzo_xlsx.read(folder / "autokolcsonzo.xlsx")
    raise ValueError("Csak csv, json és xlsx formátum választható.")
