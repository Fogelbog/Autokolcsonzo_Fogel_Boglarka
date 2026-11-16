from dataclasses import asdict

from data.basic.model_autokolcsonzo import Customer, Dataset, Rental
from data.basic.model_dataclasses import Car

SCHEMAS = {
    "customers": ("customer_id", "name", "age", "email", "phone", "city"),
    "cars": ("plate", "type", "year", "automatic"),
    "rentals": ("rental_id", "customer_id", "car_plate", "start_date",
                "end_date", "daily_rate", "total_price"),
}


def to_rows(dataset: Dataset, name: str) -> list[dict]:
    return [asdict(entity) for entity in getattr(dataset, name)]


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value in (1, "1", "True", "true", "TRUE"):
        return True
    if value in (0, "0", "False", "false", "FALSE"):
        return False
    raise ValueError(f"Érvénytelen logikai érték: {value!r}")


def from_rows(name: str, rows: list[dict]) -> list:
    objects = []
    for row in rows:
        if name == "customers":
            objects.append(Customer(
                str(row["customer_id"]), str(row["name"]), int(row["age"]),
                str(row["email"]), str(row["phone"]), str(row["city"]),
            ))
        elif name == "cars":
            objects.append(Car(
                str(row["plate"]), str(row["type"]), int(row["year"]),
                parse_bool(row["automatic"]),
            ))
        elif name == "rentals":
            objects.append(Rental(
                str(row["rental_id"]), str(row["customer_id"]),
                str(row["car_plate"]), str(row["start_date"]),
                str(row["end_date"]), int(row["daily_rate"]),
                int(row["total_price"]),
            ))
        else:
            raise ValueError(f"Ismeretlen adattípus: {name}")
    return objects


def build_dataset(loaded: dict[str, list[dict]]) -> Dataset:
    dataset = Dataset(
        customers=from_rows("customers", loaded["customers"]),
        cars=from_rows("cars", loaded["cars"]),
        rentals=from_rows("rentals", loaded["rentals"]),
    )
    dataset.validate()
    return dataset


def same_data(first: Dataset, second: Dataset) -> bool:
    return all(to_rows(first, name) == to_rows(second, name) for name in SCHEMAS)
