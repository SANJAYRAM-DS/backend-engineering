from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

signer = TimestampSigner(salt="user-email-verification-password-reset")

def generate_email_token(user_id: str) -> str:
    """Generates signed cryptographic email verification token."""
    return signer.sign(user_id)

def verify_email_token(token: str, max_age_seconds: int = 86400) -> str:
    """Verifies email token and returns user_id if valid."""
    try:
        user_id = signer.unsign(token, max_age=max_age_seconds)
        return user_id
    except (BadSignature, SignatureExpired):
        return None
