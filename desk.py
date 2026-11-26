"""Parcel desk assignment service."""

from errors import DuplicateParcelError, ParcelAssignmentError
from parcel import Parcel
from tenant import Tenant


class ParcelDesk:
    """Tracks parcels currently waiting for collection."""

    def __init__(self, building: str = "Parcel Desk") -> None:
        if not isinstance(building, str) or not building.strip():
            raise ValueError("Building name must not be blank.")
        self.building = building.strip()
        self.desk: list[dict] = []

    def is_assigned(self, pid: str) -> bool:
        return any(record["parcel"]["pid"] == pid for record in self.desk)

    def assign_parcel(self, parcel: Parcel | dict, tenant: Tenant) -> dict:
        if isinstance(parcel, Parcel):
            parcel_data = parcel.to_dict()
        elif isinstance(parcel, dict):
            parcel_data = dict(parcel)
        else:
            raise ParcelAssignmentError("Parcel must be a Parcel or parcel dictionary.")
        if not isinstance(tenant, Tenant):
            raise ParcelAssignmentError("A valid tenant is required.")
        if parcel_data.get("receiver", "").strip().casefold() != tenant.normalized_name:
            raise ParcelAssignmentError("Parcel receiver does not match this tenant.")
        pid = parcel_data.get("pid")
        if not pid:
            raise ParcelAssignmentError("Parcel has no parcel ID.")
        if self.is_assigned(pid):
            raise DuplicateParcelError(f"Parcel {pid} is already at the desk.")

        record = {
            "name": tenant.name,
            "room": tenant.room,
            "parcel": parcel_data,
        }
        self.desk.append(record)
        return record

    def remove_assignment(self, pid: str) -> dict:
        for index, record in enumerate(self.desk):
            if record["parcel"]["pid"] == pid:
                return self.desk.pop(index)
        raise ParcelAssignmentError(f"Parcel {pid} is not waiting at the desk.")

    def __iter__(self):
        return iter(self.desk)

    def __len__(self) -> int:
        return len(self.desk)
