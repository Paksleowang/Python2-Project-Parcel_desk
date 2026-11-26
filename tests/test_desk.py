import pytest

from desk import ParcelDesk
from errors import DuplicateParcelError, ParcelAssignmentError
from tenant import Tenant


def test_assign_correct_receiver(parcel, tenant):
    desk = ParcelDesk()
    record = desk.assign_parcel(parcel, tenant)
    assert record["name"] == tenant.name
    assert record["room"] == tenant.room
    assert record["parcel"]["pid"] == parcel.pid
    assert len(desk) == 1


def test_wrong_tenant_cannot_be_assigned(parcel):
    desk = ParcelDesk()
    with pytest.raises(ParcelAssignmentError):
        desk.assign_parcel(parcel, Tenant("Pema", 102))


def test_duplicate_assignment_is_rejected(parcel, tenant):
    desk = ParcelDesk()
    desk.assign_parcel(parcel, tenant)
    with pytest.raises(DuplicateParcelError):
        desk.assign_parcel(parcel, tenant)


def test_remove_assignment(parcel, tenant):
    desk = ParcelDesk()
    desk.assign_parcel(parcel, tenant)
    removed = desk.remove_assignment(parcel.pid)
    assert removed["parcel"]["pid"] == parcel.pid
    assert len(desk) == 0


def test_remove_unknown_assignment_raises():
    with pytest.raises(ParcelAssignmentError):
        ParcelDesk().remove_assignment("NOPE0000")


def test_invalid_parcel_type_rejected(tenant):
    with pytest.raises(ParcelAssignmentError):
        ParcelDesk().assign_parcel(object(), tenant)
