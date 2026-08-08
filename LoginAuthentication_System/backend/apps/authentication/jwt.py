from ninja.security import HttpBearer
from django.http import HttpRequest
from apps.users.models import User
from apps.authentication.models import BlacklistedToken
from core.security.tokens import decode_access_token
from core.exceptions import AuthenticationError

class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        if not token:
            return None
        
        payload = decode_access_token(token)
        jti = payload.get("jti")
        
        # Check if JTI is blacklisted
        if BlacklistedToken.objects.filter(jti=jti).exists():
            raise AuthenticationError("Token has been revoked/blacklisted.")
        
        user_id = payload.get("sub")
        try:
            user = User.objects.get(id=user_id, is_active=True)
            request.user = user
            request.auth_payload = payload
            return user
        except User.DoesNotExist:
            raise AuthenticationError("User account no longer active or exists.")
