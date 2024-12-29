import unittest
import django
from django.contrib.auth.hashers import make_password
from unittest.mock import MagicMock, patch
import os
from django.conf import settings
from django.db import connection

# Ensure the settings module is set for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')
django.setup()

from auth_sso.models import User


class TestUserService(unittest.TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='grpc_app_user';")  # Reset auto-increment
            cursor.execute("DELETE FROM grpc_app_user;")  # Delete all data

    @patch('django.contrib.auth.models.User.objects.create')  # Mock the User.objects.create method
    def test_insert_user(self, mock_create):
        # Simulating the creation of a user in the database
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "testuser@example.com"
        mock_user.password = "testuser123!"
        mock_create.return_value = mock_user

        hashed_password = make_password(mock_user.password)
        # Simulate user creation
        new_user = User.objects.create(username="testuser", email="testuser@example.com", password=hashed_password)
        # Assertions to verify the behavior
        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.email, "testuser@example.com")
        self.assertEqual(new_user.password, hashed_password)
        self.assertEqual(new_user.id, 1)


if __name__ == '__main__':
    unittest.main()
