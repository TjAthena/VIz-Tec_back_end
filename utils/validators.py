"""
Custom validators for data validation
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    """
    Validate phone number format
    """
    pattern = re.compile(r'^\+?1?\d{9,15}$')
    if not pattern.match(value.replace(' ', '').replace('-', '')):
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )


def validate_embed_url(value):
    """
    Validate embed URL format (PowerBI, Tableau, etc.)
    """
    if not value.startswith(('http://', 'https://')):
        raise ValidationError(
            _('Embed URL must start with http:// or https://'),
        )
    
    # Add more specific validation for PowerBI/Tableau URLs if needed
    valid_domains = ['app.powerbi.com', 'tableau', 'looker', 'analytics']
    if not any(domain in value.lower() for domain in valid_domains):
        raise ValidationError(
            _('URL does not appear to be a valid dashboard embed URL'),
        )


def validate_file_size(value):
    """
    Validate uploaded file size (max 5MB)
    """
    max_size = 5242880  # 5MB in bytes
    if value.size > max_size:
        raise ValidationError(
            _('File size cannot exceed 5MB'),
        )


def validate_image_file(value):
    """
    Validate image file type
    """
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if value.content_type not in allowed_types:
        raise ValidationError(
            _('Only JPEG, PNG, GIF, and WebP images are allowed'),
        )