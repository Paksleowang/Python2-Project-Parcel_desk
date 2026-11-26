import pytest

from database import Database
from parcel import Parcel
from system import ParcelSystem
from tenant import Tenant


@pytest.fixture
def temp_database(tmp_path):
    return Database(tmp_path)


@pytest.fixture
def system(temp_database):
    return ParcelSystem(temp_database)


@pytest.fixture
def tenant():
    return Tenant("Sonam", 101)


@pytest.fixture
def parcel():
    return Parcel("AB12CD34", "Sonam", "01/01/2026", ["Box"])
