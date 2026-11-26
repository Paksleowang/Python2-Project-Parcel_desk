import pytest

from desk import ParcelDesk
from errors import ParcelAssignmentError, ParcelNotFoundError
from parcel_pick_up import ParcelPickup


def test_correct_tenant_collects_parcel(parcel, tenant):
    desk = ParcelDesk()
    desk.assign_parcel(parcel, tenant)
    pickup = ParcelPickup(desk)
    collected = pickup.collect(tenant, parcel.pid)
    assert collected["tenant"] == tenant.name
    assert len(desk) == 0
    assert len(pickup.collected) == 1


def test_wrong_tenant_cannot_collect(parcel, tenant):
    desk = ParcelDesk()
    desk.assign_parcel(parcel, tenant)
    pickup = ParcelPickup(desk)
    from tenant import Tenant

    with pytest.raises(ParcelAssignmentError):
        pickup.collect(Tenant("Pema", 102), parcel.pid)
    assert len(desk) == 1


def test_unknown_or_already_collected_pid_raises(parcel, tenant):
    desk = ParcelDesk()
    pickup = ParcelPickup(desk)
    with pytest.raises(ParcelNotFoundError):
        pickup.collect(tenant, parcel.pid)
    desk.assign_parcel(parcel, tenant)
    pickup.collect(tenant, parcel.pid)
    with pytest.raises(ParcelNotFoundError):
        pickup.collect(tenant, parcel.pid)
