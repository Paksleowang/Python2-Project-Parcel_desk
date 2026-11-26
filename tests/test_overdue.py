from datetime import date

import pytest

from overdue import Overdue


@pytest.mark.parametrize(
    "today,expected_days,expected_fee",
    [
        (date(2026, 1, 1), 0, 0),
        (date(2026, 1, 11), 0, 0),  # 10 free days
        (date(2026, 1, 12), 1, 1),  # day 11
        (date(2026, 1, 16), 5, 5),
    ],
)
def test_fee_boundary(parcel, today, expected_days, expected_fee):
    overdue = Overdue()
    data = parcel.to_dict()
    assert overdue.overdue_days(data, today) == expected_days
    assert overdue.calculate_fee(data, today) == expected_fee


def test_future_received_date_has_zero_fee(parcel):
    parcel.date = "10/01/2026"
    assert Overdue().calculate_fee(parcel.to_dict(), date(2026, 1, 1)) == 0


@pytest.mark.parametrize("date_text", ["", "2026-01-01", "31/02/2026"])
def test_invalid_date_rejected(parcel, date_text):
    parcel.date = date_text
    with pytest.raises(ValueError):
        Overdue().calculate_fee(parcel.to_dict(), date(2026, 1, 20))
