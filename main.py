import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from data.basic.autokolcsonzo_generator import generate_dataset
from data.basic.autokolcsonzo_service import load, save
from data.basic.handler.autokolcsonzo_common import same_data
from data.basic.model_autokolcsonzo import Dataset

OUTPUT = PROJECT_ROOT / "kimenet"


def show_summary(dataset: Dataset) -> None:
    print(f"\nÜgyfelek száma: {len(dataset.customers)}")
    print(f"Autók száma: {len(dataset.cars)}")
    print(f"Bérlések száma: {len(dataset.rentals)}")
    print(f"Bérlések összértéke: {sum(r.total_price for r in dataset.rentals):,} Ft".replace(",", " "))
    print("\nElső három bérlés:")
    for item in dataset.rentals[:3]:
        print(f"  {item.rental_id}: {item.customer_id} - {item.car_plate}, "
              f"{item.start_date} / {item.end_date}, {item.total_price} Ft")


def demo(size: int) -> None:
    dataset = generate_dataset(size)
    show_summary(dataset)
    for name in ("csv", "json", "xlsx"):
        path = save(dataset, name, OUTPUT)
        loaded = load(name, OUTPUT)
        if not same_data(dataset, loaded):
            raise RuntimeError(f"Nem egyezik az eredeti és visszaolvasott adat: {name}")
        print(f"OK - {name.upper()} mentés és visszaolvasás: {path}")
    print("\nMindhárom formátum ellenőrzése sikeres!")


def interactive() -> None:
    dataset = None
    while True:
        print("\n" + "=" * 45)
        print("AUTÓKÖLCSÖNZŐ ADATKEZELŐ - FÓGEL BOGLÁRKA")
        print("=" * 45)
        print("1. Tesztadatok generálása")
        print("2. Mentés CSV formátumban")
        print("3. Mentés JSON formátumban")
        print("4. Mentés Excel (XLSX) formátumban")
        print("5. Mentett adatok visszaolvasása")
        print("6. Adatok összegzése és megjelenítése")
        print("7. Teljes próba három formátumban")
        print("0. Kilépés")
        choice = input("Választás: ").strip()

        try:
            if choice == "0":
                print("Viszontlátásra!")
                return
            if choice == "7":
                demo(int(input("Hány bérlést generáljunk? [például 10]: ")))
                continue
            if choice == "1":
                dataset = generate_dataset(int(input("Bérlések száma: ")))
                print("Az adatok elkészültek.")
                show_summary(dataset)
                continue
            if choice in ("2", "3", "4"):
                if dataset is None:
                    print("Előbb válaszd az 1. menüpontot!")
                    continue
                fmt = {"2": "csv", "3": "json", "4": "xlsx"}[choice]
                print(f"Sikeres mentés: {save(dataset, fmt, OUTPUT)}")
                continue
            if choice == "5":
                fmt = input("Melyik formátum? (csv / json / xlsx): ").strip().lower()
                loaded = load(fmt, OUTPUT)
                print("Sikeres visszaolvasás és kapcsolat-ellenőrzés.")
                if dataset is not None:
                    print("Egyezik a memóriában tárolt adatokkal:", same_data(dataset, loaded))
                dataset = loaded
                show_summary(dataset)
                continue
            if choice == "6":
                if dataset is None:
                    print("Még nincsenek adatok; előbb generálj vagy olvass be!")
                else:
                    show_summary(dataset)
                continue
            print("Ismeretlen menüpont.")
        except (ValueError, FileNotFoundError, KeyError, OSError) as error:
            print(f"Hiba: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Autókölcsönző CSV/JSON/XLSX beadandó")
    parser.add_argument("--demo", action="store_true", help="Teljes generálás, mentés és ellenőrzés")
    parser.add_argument("--size", type=int, default=10, help="Bérlések száma a demóban")
    args = parser.parse_args()
    if args.demo:
        demo(args.size)
    else:
        interactive()


if __name__ == "__main__":
    main()
