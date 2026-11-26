
from dataclasses import dataclass, field
import secrets
import string
import json
from pathlib import Path

PATH = Path(__file__).parent/"parcel.json"

@dataclass
class Parcel:
    receiver: str
    parcels: list[dict] = field(default_factory=list)

    def pID(self) -> str:
        """Return a unique parcel ID."""
        alphanumeric = string.ascii_letters + string.digits

        existing_pids = []

        for parcel in self.parcels:
            existing_pids.append(parcel["pid"])

        while True:
            pid = "".join(
                secrets.choice(alphanumeric) for _ in range(8)
            )

            if pid not in existing_pids:
                return pid

    def add_item(self, date: str, receiver: str, item: str) -> None:
        """Add an item to an existing parcel or create a new parcel."""

        for parcel in self.parcels:
            if parcel["receiver"] == receiver and parcel["date"] == date:
                parcel["items"].append(item)
                print("Item added to existing parcel")
                return
        pid = self.pID()

        new_parcel = {
            "pid": pid,
            "receiver": receiver,
            "date": date,
            "items": [item]
        }
        self.parcels.append(new_parcel)
        print("New parcel created")
    
    def save(self) -> None:
        """Save the parcel list to a JSON file."""
        with open(PATH, "w",encoding="utf-8") as file:
            json.dump(self.parcels, file, indent=4) 
        return None  

    def show_pID(self) -> None:
        """Display parcel IDs and their items."""

        for parcel in self.parcels:
            print(f"Parcel ID: {parcel['pid']}")
            print(f"Receiver: {parcel['receiver']}")
            print(f"Date: {parcel['date']}")
            print(f"Items: {parcel['items']}")
            print()


if __name__ == "__main__":

    sonam = Parcel("Sonam")

    sonam.add_item("21/08/2026", "Sonam", "box-1")
    sonam.add_item("21/08/2026", "Sonam", "box-2")
    sonam.add_item("22/08/2026", "Sonam", "box-3")
    sonam.add_item("21/08/2026", "Pema", "box-4")
    sonam.save()

    sonam.show_pID()
