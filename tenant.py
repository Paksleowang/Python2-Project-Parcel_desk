"""Tenant domain model and registry."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tenant:
    """A resident who can receive parcels."""

    name: str
    room: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Tenant name must not be blank.")
        if isinstance(self.room, bool) or not isinstance(self.room, int):
            raise ValueError("Room number must be an integer.")
        if self.room <= 0:
            raise ValueError("Room number must be positive.")

    @property
    def normalized_name(self) -> str:
        """Name normalized for case-insensitive comparisons."""
        return self.name.strip().casefold()

    def to_dict(self) -> dict:
        return {"name": self.name.strip(), "room": self.room}

    @classmethod
    def from_dict(cls, data: dict) -> "Tenant":
        return cls(name=data["name"], room=int(data["room"]))


class TenantRegistry:
    """Stores and searches registered tenants."""

    def __init__(self, tenants: list[Tenant] | None = None) -> None:
        self._tenants: list[Tenant] = []
        for tenant in tenants or []:
            self.add(tenant)

    def add(self, tenant: Tenant) -> Tenant:
        if not isinstance(tenant, Tenant):
            raise TypeError("tenant must be a Tenant instance")
        if any(t.normalized_name == tenant.normalized_name for t in self._tenants):
            from errors import DuplicateTenantError

            raise DuplicateTenantError(f"{tenant.name} is already registered.")
        if any(t.room == tenant.room for t in self._tenants):
            from errors import DuplicateTenantError

            raise DuplicateTenantError(f"Room {tenant.room} is already registered.")
        self._tenants.append(tenant)
        return tenant

    def find(self, name: str) -> Tenant:
        from errors import TenantNotFoundError

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tenant name must not be blank.")
        for tenant in self._tenants:
            if tenant.normalized_name == name.strip().casefold():
                return tenant
        raise TenantNotFoundError(f"Tenant '{name}' was not found.")

    def __iter__(self):
        return iter(self._tenants)

    def __len__(self) -> int:
        return len(self._tenants)

    def to_list(self) -> list[dict]:
        return [tenant.to_dict() for tenant in self._tenants]
