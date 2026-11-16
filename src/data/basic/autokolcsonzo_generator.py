import random
from datetime import date, timedelta

from faker import Faker

from data.basic.generator import generate_cars as sample_generate_cars
from data.basic.model_autokolcsonzo import Customer, Dataset, Rental
from data.basic.model_dataclasses import Car


def generate_customers(n: int, locale: str = "hu_HU", min_age: int = 18,
                       max_age: int = 80) -> list[Customer]:
    if n < 1 or not (18 <= min_age <= max_age):
        raise ValueError("Legalább egy ügyfél és érvényes életkor szükséges.")
    fake = Faker(locale)
    customers = []
    for index in range(1, n + 1):
        customers.append(Customer(
            customer_id=f"U-{index:04d}",
            name=fake.name(),
            age=random.randint(min_age, max_age),
            email=fake.email(),
            phone=fake.phone_number(),
            city=fake.city(),
        ))
    return customers


def generate_cars(n: int, automatic_ratio: float = 0.5,
                  min_year: int = 2010, max_year: int = 2021) -> list[Car]:
    if n < 1 or not (0 < automatic_ratio < 1):
        raise ValueError("Legalább egy autó és 0 és 1 közötti arány szükséges.")
    if not (1950 <= min_year <= max_year <= 2021):
        raise ValueError("Az oktatói mintagenerátor 1950-2021 közötti éveket támogat.")
    return sample_generate_cars(
        n, automatic_ratio=automatic_ratio, locale="hu_HU",
        unique=True, min_year=min_year, max_year=max_year,
    )


def generate_rentals(n: int, customers: list[Customer], cars: list[Car],
                     min_days: int = 1, max_days: int = 14,
                     min_daily_rate: int = 9000,
                     max_daily_rate: int = 30000) -> list[Rental]:
    if n < 1 or not customers or not cars:
        raise ValueError("A bérlésekhez ügyfelek és autók is szükségesek.")
    if not (1 <= min_days <= max_days):
        raise ValueError("Érvénytelen bérlési időtartam.")
    if not (1 <= min_daily_rate <= max_daily_rate):
        raise ValueError("Érvénytelen napidíj.")

    fake = Faker("hu_HU")
    available_from = {car.plate: date(2025, 1, 1) for car in cars}
    rentals = []
    for index in range(1, n + 1):
        customer = random.choice(customers)
        car = random.choice(cars)
        start = available_from[car.plate] + timedelta(days=random.randint(1, 15))
        duration = random.randint(min_days, max_days)
        end = start + timedelta(days=duration)
        available_from[car.plate] = end
        daily_rate = fake.random_int(min=min_daily_rate // 1000,
                                     max=max_daily_rate // 1000) * 1000
        rentals.append(Rental(
            rental_id=f"B-{index:05d}",
            customer_id=customer.customer_id,
            car_plate=car.plate,
            start_date=start.isoformat(),
            end_date=end.isoformat(),
            daily_rate=daily_rate,
            total_price=duration * daily_rate,
        ))
    return rentals


def generate_dataset(n: int) -> Dataset:
    if n < 1:
        raise ValueError("A generálandó lista mérete legalább 1 legyen.")
    parent_count = max(1, (n + 1) // 2)
    customers = generate_customers(parent_count)
    cars = generate_cars(parent_count)
    rentals = generate_rentals(n, customers, cars)
    dataset = Dataset(customers, cars, rentals)
    dataset.validate()
    return dataset
