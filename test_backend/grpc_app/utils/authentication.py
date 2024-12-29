import jwt
import os
from datetime import datetime
from django.conf import settings
from rest_framework import exceptions
from grpc_app.models import User, BlacklistToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise exceptions.AuthenticationFailed('Authorization header is required')

        # Extract token from Bearer authorization header
        token = token.split(' ')[1] if token.startswith('Bearer ') else token

        try:
            # Check if the token is blacklisted
            if BlacklistToken.objects.filter(token=token).exists():
                raise exceptions.AuthenticationFailed('This token is blacklisted')

            # Decode the JWT token
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY_SSO"), algorithms=['HS256'])

            # Check if the 'exp' field exists in the decoded token
            if 'exp' not in decoded_token:
                raise exceptions.AuthenticationFailed('Token does not have an expiration field (exp)')

            # Check if token has expired
            exp = decoded_token['exp']
            if datetime.fromtimestamp(exp) < datetime.now():
                raise exceptions.AuthenticationFailed('Token has expired')

            # Return the user associated with the token
            user_id = decoded_token.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Token does not have user_id field')

            # Assuming you have a User model or similar to fetch the user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
            
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
        