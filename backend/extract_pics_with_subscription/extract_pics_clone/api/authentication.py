from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class for API key authentication.
    Clients should pass the API key in the X-API-Key header.
    """
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None  # No API key provided, let other auth methods handle it
        
        user = APIKey.validate_key(api_key)
        
        if user is None:
            raise AuthenticationFailed('Invalid or inactive API key')
        
        return (user, None)  # Return user and auth token (None for API key auth)

