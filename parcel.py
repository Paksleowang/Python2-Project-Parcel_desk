"""Parcel model and parcel collection."""

import secrets
import string
from dataclasses import dataclass, field
from datetime import date, datetime

from errors import InvalidParcelError, ParcelNotFoundError

DATE_FORMAT = "%d/%m/%Y"


def parse_date(value: str | date) -> date:
    """Parse a date or DD/MM/YYYY string."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise InvalidParcelError("Date must be DD/MM/YYYY.")
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT).date()
    except ValueError as error:
        raise InvalidParcelError("Date must be a valid DD/MM/YYYY date.") from error


@dataclass
class Parcel:
    """One parcel received for a tenant."""

    pid: str
    receiver: str
    date: str
    items: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate parcel data after initialization."""
        if not isinstance(self.pid, str) or len(self.pid) != 8:
            raise InvalidParcelError("Parcel ID must contain 8 characters.")
        if not isinstance(self.receiver, str) or not self.receiver.strip():
            raise InvalidParcelError("Receiver name must not be blank.")
        self.receiver = self.receiver.strip()
        received = parse_date(self.date)
        self.date = received.strftime(DATE_FORMAT)
        if not isinstance(self.items, list) or not self.items:
            raise InvalidParcelError("Parcel must contain at least one item.")
        if any(not isinstance(item, str) or not item.strip() for item in self.items):
            raise InvalidParcelError("Item descriptions must not be blank.")
        self.items = [item.strip() for item in self.items]

    @property
    def received_date(self) -> date:
        return parse_date(self.date)

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "receiver": self.receiver,
            "date": self.date,
            "items": list(self.items),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Parcel":
        return cls(
            pid=data["pid"],
            receiver=data["receiver"],
            date=data["date"],
            items=list(data["items"]),
        )


class ParcelManager:
    """Creates, stores, searches, and iterates over parcels."""

    def __init__(self, parcels: list[Parcel] | None = None) -> None:
        self._parcels: list[Parcel] = []
        for parcel in parcels or []:
            self.add(parcel)

    @property
    def parcels(self) -> list[Parcel]:
        return self._parcels

    def _new_pid(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        existing = {parcel.pid for parcel in self._parcels}
        while True:
            pid = "".join(secrets.choice(alphabet) for _ in range(8))
            if pid not in existing:
                return pid

    def add(self, parcel: Parcel) -> Parcel:
        if not isinstance(parcel, Parcel):
            raise TypeError("parcel must be a Parcel instance")
        if any(p.pid == parcel.pid for p in self._parcels):
            from errors import DuplicateParcelError

            raise DuplicateParcelError(f"Parcel {parcel.pid} already exists.")
        self._parcels.append(parcel)
        return parcel

    def add_item(self, received_date: str, receiver: str, item: str) -> Parcel:
        """Add an item to an existing receiver/date parcel or create one."""
        date_value = parse_date(received_date).strftime(DATE_FORMAT)
        if not isinstance(receiver, str) or not receiver.strip():
            raise InvalidParcelError("Receiver name must not be blank.")
        if not isinstance(item, str) or not item.strip():
            raise InvalidParcelError("Item description must not be blank.")

        for parcel in self._parcels:
            if (
                parcel.receiver.casefold() == receiver.strip().casefold()
                and parcel.date == date_value
            ):
                parcel.items.append(item.strip())
                return parcel

        parcel = Parcel(
            pid=self._new_pid(),
            receiver=receiver.strip(),
            date=date_value,
            items=[item.strip()],
        )
        self._parcels.append(parcel)
        return parcel

    def find(self, pid: str) -> Parcel:
        if not isinstance(pid, str) or not pid.strip():
            raise ValueError("Parcel ID must not be blank.")
        for parcel in self._parcels:
            if parcel.pid == pid.strip():
                return parcel
        raise ParcelNotFoundError(f"Parcel ID '{pid}' was not found.")

    def __iter__(self):
        return iter(self._parcels)

    def __len__(self) -> int:
        return len(self._parcels)

    def to_list(self) -> list[dict]:
        return [parcel.to_dict() for parcel in self._parcels]
