# Phase 30: Global Exception Handling & Uniform Responses

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 30 of 35  
> **Target Path**: `docs/30-exception-handling.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Building a centralized exception handling architecture that catches uncaught exceptions across all API endpoints.
* Preventing sensitive implementation details (database queries, stack traces, path names) from leaking in production error responses.
* Standardizing API error responses using RFC 7807 Problem Details JSON format.
* Mapping custom domain exceptions (`AuthenticationException`, `PermissionDeniedException`, `ValidationException`) to accurate HTTP status codes.

---

## 2. Global Exception Architecture

```mermaid
flowchart TD
    Endpoint["API View Execution"] -->|Raises Exception| Router["Django Ninja API Router"]
    Router --> Handler["Global Exception Handler Middleware"]
    Handler --> CheckType{"Custom Domain Exception?"}
    CheckType -->|Yes (e.g. SecurityException)| FormatCustom["Format Safe JSON Error Response"]
    CheckType -->|No (Unhandled 500 Error)| LogTrace["Log Full Stack Trace to Sentry / Logs"]
    LogTrace --> Format500["Return Generic Safe 500 JSON"]
    FormatCustom --> Client["Client Receives Standard RFC 7807 Payload"]
    Format500 --> Client
```

---

## 3. Production Exception Handler Implementation

### Custom Domain Exception Base Class

File path: `core/exceptions.py`

```python
"""
Custom Application Domain Exceptions Hierarchy.
"""
from typing import Optional, Dict, Any


class BaseAppException(Exception):
    """Base class for all application domain exceptions."""
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class AuthenticationException(BaseAppException):
    def __init__(self, message: str = "Authentication failed.", status_code: int = 401, details: Optional[dict] = None):
        super().__init__(message, status_code, details)


class PermissionDeniedException(BaseAppException):
    def __init__(self, message: str = "Permission denied.", status_code: int = 403, details: Optional[dict] = None):
        super().__init__(message, status_code, details)


class SecurityException(BaseAppException):
    def __init__(self, message: str = "Security policy violation.", status_code: int = 400, details: Optional[dict] = None):
        super().__init__(message, status_code, details)
```

### Ninja API Exception Registration Handler

File path: `core/handlers.py`

```python
"""
Global Django Ninja Exception Handlers ensuring uniform RFC 7807 error responses.
"""
from ninja import NinjaAPI
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from core.exceptions import BaseAppException
import logging
import uuid

logger = logging.getLogger("core.exceptions")


def register_exception_handlers(api: NinjaAPI) -> None:

    @api.exception_handler(BaseAppException)
    def custom_app_exception_handler(request: HttpRequest, exc: BaseAppException):
        """Handles all expected domain exceptions safely."""
        error_id = str(uuid.uuid4())[:8]
        payload = {
            "error": {
                "id": error_id,
                "type": exc.__class__.__name__,
                "message": exc.message,
                "status": exc.status_code,
                "details": exc.details,
            }
        }
        return JsonResponse(payload, status=exc.status_code)

    @api.exception_handler(Exception)
    def unhandled_exception_handler(request: HttpRequest, exc: Exception):
        """
        Catches any unexpected internal server error (500).
        Logs the complete stack trace internally while masking sensitive details from the client response.
        """
        error_id = str(uuid.uuid4())
        logger.error(f"UNHANDLED_EXCEPTION [Error ID {error_id}]: {str(exc)}", exc_info=True)

        message = "An unexpected internal server error occurred."
        details = {}

        # Expose details ONLY in Debug development mode
        if settings.DEBUG:
            message = str(exc)
            details = {"type": exc.__class__.__name__}

        payload = {
            "error": {
                "id": error_id,
                "type": "InternalServerError",
                "message": message,
                "status": 500,
                "details": details,
            }
        }
        return JsonResponse(payload, status=500)
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. **Why is returning raw stack traces (e.g. `Traceback (most recent call last)...`) to API clients a critical security risk?**  
   *Answer: Stack traces leak confidential implementation details including file system paths, database table names, SQL query syntax, library versions, and third-party dependency names, giving attackers exact targets for exploitation.*

2. **Why do we attach a unique `error_id` (UUID) to every error response?**  
   *Answer: An `error_id` allows users or frontend apps to report a specific error code to support without revealing sensitive internal logs. Developers can cross-reference the `error_id` in internal log aggregators (e.g. Datadog / Sentry) to find the exact stack trace.*

### Practical Exercise
* Write an automated test asserting that triggering a database connection failure returns a sanitized `500 Internal Server Error` response containing an `error_id` and masking the raw database password/connection string.
