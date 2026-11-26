from datetime import date

import pytest

from errors import InvalidPaymentError
from overdue import Overdue
from payment import Payment
from tenant import Tenant


def test_partial_payment_reduces_balance(parcel, tenant):
    payment = Payment(Overdue())
    today = date(2026, 1, 16)  # 5 chargeable days
    payment.make_payment(tenant, parcel.to_dict(), 2, today)
    assert payment.total_paid(parcel.pid) == 2
    assert payment.outstanding_fee(parcel.to_dict(), today) == 3


def test_exact_payment_clears_balance(parcel, tenant):
    payment = Payment(Overdue())
    today = date(2026, 1, 16)
    payment.make_payment(tenant, parcel.to_dict(), 5, today)
    assert payment.outstanding_fee(parcel.to_dict(), today) == 0


@pytest.mark.parametrize("amount", [0, -1, True, 1.5, "2", None])
def test_invalid_amount_raises(parcel, tenant, amount):
    with pytest.raises(InvalidPaymentError):
        Payment().make_payment(tenant, parcel.to_dict(), amount, date(2026, 1, 16))


def test_overpayment_rejected(parcel, tenant):
    with pytest.raises(InvalidPaymentError):
        Payment().make_payment(tenant, parcel.to_dict(), 100, date(2026, 1, 16))


def test_wrong_receiver_rejected(parcel):
    with pytest.raises(InvalidPaymentError):
        Payment().make_payment(
            Tenant("Pema", 102), parcel.to_dict(), 1, date(2026, 1, 16)
        )


def test_payment_date_and_fields(parcel, tenant):
    record = Payment().make_payment(tenant, parcel.to_dict(), 1, date(2026, 1, 16))
    assert record == {
        "pid": parcel.pid,
        "tenant": tenant.name,
        "room": tenant.room,
        "amount": 1,
        "date": "16/01/2026",
    }
