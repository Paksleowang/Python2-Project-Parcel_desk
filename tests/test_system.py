import pytest

from errors import DuplicateTenantError, ParcelNotFoundError
from system import ParcelSystem


def test_system_operations_persist(temp_database):
    system = ParcelSystem(temp_database)
    tenant = system.register_tenant("Sonam", 101)
    parcel = system.add_parcel("01/01/2026", tenant.name, "Package")
    system.assign_parcel(parcel.pid)
    assert system.desk.is_assigned(parcel.pid)

    restarted = ParcelSystem(temp_database)
    assert restarted.find_parcel(parcel.pid).receiver == "Sonam"
    assert restarted.find_tenant("sonam").room == 101
    assert restarted.desk.is_assigned(parcel.pid)


def test_duplicate_tenant_rejected_and_not_saved(system):
    system.register_tenant("Sonam", 101)
    with pytest.raises(DuplicateTenantError):
        system.register_tenant("sonam", 102)


def test_unknown_parcel_raises(system):
    with pytest.raises(ParcelNotFoundError):
        system.find_parcel("NOPE0000")


def test_context_manager_saves(temp_database):
    with ParcelSystem(temp_database) as system:
        system.register_tenant("Sonam", 101)
    assert ParcelSystem(temp_database).find_tenant("Sonam").room == 101


def test_end_to_end_assignment_pickup(system):
    tenant = system.register_tenant("Sonam", 101)
    parcel = system.add_parcel("01/01/2026", tenant.name, "Package")
    system.assign_parcel(parcel.pid)
    system.collect_parcel("Sonam", parcel.pid)
    assert not system.desk.is_assigned(parcel.pid)
    assert system.pickup.collected[0]["parcel"]["pid"] == parcel.pid
