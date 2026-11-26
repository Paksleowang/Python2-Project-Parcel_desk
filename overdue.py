"""Overdue fee calculation."""

from datetime import date

from parcel import parse_date


class Overdue:
    FREE_DAYS = 10
    DAILY_FEE = 1

    def overdue_days(self, parcel: dict, today: date | None = None) -> int:
        if not isinstance(parcel, dict) or "date" not in parcel:
            raise ValueError("Parcel data must contain a received date.")
        today = today or date.today()
        if not isinstance(today, date):
            raise TypeError("today must be a date object.")
        waiting_days = (today - parse_date(parcel["date"])).days
        return max(waiting_days - self.FREE_DAYS, 0)

    def calculate_fee(self, parcel: dict, today: date | None = None) -> int:
        return self.overdue_days(parcel, today) * self.DAILY_FEE
