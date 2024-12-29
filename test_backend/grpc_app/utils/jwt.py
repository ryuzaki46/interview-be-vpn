# apps/authentication/middleware.py
import jwt
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from grpc_app.models import BlacklistToken

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return JsonResponse({'error': 'Authorization token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is blacklisted
            if BlacklistToken.objects.filter(token=token).exists():
                return JsonResponse({'error': 'Token is blacklisted'}, status=status.HTTP_401_UNAUTHORIZED)

            request.user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response
