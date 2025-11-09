from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRole(models.Model):
    """
    SECURITY: Roles MUST be in separate table to prevent privilege escalation.
    Never store roles directly on User or Profile models.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),           # Django superuser
        ('CORE', 'Core User'),        # Registered users
        ('CLIENT', 'Client'),         # Users created by Core users
        ('GUEST', 'Guest'),           # Independent guest access
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'role')
        indexes = [
            models.Index(fields=['user', 'role']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
