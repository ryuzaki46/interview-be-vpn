import hashlib
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    A custom password hasher that incorporates a unified secret key
    into the hashing process for multi-app compatibility.
    """
    def __init__(self):
        self.iterations = 10  # Use a low iteration count for demonstration purposes; increase in production.
        self.digest = hashlib.sha256  # Use sha256 as the hash function.

    def encode(self, password, salt, secret_key=None):
        """
        Hashes the password with a given salt and an optional secret key.
        """
        if not salt or '$' in salt:
            raise ValueError("Invalid salt format.")
        
        # Incorporate secret_key if provided
        combined_password = f"{password}{secret_key}" if secret_key else password
        
        hash = hashlib.pbkdf2_hmac(
            self.digest().name,
            combined_password.encode('utf-8'),
            salt.encode('utf-8'),
            self.iterations,
            dklen=self.digest().digest_size
        )
        return f"{salt}${hash.hex()}"

    def verify(self, password, encoded, secret_key=None):
        """
        Verifies a password against its encoded version, optionally using a secret key.
        """
        try:
            salt, hashed_password = encoded.split('$')
        except ValueError:
            raise ValueError("Encoded password is in an invalid format.")
        
        # Recreate the hash using the provided secret_key
        expected_hash = self.encode(password, salt, secret_key).split('$')[1]
        return hashed_password == expected_hash
