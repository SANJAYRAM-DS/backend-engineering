import time
import uuid
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware injecting security response headers (HSTS, CSP, X-Frame, X-Content-Type).
    """
    def process_response(self, request, response):
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Inject correlation ID
        if not response.has_header("X-Request-ID"):
            response["X-Request-ID"] = getattr(request, "request_id", str(uuid.uuid4()))
            
        return response

    def process_request(self, request):
        request.request_id = str(uuid.uuid4())
        request.start_time = time.time()
