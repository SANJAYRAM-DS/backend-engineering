import hmac
import hashlib
from typing import Tuple

def constant_time_compare(val1: str, val2: str) -> bool:
    """Compare strings in constant time to prevent timing attacks."""
    return hmac.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))

def extract_client_info(request) -> Tuple[str, str]:
    """Extract Client IP and User-Agent from HTTP Request headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
    
    user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
    return ip, user_agent
