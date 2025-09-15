# utils/jwt_utils.py
import jwt
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.contrib.auth import get_user_model
from utils.jwt_utils import get_user_from_token, get_token_payload, decode_jwt_token
from utils.response_utils import error_response

User = get_user_model()

def get_user_from_token(request):
    """
    Extract user from JWT token in request
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    try:
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except (IndexError, InvalidToken, TokenError, User.DoesNotExist):
        return None

def decode_jwt_token(token):
    """
    Decode JWT token and return payload
    """
    try:
        # Untuk Simple JWT, kita bisa menggunakan AccessToken
        access_token = AccessToken(token)
        return {
            'user_id': access_token['user_id'],
            'username': access_token.get('username', ''),
            'email': access_token.get('email', ''),
            'is_superuser': access_token.get('is_superuser', False),
            'exp': access_token['exp'],
            'iat': access_token['iat']
        }
    except (InvalidToken, TokenError) as e:
        raise ValueError(f"Invalid token: {str(e)}")

def get_token_payload(request):
    """
    Get JWT token payload from request
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    try:
        token = auth_header.split(' ')[1]
        return decode_jwt_token(token)
    except (IndexError, ValueError):
        return None