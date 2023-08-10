from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission


class CustomUser(AbstractUser):
    deactivated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_account_admin = models.BooleanField(default=True)
    is_site_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='user_management_users')
    user_permissions = models.ManyToManyField(Permission, related_name='user_management_users')

    # Make sure email is unique
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email already exists.",
    })

    def __str__(self):
        return self.username
    

# Description: Defines all the permissions available in the system, like 'can_add_job', 'can_edit_candidate', etc.
class Permission(models.Model):
    permission_name = models.CharField(max_length=255, unique=True)
    permission_type = models.CharField(max_length=255)
    permission_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'

    class Meta:
        indexes = [
            models.Index(fields=['permission_name']),
            models.Index(fields=['permission_type']),
        ]