import pytest

from errors import DuplicateParcelError, InvalidParcelError, ParcelNotFoundError
from parcel import Parcel, ParcelManager


@pytest.fixture
def manager():
    return ParcelManager()


def test_add_item_creates_parcel(manager):
    parcel = manager.add_item("01/01/2026", "Sonam", "Box")
    assert parcel.receiver == "Sonam"
    assert parcel.items == ["Box"]
    assert len(parcel.pid) == 8
    assert len(manager) == 1


def test_same_receiver_and_date_groups_items(manager):
    first = manager.add_item("01/01/2026", "Sonam", "Box")
    second = manager.add_item("01/01/2026", "sonam", "Envelope")
    assert first is second
    assert first.items == ["Box", "Envelope"]
    assert len(manager) == 1


def test_different_date_or_receiver_creates_new_parcel(manager):
    manager.add_item("01/01/2026", "Sonam", "Box")
    manager.add_item("02/01/2026", "Sonam", "Box")
    manager.add_item("01/01/2026", "Pema", "Box")
    assert len(manager) == 3


def test_generated_ids_are_unique(manager):
    for day in range(1, 21):
        manager.add_item(f"{day:02d}/01/2026", "Sonam", "Box")
    ids = [parcel.pid for parcel in manager]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize(
    "received,receiver,item",
    [
        ("bad-date", "Sonam", "Box"),
        ("31/02/2026", "Sonam", "Box"),
        ("01/01/2026", "", "Box"),
        ("01/01/2026", "Sonam", " "),
    ],
)
def test_invalid_parcel_inputs(manager, received, receiver, item):
    with pytest.raises(InvalidParcelError):
        manager.add_item(received, receiver, item)


def test_find_existing_and_missing(manager):
    parcel = manager.add_item("01/01/2026", "Sonam", "Box")
    assert manager.find(parcel.pid) is parcel
    with pytest.raises(ParcelNotFoundError):
        manager.find("NOPE0000")


def test_duplicate_parcel_id_is_rejected(parcel):
    manager = ParcelManager([parcel])
    with pytest.raises(DuplicateParcelError):
        manager.add(parcel)


def test_parcel_serialization_round_trip(parcel):
    assert Parcel.from_dict(parcel.to_dict()) == parcel


def test_iterator_returns_parcels(manager):
    manager.add_item("01/01/2026", "Sonam", "Box")
    assert all(isinstance(item, Parcel) for item in manager)
