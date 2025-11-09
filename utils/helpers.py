"""
Helper utility functions
"""
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone


def generate_otp(length=6):
    """
    Generate a random numeric OTP
    """
    return ''.join(random.choices(string.digits, k=length))


def generate_access_code(length=8):
    """
    Generate a random alphanumeric access code
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_share_link():
    """
    Generate a unique share link identifier
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))


def get_otp_expiry(minutes=10):
    """
    Get OTP expiry datetime (default 10 minutes from now)
    """
    return timezone.now() + timedelta(minutes=minutes)


def get_default_access_expiry(days=7):
    """
    Get default access expiry datetime (default 7 days from now)
    """
    return timezone.now() + timedelta(days=days)


def is_expired(expiry_date):
    """
    Check if a date has expired
    """
    if not expiry_date:
        return False
    return timezone.now() > expiry_date


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Get user agent from request
    """
    return request.META.get('HTTP_USER_AGENT', '')