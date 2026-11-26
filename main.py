"""Command-line entry point."""

from errors import ParcelSystemError
from system import ParcelSystem


def prompt_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a whole number.")


def show_parcels(system: ParcelSystem) -> None:
    if not len(system.parcel_manager):
        print("No parcels registered.")
        return
    for parcel in system:
        print(
            f"{parcel.pid} | {parcel.receiver} | "
            f"{parcel.date} | {', '.join(parcel.items)}"
        )


def show_desk(system: ParcelSystem) -> None:
    if not system.desk.desk:
        print("No parcels waiting at the desk.")
        return
    for record in system.desk:
        parcel = record["parcel"]
        print(
            f"{parcel['pid']} | {record['name']} (Room {record['room']}) | "
            f"{', '.join(parcel['items'])}"
        )


def show_collected(system: ParcelSystem) -> None:
    if not system.pickup.collected:
        print("No parcels have been collected.")
        return
    for record in system.pickup.collected:
        parcel = record["parcel"]
        print(
            f"{parcel['pid']} | {record['tenant']} "
            f"(Room {record['room']}) | {parcel['date']}"
        )


def show_payments(system: ParcelSystem) -> None:
    if not system.payment.payments:
        print("No payments recorded.")
        return
    for record in system.payment.payments:
        print(
            f"{record['date']} | {record['pid']} | "
            f"{record['tenant']} | ฿{record['amount']}"
        )


def menu(system: ParcelSystem) -> None:
    options = {
        "1": "Add parcel",
        "2": "Register tenant",
        "3": "View parcels",
        "4": "Assign parcel",
        "5": "View parcel desk",
        "6": "Collect parcel",
        "7": "Check overdue fee",
        "8": "Make payment",
        "9": "View payment records",
        "10": "View collected parcels",
        "0": "Save and exit",
    }

    while True:
        print("\n=== PARCEL MANAGEMENT SYSTEM ===")
        for key, label in options.items():
            print(f"{key}. {label}")
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                received = input("Received date (DD/MM/YYYY): ").strip()
                receiver = input("Receiver name: ").strip()
                item = input("Item description: ").strip()
                parcel = system.add_parcel(received, receiver, item)
                print(f"Saved parcel: {parcel.pid}")

            elif choice == "2":
                name = input("Tenant name: ").strip()
                room = prompt_int("Room number: ")
                system.register_tenant(name, room)
                print("Tenant registered.")

            elif choice == "3":
                show_parcels(system)

            elif choice == "4":
                pid = input("Parcel ID: ").strip()
                record = system.assign_parcel(pid)
                print(f"Assigned to {record['name']} in room {record['room']}.")

            elif choice == "5":
                show_desk(system)

            elif choice == "6":
                name = input("Tenant name: ").strip()
                pid = input("Parcel ID: ").strip()
                system.collect_parcel(name, pid)
                print("Parcel collected.")

            elif choice == "7":
                pid = input("Parcel ID: ").strip()
                summary = system.overdue_summary(pid)
                print(f"Days overdue: {summary['days_overdue']}")
                print(f"Fee: ฿{summary['fee']}")
                print(f"Paid: ฿{summary['paid']}")
                print(f"Balance: ฿{summary['balance']}")

            elif choice == "8":
                name = input("Tenant name: ").strip()
                pid = input("Parcel ID: ").strip()
                amount = prompt_int("Payment amount (baht): ")
                system.make_payment(name, pid, amount)
                print("Payment recorded.")

            elif choice == "9":
                show_payments(system)

            elif choice == "10":
                show_collected(system)

            elif choice == "0":
                system.save_all()
                print("Data saved. Goodbye.")
                return

            else:
                print("Unknown choice. Please choose a menu number.")

        except (ParcelSystemError, ValueError, TypeError) as error:
            print(f"Error: {error}")


def main() -> None:
    try:
        with ParcelSystem() as system:
            menu(system)
    except ParcelSystemError as error:
        print(f"Could not start/save the application: {error}")


if __name__ == "__main__":
    main()
