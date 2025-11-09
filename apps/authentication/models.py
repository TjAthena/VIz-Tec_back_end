from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # For Django admin
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles.filter(role=role_name).exists()
    
    def get_primary_role(self):
        """Get user's primary role (highest privilege)"""
        role_hierarchy = ['ADMIN', 'CORE', 'CLIENT', 'GUEST']
        for role in role_hierarchy:
            if self.has_role(role):
                return role
        return None
