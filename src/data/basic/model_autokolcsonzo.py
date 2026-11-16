from dataclasses import dataclass
from datetime import date

from data.basic.model_dataclasses import Car


@dataclass
class Customer:
    customer_id: str
    name: str
    age: int
    email: str
    phone: str
    city: str


@dataclass
class Rental:
    rental_id: str
    customer_id: str
    car_plate: str
    start_date: str
    end_date: str
    daily_rate: int
    total_price: int


@dataclass
class Dataset:
    customers: list[Customer]
    cars: list[Car]
    rentals: list[Rental]

    def validate(self) -> None:
        customer_ids = [c.customer_id for c in self.customers]
        car_plates = [c.plate for c in self.cars]
        rental_ids = [r.rental_id for r in self.rentals]

        if len(customer_ids) != len(set(customer_ids)):
            raise ValueError("Ismétlődő ügyfélazonosító.")
        if len(car_plates) != len(set(car_plates)):
            raise ValueError("Ismétlődő rendszám.")
        if len(rental_ids) != len(set(rental_ids)):
            raise ValueError("Ismétlődő bérlésazonosító.")

        customers = set(customer_ids)
        cars = set(car_plates)
        for rental in self.rentals:
            if rental.customer_id not in customers:
                raise ValueError(f"Nem létező ügyfél a bérlésben: {rental.rental_id}")
            if rental.car_plate not in cars:
                raise ValueError(f"Nem létező autó a bérlésben: {rental.rental_id}")
            days = (date.fromisoformat(rental.end_date) - date.fromisoformat(rental.start_date)).days
            if days <= 0 or rental.daily_rate <= 0:
                raise ValueError(f"Hibás dátum vagy napidíj: {rental.rental_id}")
            if rental.total_price != days * rental.daily_rate:
                raise ValueError(f"Hibás végösszeg: {rental.rental_id}")
