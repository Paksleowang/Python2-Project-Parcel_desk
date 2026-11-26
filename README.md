# Parcel Management System

A beginner-friendly parcel desk application written in Python. It supports tenant registration, parcel tracking, desk assignment, pickup, overdue fee calculation, payment tracking, and JSON/CSV persistence.

## Features

- Register tenants and validate room numbers.
- Add parcels; items for the same receiver and received date are grouped together.
- Generate unique 8-character parcel IDs.
- Assign parcels to the matching registered receiver.
- Record parcel pickup.
- Calculate storage charges: the first 10 days are free; thereafter the fee is ฿1 per day.
- Record partial or full payments without allowing overpayment.
- Save parcel, tenant, desk, and collection data as JSON; payment history as CSV.
- CLI application and a small JSON HTTP API.
- Domain models, custom exceptions, iterator support, a persistence decorator, and a context manager.

## Requirements

- Python 3.10 or newer (the project uses modern type annotations).
- `pytest` is only needed to run tests.

No third-party package is required to run the application or API.

## Installation

### Windows

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/).
2. During installation, select **Add Python to PATH**.
3. Open PowerShell or Command Prompt.
4. Move into the project directory:

   ```powershell
   cd path\to\parcel_management
   ```

5. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

6. Activate it:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:

   ```bat
   .venv\Scripts\activate.bat
   ```

7. Install pytest for testing:

   ```powershell
   python -m pip install pytest
   ```

### macOS

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/) or use a suitable package manager.
2. Open Terminal and move into the project directory:

   ```bash
   cd /path/to/parcel_management
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate it:

   ```bash
   source .venv/bin/activate
   ```

5. Install pytest for testing:

   ```bash
   python -m pip install pytest
   ```

## Run the application

From the project root, with the virtual environment active:

```bash
python main.py
```

Choose an option from the menu. Use `0` to save and exit.

The application creates these data files beside the Python files:

- `parcels.json`
- `tenants.json`
- `desk.json`
- `collected.json`
- `payments.csv`

Do not manually edit these while the program is running. Back them up before making changes.

## Business rules

1. A tenant name cannot be blank.
2. Room numbers must be positive integers and cannot be duplicated.
3. A parcel must have a valid received date in `DD/MM/YYYY` format and a non-empty item.
4. Parcels with the same receiver and date are grouped.
5. A parcel can only be assigned to a tenant whose name matches the parcel receiver.
6. A parcel cannot be assigned twice while it is waiting at the desk.
7. The first 10 days after receipt are free. Starting on day 11, the fee is ฿1 per day.
8. Payments must be positive whole numbers and cannot exceed the current outstanding balance.
9. The system records payment history; overdue fees are calculated from the parcel's received date.

## Run tests

```bash
python -m pytest -v
```

## JSON API

The API uses Python's built-in `http.server`, so no external API framework is needed.

Start it in a separate terminal:

```bash
python api.py
```

Base address: `http://127.0.0.1:8000`

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/parcels` | List parcels |
| GET | `/api/desk` | List parcels waiting at the desk |
| GET | `/api/collected` | List collected parcels |
| GET | `/api/overdue/{PID}` | Get fee, paid amount, and balance |
| POST | `/api/parcels` | Add an item/parcel |
| POST | `/api/tenants` | Register a tenant |
| POST | `/api/assign` | Assign a parcel |
| POST | `/api/collect` | Collect a parcel |
| POST | `/api/payments` | Record a payment |

### Example requests

List parcels:

```bash
curl http://127.0.0.1:8000/api/parcels
```

Create a parcel:

```bash
curl -X POST http://127.0.0.1:8000/api/parcels \
  -H "Content-Type: application/json" \
  -d '{"date":"01/11/2026","receiver":"Sonam","item":"Package"}'
```

Register a tenant:

```bash
curl -X POST http://127.0.0.1:8000/api/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"Sonam","room":101}'
```

Assign a parcel:

```bash
curl -X POST http://127.0.0.1:8000/api/assign \
  -H "Content-Type: application/json" \
  -d '{"pid":"YOURPID1"}'
```

Check overdue balance:

```bash
curl http://127.0.0.1:8000/api/overdue/YOURPID1
```

The API is intended for local learning and development. It does not include authentication, TLS, or production-grade concurrency handling. Do not expose it to the public internet.

## OOP and Python concepts used

- **Encapsulation:** parcel and tenant behavior is kept in domain classes.
- **Composition:** `ParcelSystem` coordinates parcel, tenant, desk, pickup, overdue, payment, and database objects.
- **Iterator:** `ParcelManager` supports `for parcel in parcel_manager`.
- **Context manager:** `ParcelSystem` saves data when used with `with ParcelSystem() as system:`.
- **Decorator:** `@persist_after` saves data after successful state-changing operations.
- **Custom exceptions:** expected application errors are defined in `errors.py`.
- **Separation of concerns:** CLI, API, business logic, and persistence are separate modules.

## Project layout

```text
parcel_management/
├── main.py
├── api.py
├── system.py
├── parcel.py
├── tenant.py
├── desk.py
├── parcel_pickup.py
├── overdue.py
├── payment.py
├── database.py
├── errors.py
├── README.md
└── tests/
    ├── conftest.py
    ├── test_parcel.py
    ├── test_tenant.py
    ├── test_desk.py
    ├── test_pickup.py
    ├── test_overdue.py
    ├── test_payment.py
    ├── test_database.py
    └── test_system.py
```

