"""This class is to store and record the parcels recieved."""
from parcel import Parcel


from parcel import Parcel


class ParcelDesk:
    def __init__(self, building: str):
        self.building = building
        self.desk: list[dict] = []

    def assign_parcel(self, parcel: Parcel, tenant_name: str, room: int) -> None:
        """Assign a parcel to a tenant and store the information."""

        assigned_parcel = {
            "name": tenant_name,
            "room": room,
            "parcel": parcel
        }

        self.desk.append(assigned_parcel)

    def show_parcels(self) -> None:
        """Display all parcels assigned to tenants."""

        for record in self.desk:
            parcel = record["parcel"]

            print(f"Tenant: {record['name']}")
            print(f"Room: {record['room']}")
            print(f"Parcel ID: {parcel.pid}")
            print(f"Date: {parcel.date}")
            print(f"Items: {parcel.items}")
            print()
