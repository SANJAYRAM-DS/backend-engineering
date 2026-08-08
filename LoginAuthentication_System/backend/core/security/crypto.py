import hashlib
import secrets
import bcrypt

def hash_token(raw_token: str) -> str:
    """Computes SHA-256 digest of a token string for indexing and secure store."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

def generate_opaque_token(length: int = 32) -> str:
    """Generates a cryptographically secure random urlsafe token."""
    return secrets.token_urlsafe(length)

def hash_password(plain_password: str) -> str:
    """Hashes password using bcrypt with work factor 12."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against stored bcrypt digest."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False
