# 10 — URL Validation & Security Sanitization

## 1. Learning Objective
Learn to sanitize target URLs against malicious schemes, open redirect vulnerabilities, and Server-Side Request Forgery (SSRF).

---

## 2. Security Checks
1. **Protocol Validation**: Strictly permit `http://` and `https://`. Reject `file://`, `ftp://`, `javascript:`, `data:`.
2. **SSRF Prevention**: Block shortening internal IP ranges (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `localhost`).
3. **Loop Prevention**: Prevent users from shortening the URL shortener's own domain (`short.ly/aB72x` -> `short.ly/aB72x`).

---

## 3. Pydantic Validator Implementation

```python
import ipaddress
from urllib.parse import urlparse

FORBIDDEN_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}

def validate_url_security(url_str: str) -> str:
    parsed = urlparse(url_str)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Scheme must be http or https")
    if parsed.hostname in FORBIDDEN_HOSTS:
        raise ValueError("Cannot shorten local loopback addresses")
    return url_str
```
