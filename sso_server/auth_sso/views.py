import os
import jwt
from datetime import datetime
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, BlacklistToken
from .serializers import UserSerializer
from .utils.password_hash import CustomPBKDF2PasswordHasher
from .services import create_jwt_token, verify_jwt_token, generate_random_salt

@api_view(['POST'])
def logout(request):
    token = request.headers.get('Authorization')
    if not token:
        return Response({'error': 'No token provided'}, status=400)

    try:
        parts = token.split()
        decoded_token = verify_jwt_token(parts[1], settings.SECRET_KEY)
        # Blacklist the token if it's not already blacklisted
        if not BlacklistToken.objects.filter(token=token).exists():
            BlacklistToken.objects.create(
                token=parts[1],
                expires_at=datetime.fromtimestamp(decoded_token['exp'])
            )

        return Response({'status_code': status.HTTP_200_OK, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except jwt.InvalidTokenError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=username)
    hash_passwd = user.password

    # Verify Password
    verify_passwd = CustomPBKDF2PasswordHasher().verify(password=password, encoded=hash_passwd, secret_key=os.getenv("SECRET_KEY_SSO"))
    if verify_passwd:
        access_token = create_jwt_token(user, settings.SECRET_KEY)
        refresh_token = create_jwt_token(user, settings.SECRET_KEY, is_refresh=True)
        res = dict(
            status_code=status.HTTP_200_OK,
            message="Login successful",
            data=dict(
                username=user.username,
                email=user.email,
                access_token=str(access_token),
                refresh_token=str(refresh_token),
                expired=settings.ACCESS_TOKEN_LIFETIME
            )
        )
        return Response(res, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def create_user(request):
    # For create user with API
    password = request.data.get("password")
    salt = generate_random_salt()
    # Hash the password securely using Django's make_password (PBKDF2 by default)
    if password:
        hashed_password = CustomPBKDF2PasswordHasher().encode(password, salt=salt, secret_key=os.getenv("SECRET_KEY_SSO"))
        request.data["password"] = hashed_password
    else:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        res = dict(
            status_code=status.HTTP_201_CREATED,
            message="User created successfully",
            data=dict(
                username=serializer.data['username'],
                email=serializer.data['email']
            )
        )
        return Response(res, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)