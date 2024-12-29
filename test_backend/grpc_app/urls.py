from django.urls import path
from .views import testing

urlpatterns = [
    path('test', testing, name='test')
]