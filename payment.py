"""Payment tracking for overdue parcel fees."""

from datetime import date
from tenant import Tenant
from overdue import Overdue
from errors import InvalidPaymentError


class Payment:
    FIELDS = ("pid", "tenant", "room", "amount", "date")

    def __init__(self, overdue: Overdue | None = None) -> None:
        self.overdue = overdue or Overdue()
        self.payments: list[dict] = []

    def total_paid(self, pid: str) -> int:
        return sum(record["amount"] for record in self.payments if record["pid"] == pid)

    def outstanding_fee(self, parcel: dict, today: date | None = None) -> int:
        total_due = self.overdue.calculate_fee(parcel, today)
        return max(total_due - self.total_paid(parcel["pid"]), 0)

    def make_payment(
        self,
        tenant: Tenant,
        parcel: dict,
        amount: int,
        today: date | None = None,
    ) -> dict:
        if not isinstance(tenant, Tenant):
            raise InvalidPaymentError("A valid tenant is required.")
        if not isinstance(parcel, dict) or not parcel.get("pid"):
            raise InvalidPaymentError("Valid parcel data is required.")
        if parcel.get("receiver", "").strip().casefold() != tenant.normalized_name:
            raise InvalidPaymentError("This tenant is not the parcel receiver.")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise InvalidPaymentError("Payment amount must be a positive whole number.")

        today = today or date.today()
        balance = self.outstanding_fee(parcel, today)
        if balance <= 0:
            raise InvalidPaymentError("No overdue balance is outstanding.")
        if amount > balance:
            raise InvalidPaymentError(
                f"Payment exceeds outstanding balance of {balance} baht."
            )

        record = {
            "pid": parcel["pid"],
            "tenant": tenant.name,
            "room": tenant.room,
            "amount": amount,
            "date": today.strftime("%d/%m/%Y"),
        }
        self.payments.append(record)
        return record
