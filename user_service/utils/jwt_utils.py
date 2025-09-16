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
    Decode JWT token and return payload with improved error handling
    """
    try:
        # Method 1: Using SimpleJWT's AccessToken (recommended)
        access_token = AccessToken(token)
        
        # Get the user to verify additional details if needed
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        
        return {
            'user_id': user_id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'exp': access_token['exp'],
            'iat': access_token['iat']
        }
        
    except (InvalidToken, TokenError) as e:
        # If SimpleJWT fails, try with standard JWT library as fallback
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,  # Ensure this is the same key used for signing
                algorithms=['HS256'],
                options={"verify_exp": True}
            )
            
            user_id = payload.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                return {
                    'user_id': user_id,
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser,
                    'exp': payload.get('exp'),
                    'iat': payload.get('iat')
                }
                
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except User.DoesNotExist:
            raise ValueError("User does not exist")
        except Exception as e:
            raise ValueError(f"Token verification failed: {str(e)}")
            
    except User.DoesNotExist:
        raise ValueError("User does not exist")
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

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