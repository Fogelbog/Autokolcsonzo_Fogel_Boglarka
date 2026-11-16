from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from data.basic.handler.autokolcsonzo_common import SCHEMAS, build_dataset, to_rows
from data.basic.model_autokolcsonzo import Dataset


def write(dataset: Dataset, filename: Path) -> None:
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    workbook.remove(workbook.active)
    workbook.properties.creator = "Fógel Boglárka"
    for name, fields in SCHEMAS.items():
        sheet = workbook.create_sheet(name)
        sheet.append(fields)
        for row in to_rows(dataset, name):
            sheet.append([row[field] for field in fields])
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        for cell in sheet[1]:
            cell.fill = PatternFill("solid", fgColor="24466B")
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(horizontal="center")
        for column_index, field in enumerate(fields, start=1):
            sheet.column_dimensions[get_column_letter(column_index)].width = min(32, max(17, len(field) + 5))
    workbook.save(filename)


def read(filename: Path) -> Dataset:
    workbook = load_workbook(Path(filename), data_only=True)
    records = {}
    try:
        for name, fields in SCHEMAS.items():
            sheet = workbook[name]
            rows = sheet.iter_rows(values_only=True)
            header = next(rows, ())
            if tuple(header) != fields:
                raise ValueError(f"Hibás XLSX-fejléc: {name}")
            records[name] = [dict(zip(fields, row)) for row in rows if any(value is not None for value in row)]
    finally:
        workbook.close()
    return build_dataset(records)
