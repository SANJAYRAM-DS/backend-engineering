from django.http import HttpResponse

def set_auth_cookies(response: HttpResponse, access_token: str, refresh_token: str) -> HttpResponse:
    """Injects HttpOnly, SameSite=Lax, Secure auth cookies into HttpResponse."""
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,  # Set True in Production HTTPS
        max_age=15 * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=False,  # Set True in Production HTTPS
        max_age=7 * 24 * 60 * 60,
    )
    return response

def clear_auth_cookies(response: HttpResponse) -> HttpResponse:
    """Deletes HttpOnly auth cookies."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
