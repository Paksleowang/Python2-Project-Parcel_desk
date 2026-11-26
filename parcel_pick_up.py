"""Parcel collection service."""

from desk import ParcelDesk
from errors import ParcelAssignmentError, ParcelNotFoundError
from tenant import Tenant


class ParcelPickup:
    def __init__(self, desk: ParcelDesk) -> None:
        self.desk = desk
        self.collected: list[dict] = []

    def collect(self, tenant: Tenant, pid: str) -> dict:
        if not isinstance(tenant, Tenant):
            raise TypeError("tenant must be a Tenant instance")
        for record in self.desk.desk:
            parcel = record["parcel"]
            if parcel["pid"] == pid:
                if record["name"].casefold() != tenant.name.casefold():
                    raise ParcelAssignmentError(
                        f"Parcel {pid} is not assigned to {tenant.name}."
                    )
                assigned = self.desk.remove_assignment(pid)
                collected = {
                    "tenant": tenant.name,
                    "room": tenant.room,
                    "parcel": assigned["parcel"],
                }
                self.collected.append(collected)
                return collected
        raise ParcelNotFoundError(f"Parcel {pid} is not waiting for pickup.")
