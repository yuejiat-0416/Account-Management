from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    deactivated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_account_admin = models.BooleanField(default=False)
    is_site_admin = models.BooleanField(default=False)

    # Make sure email is unique
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email already exists.",
    })

    def __str__(self):
        return self.username