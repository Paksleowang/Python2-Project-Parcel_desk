import csv

import pytest

from errors import ParcelStorageError


def test_json_save_load(temp_database, parcel):
    data = [parcel.to_dict()]
    temp_database.save_parcels(data)
    assert temp_database.load_parcels() == data


def test_tenant_data_save_load(temp_database, tenant):
    temp_database.save_tenants([tenant.to_dict()])
    assert temp_database.load_tenants() == [tenant.to_dict()]


def test_missing_data_files_load_empty(temp_database):
    assert temp_database.load_parcels() == []
    assert temp_database.load_payments() == []


def test_payments_are_csv_and_round_trip(temp_database):
    data = [
        {
            "pid": "AB12CD34",
            "tenant": "Sonam",
            "room": 101,
            "amount": 4,
            "date": "16/01/2026",
        }
    ]
    temp_database.save_payments(data)
    with temp_database.payments_path.open(newline="", encoding="utf-8") as file:
        assert list(csv.DictReader(file))[0]["amount"] == "4"
    assert temp_database.load_payments() == data


def test_corrupt_json_raises(temp_database):
    temp_database.parcels_path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ParcelStorageError):
        temp_database.load_parcels()


def test_context_manager_does_not_suppress_exception(temp_database):
    with pytest.raises(RuntimeError), temp_database:
        raise RuntimeError("expected")
