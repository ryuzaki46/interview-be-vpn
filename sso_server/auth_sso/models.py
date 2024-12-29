from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'grpc_app_user'

    def __str__(self):
        return self.username

class BlacklistToken(models.Model):
    token = models.CharField(max_length=1024, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Blacklisted token {self.token[:20]}..."