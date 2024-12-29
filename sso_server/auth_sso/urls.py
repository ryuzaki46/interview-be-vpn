from django.urls import path
from .views import create_user, login, logout

urlpatterns = [
    path('register', create_user, name='create_user'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]