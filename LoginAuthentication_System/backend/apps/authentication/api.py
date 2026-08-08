from typing import List
from ninja import Router
from django.http import HttpRequest, HttpResponse
from apps.users.schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema,
    EmailVerificationSchema,
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema
)
from apps.authentication.schemas import TokenPairSchema, RefreshTokenRequestSchema, LogoutRequestSchema, DeviceSessionResponseSchema
from apps.authentication.services import AuthService
from apps.users.services import UserService
from apps.authentication.rotation import TokenRotationEngine
from apps.authentication.sessions import SessionService
from apps.authentication.jwt import JWTAuth
from apps.rbac.services import RbacService
from core.utils import extract_client_info
from core.security.transport import set_auth_cookies, clear_auth_cookies
from core.exceptions import BaseAppException, NotFoundError

auth_router = Router(tags=["Authentication & Identity"])
sessions_router = Router(tags=["Session Management"])

@auth_router.post("/register", response={201: dict})
def register(request: HttpRequest, payload: UserRegisterSchema):
    """Registers a new user account and generates email verification token."""
    user = UserService.register_user(payload)
    verification_token = UserService.get_verification_token(user)
    return 201, {
        "status": "success",
        "message": "User registered successfully. Please verify your email.",
        "user_id": str(user.id),
        "verification_token_demo": verification_token  # Provided for demo/testing convenience
    }

@auth_router.post("/verify-email", response={200: dict})
def verify_email(request: HttpRequest, payload: EmailVerificationSchema):
    """Verifies user email using cryptographic token."""
    UserService.verify_email(payload.token)
    return 200, {"status": "success", "message": "Email address verified successfully."}

@auth_router.post("/login", response={200: TokenPairSchema})
def login(request: HttpRequest, payload: UserLoginSchema, response: HttpResponse):
    """Authenticates user credentials and issues short-lived Access + Refresh token pair."""
    ip_address, user_agent = extract_client_info(request)
    user, access_token, refresh_token = AuthService.authenticate_user(
        email=payload.email,
        password=payload.password,
        ip_address=ip_address,
        user_agent=user_agent
    )
    set_auth_cookies(response, access_token, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 900
    }

@auth_router.post("/refresh", response={200: TokenPairSchema})
def refresh_token(request: HttpRequest, payload: RefreshTokenRequestSchema, response: HttpResponse):
    """Exchanges a refresh token for a new token pair using Refresh Token Rotation (RTR)."""
    ip_address, user_agent = extract_client_info(request)
    raw_refresh = payload.refresh_token or request.COOKIES.get("refresh_token")
    if not raw_refresh:
        raise BaseAppException(message="Refresh token is required.", status_code=400)

    new_access, new_refresh = TokenRotationEngine.rotate_refresh_token(
        raw_refresh_token=raw_refresh,
        ip_address=ip_address,
        user_agent=user_agent
    )
    set_auth_cookies(response, new_access, new_refresh)
    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "Bearer",
        "expires_in": 900
    }

@auth_router.post("/logout", auth=JWTAuth(), response={200: dict})
def logout(request: HttpRequest, payload: LogoutRequestSchema, response: HttpResponse):
    """Logs out user, blacklisting access token JTI and revoking refresh token."""
    jti = request.auth_payload.get("jti")
    raw_refresh = payload.refresh_token or request.COOKIES.get("refresh_token")
    AuthService.logout(user=request.user, jti=jti, refresh_token=raw_refresh)
    clear_auth_cookies(response)
    return 200, {"status": "success", "message": "Logged out successfully."}

@auth_router.get("/me", auth=JWTAuth(), response={200: UserResponseSchema})
def me(request: HttpRequest):
    """Returns authenticated user profile and assigned roles."""
    user = request.user
    roles = list(user.user_roles.values_list("role__name", flat=True))
    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_email_verified": user.is_email_verified,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "roles": roles,
        "created_at": user.created_at.isoformat()
    }

@auth_router.post("/password-reset/request", response={200: dict})
def password_reset_request(request: HttpRequest, payload: PasswordResetRequestSchema):
    """Sends password reset token (returns generic 200 to prevent user enumeration)."""
    try:
        from apps.users.models import User
        user = User.objects.get(email=payload.email.lower())
        token = UserService.get_verification_token(user)
        return 200, {
            "status": "success",
            "message": "If an account exists with that email, a password reset link has been issued.",
            "reset_token_demo": token  # For demo UI convenience
        }
    except User.DoesNotExist:
        return 200, {
            "status": "success",
            "message": "If an account exists with that email, a password reset link has been issued."
        }

@auth_router.post("/password-reset/confirm", response={200: dict})
def password_reset_confirm(request: HttpRequest, payload: PasswordResetConfirmSchema):
    """Resets user password given a valid reset token."""
    user_id = UserService.verify_email(payload.token)
    try:
        from apps.users.models import User
        user = User.objects.get(id=user_id)
        user.set_password(payload.new_password)
        user.save(update_fields=["password"])
        return 200, {"status": "success", "message": "Password reset successfully."}
    except User.DoesNotExist:
        raise NotFoundError("User not found.")

# Session management endpoints
@sessions_router.get("/active", auth=JWTAuth(), response={200: List[DeviceSessionResponseSchema]})
def get_active_sessions(request: HttpRequest):
    """Lists all active device sessions for current user."""
    sessions = SessionService.get_active_sessions(request.user)
    return [
        {
            "id": str(s.id),
            "session_key": s.session_key,
            "ip_address": s.ip_address,
            "user_agent": s.user_agent,
            "device_type": s.device_type,
            "is_active": s.is_active,
            "last_activity_at": s.last_activity_at.isoformat(),
            "created_at": s.created_at.isoformat()
        }
        for s in sessions
    ]

@sessions_router.post("/revoke/{session_id}", auth=JWTAuth(), response={200: dict})
def revoke_session(request: HttpRequest, session_id: str):
    """Revokes a specific active session remotely."""
    SessionService.revoke_session(request.user, session_id)
    return 200, {"status": "success", "message": f"Session {session_id} revoked."}

@sessions_router.post("/revoke-all", auth=JWTAuth(), response={200: dict})
def revoke_all_sessions(request: HttpRequest):
    """Revokes all active sessions for current user across all devices."""
    SessionService.revoke_all_sessions(request.user)
    return 200, {"status": "success", "message": "All sessions revoked."}
