"""JSON and CSV persistence, with a context manager for safe application use."""

import csv
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from errors import ParcelStorageError


class Database:
    """Persistence layer. JSON stores application data; CSV stores payments."""

    PAYMENT_FIELDS = ["pid", "tenant", "room", "amount", "date"]

    def __init__(self, directory: str | Path | None = None) -> None:
        self.directory = Path(directory) if directory else Path(__file__).parent
        self.directory.mkdir(parents=True, exist_ok=True)
        self.parcels_path = self.directory / "parcels.json"
        self.tenants_path = self.directory / "tenants.json"
        self.desk_path = self.directory / "desk.json"
        self.collected_path = self.directory / "collected.json"
        self.payments_path = self.directory / "payments.csv"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        # Database does not swallow exceptions; saves happen explicitly.
        return False

    def save_json(self, path: Path, data) -> None:
        try:
            with NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.directory,
                delete=False, suffix=".tmp"
            ) as temporary:
                json.dump(data, temporary, indent=4, ensure_ascii=False)
                temporary.flush()
                os.fsync(temporary.fileno())
                temp_path = Path(temporary.name)
            temp_path.replace(path)
        except (OSError, TypeError, ValueError) as error:
            raise ParcelStorageError(f"Could not save {path.name}: {error}") from error

    def load_json(self, path: Path, default=None):
        if default is None:
            default = []
        if not path.exists():
            self.save_json(path, default)
            return default
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError(f"{path.name} must contain a JSON list.")
            return data
        except (OSError, json.JSONDecodeError, ValueError) as error:
            raise ParcelStorageError(f"Could not load {path.name}: {error}") from error

    def save_parcels(self, parcels: list[dict]) -> None:
        self.save_json(self.parcels_path, parcels)

    def load_parcels(self) -> list[dict]:
        return self.load_json(self.parcels_path)

    def save_tenants(self, tenants: list[dict]) -> None:
        self.save_json(self.tenants_path, tenants)

    def load_tenants(self) -> list[dict]:
        return self.load_json(self.tenants_path)

    def save_desk(self, desk: list[dict]) -> None:
        self.save_json(self.desk_path, desk)

    def load_desk(self) -> list[dict]:
        return self.load_json(self.desk_path)

    def save_collected(self, collected: list[dict]) -> None:
        self.save_json(self.collected_path, collected)

    def load_collected(self) -> list[dict]:
        return self.load_json(self.collected_path)

    def save_payments(self, payments: list[dict]) -> None:
        try:
            with self.payments_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.PAYMENT_FIELDS)
                writer.writeheader()
                writer.writerows(payments)
        except (OSError, csv.Error) as error:
            raise ParcelStorageError(f"Could not save payments: {error}") from error

    def load_payments(self) -> list[dict]:
        if not self.payments_path.exists():
            self.save_payments([])
            return []
        try:
            with self.payments_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != self.PAYMENT_FIELDS:
                    raise ValueError("Payments CSV has an invalid header.")
                result = []
                for row in reader:
                    result.append({
                        "pid": row["pid"],
                        "tenant": row["tenant"],
                        "room": int(row["room"]),
                        "amount": int(row["amount"]),
                        "date": row["date"],
                    })
                return result
        except (OSError, csv.Error, ValueError, KeyError) as error:
            raise ParcelStorageError(f"Could not load payments: {error}") from error

    def save_all(self, state: dict) -> None:
        self.save_parcels(state["parcels"])
        self.save_tenants(state["tenants"])
        self.save_desk(state["desk"])
        self.save_collected(state["collected"])
        self.save_payments(state["payments"])
