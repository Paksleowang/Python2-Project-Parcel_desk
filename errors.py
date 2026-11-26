
class ParcelSystemError(Exception):
    """Base exception for the parcel management system."""
    pass



# Parcel errors


class ParcelError(ParcelSystemError):
    """Base exception for parcel-related errors."""
    pass


class InvalidParcelError(ParcelError):
    """Raised when parcel information is invalid."""
    pass


class ParcelNotFoundError(ParcelError):
    """Raised when a parcel cannot be found."""
    pass


class DuplicateParcelError(ParcelError):
    """Raised when a parcel is already registered."""
    pass



# Tenant errors


class TenantError(ParcelSystemError):
    """Base exception for tenant-related errors."""
    pass


class InvalidTenantError(TenantError):
    """Raised when tenant information is invalid."""
    pass


class TenantNotFoundError(TenantError):
    """Raised when a tenant cannot be found."""
    pass


class DuplicateTenantError(TenantError):
    """Raised when a tenant is already registered."""
    pass



# Parcel desk errors


class ParcelDeskError(ParcelSystemError):
    """Base exception for parcel desk-related errors."""
    pass


class ParcelAssignmentError(ParcelDeskError):
    """Raised when a parcel cannot be assigned to a tenant."""
    pass
 
# Storage errors


class ParcelStorageError(ParcelSystemError):
    """Raised when saving or loading parcel data fails."""
    pass
