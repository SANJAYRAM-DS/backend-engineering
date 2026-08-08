from typing import Optional, Dict, Any

class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class AuthenticationError(BaseAppException):
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, details=details)

class PermissionDeniedError(BaseAppException):
    def __init__(self, message: str = "Permission denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, details=details)

class NotFoundError(BaseAppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, details=details)

class AccountLockedError(BaseAppException):
    def __init__(self, message: str = "Account locked due to multiple failed login attempts", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=423, details=details)

class TokenReuseError(BaseAppException):
    def __init__(self, message: str = "Security alert: Token reuse detected. Session revoked.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, details=details)

class RateLimitExceededError(BaseAppException):
    def __init__(self, message: str = "Rate limit exceeded. Please try again later.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=429, details=details)
