class DomainError(Exception):
    """Base class for domain exceptions"""

class NotFoundError(DomainError):
    """Entity was not found"""

class BadRequestError(DomainError):
    """Request was invalid"""

class ConflictError(DomainError):
    """Resource conflict (e.g. already exists)"""

class InvalidImageFormatError(BadRequestError):
    """Raised when the uploaded image format is not supported"""
    pass
