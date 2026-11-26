import pytest

from errors import DuplicateTenantError, TenantNotFoundError
from tenant import Tenant, TenantRegistry


@pytest.mark.parametrize("name,room", [("Sonam", 1), ("Pema", 1001)])
def test_valid_tenant(name, room):
    tenant = Tenant(name, room)
    assert tenant.name == name
    assert tenant.room == room


@pytest.mark.parametrize(
    "name,room",
    [
        ("", 101),
        ("   ", 101),
        ("Sonam", 0),
        ("Sonam", -1),
        ("Sonam", "101"),
        ("Sonam", True),
    ],
)
def test_invalid_tenant_inputs(name, room):
    with pytest.raises(ValueError):
        Tenant(name, room)


def test_registry_add_and_find(tenant):
    registry = TenantRegistry()
    registry.add(tenant)
    assert registry.find("sonam") is tenant
    assert len(registry) == 1


@pytest.mark.parametrize(
    "new_tenant",
    [
        Tenant("SONAM", 102),
        Tenant("Pema", 101),
    ],
)
def test_registry_rejects_duplicate_name_or_room(tenant, new_tenant):
    registry = TenantRegistry([tenant])
    with pytest.raises(DuplicateTenantError):
        registry.add(new_tenant)


def test_registry_unknown_tenant_raises():
    with pytest.raises(TenantNotFoundError):
        TenantRegistry().find("Nobody")


def test_tenant_serialization_round_trip(tenant):
    assert Tenant.from_dict(tenant.to_dict()) == tenant
