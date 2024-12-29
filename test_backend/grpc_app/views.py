from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .utils.authentication import JWTAuthentication
from django.http import HttpResponse


@api_view(['GET'])
def default_page(request):
    # For default page 
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Congratulations!</title>
        <style>
            html { color-scheme: light; }
            body { margin: 2em auto; max-width: 800px; line-height: 1.6; font: 18px sans-serif; color: #333; padding: 0 10px; }
            h1 { color: #009900; }
        </style>
    </head>
    <body>
        <h1>It worked!</h1>
        <p>Congratulations on your first Django-powered page.</p>
        <p>You’ve successfully installed Django. Now start building your application!</p>
        <p><a href="https://docs.djangoproject.com/">Django documentation</a></p>
    </body>
    </html>
    """)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # Set JWT Authentication
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def testing(request):
    return Response({'status_code': status.HTTP_200_OK, 'message': 'You are authenticated!'}, status=status.HTTP_200_OK)
