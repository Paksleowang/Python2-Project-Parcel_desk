"""Application service layer shared by CLI and HTTP API."""

from datetime import date
from functools import wraps

from database import Database
from desk import ParcelDesk
from overdue import Overdue
from parcel import Parcel, ParcelManager
from parcel_pick_up import ParcelPickup
from payment import Payment
from tenant import Tenant, TenantRegistry


def persist_after(method):
    """Save application state after a successful mutating operation."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.save_all()
        return result

    return wrapper


class ParcelSystem:
    """Coordinates domain objects and persistence."""

    def __init__(self, database: Database | None = None) -> None:
        self.db = database or Database()
        parcel_objects = [Parcel.from_dict(row) for row in self.db.load_parcels()]
        self.parcel_manager = ParcelManager(parcel_objects)
        self.tenants = TenantRegistry(
            [Tenant.from_dict(row) for row in self.db.load_tenants()]
        )
        self.desk = ParcelDesk()
        self.desk.desk = self.db.load_desk()
        self.pickup = ParcelPickup(self.desk)
        self.pickup.collected = self.db.load_collected()
        self.overdue = Overdue()
        self.payment = Payment(self.overdue)
        self.payment.payments = self.db.load_payments()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type is None:
            self.save_all()
        return False

    def state(self) -> dict:
        return {
            "parcels": self.parcel_manager.to_list(),
            "tenants": self.tenants.to_list(),
            "desk": self.desk.desk,
            "collected": self.pickup.collected,
            "payments": self.payment.payments,
        }

    def save_all(self) -> None:
        self.db.save_all(self.state())

    @persist_after
    def add_parcel(self, received_date: str, receiver: str, item: str) -> Parcel:
        return self.parcel_manager.add_item(received_date, receiver, item)

    @persist_after
    def register_tenant(self, name: str, room: int) -> Tenant:
        return self.tenants.add(Tenant(name, room))

    def find_parcel(self, pid: str) -> Parcel:
        return self.parcel_manager.find(pid)

    def find_tenant(self, name: str) -> Tenant:
        return self.tenants.find(name)

    @persist_after
    def assign_parcel(self, pid: str):
        parcel = self.find_parcel(pid)
        tenant = self.find_tenant(parcel.receiver)
        return self.desk.assign_parcel(parcel, tenant)

    @persist_after
    def collect_parcel(self, tenant_name: str, pid: str):
        tenant = self.find_tenant(tenant_name)
        return self.pickup.collect(tenant, pid)

    def overdue_summary(self, pid: str, today: date | None = None) -> dict:
        parcel = self.find_parcel(pid)
        fee = self.overdue.calculate_fee(parcel.to_dict(), today)
        paid = self.payment.total_paid(pid)
        return {
            "pid": pid,
            "days_overdue": self.overdue.overdue_days(parcel.to_dict(), today),
            "fee": fee,
            "paid": paid,
            "balance": max(fee - paid, 0),
        }

    @persist_after
    def make_payment(
        self, tenant_name: str, pid: str, amount: int, today: date | None = None
    ):
        tenant = self.find_tenant(tenant_name)
        parcel = self.find_parcel(pid)
        return self.payment.make_payment(tenant, parcel.to_dict(), amount, today)

    def __iter__(self):
        return iter(self.parcel_manager)
