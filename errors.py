"""Custom exceptions used by the parcel management system."""


class ParcelSystemError(Exception):
    """Base exception for expected application errors."""


class ParcelError(ParcelSystemError):
    """Base exception for parcel-related errors."""


class InvalidParcelError(ParcelError, ValueError):
    """Raised when parcel data is invalid."""


class ParcelNotFoundError(ParcelError, LookupError):
    """Raised when a parcel cannot be found."""


class DuplicateParcelError(ParcelError):
    """Raised when a parcel already exists or is assigned."""


class TenantError(ParcelSystemError):
    """Base exception for tenant-related errors."""


class InvalidTenantError(TenantError, ValueError):
    """Raised when tenant data is invalid."""


class TenantNotFoundError(TenantError, LookupError):
    """Raised when a tenant cannot be found."""


class DuplicateTenantError(TenantError):
    """Raised when a tenant is already registered."""


class ParcelDeskError(ParcelSystemError):
    """Base exception for parcel-desk errors."""


class ParcelAssignmentError(ParcelDeskError):
    """Raised when an assignment is invalid."""


class ParcelStorageError(ParcelSystemError):
    """Raised when persistence fails."""


class PaymentError(ParcelSystemError):
    """Base exception for payment errors."""


class InvalidPaymentError(PaymentError, ValueError):
    """Raised when a payment is invalid."""
