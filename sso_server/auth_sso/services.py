import jwt
import datetime
import secrets
from django.conf import settings

def create_jwt_token(user, secret_key=None, is_refresh=False):
    # Create JWT Token

    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.now() + datetime.timedelta(days=settings.ACCESS_TOKEN_LIFETIME),
        'iat': datetime.datetime.now()
    }

    if is_refresh:
        payload['type'] = 'refresh'

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_jwt_token(token, secret_key=None):
    # Verify JWT Token

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_random_salt(length=16):
    """Generate a secure random salt."""
    return secrets.token_hex(length)
