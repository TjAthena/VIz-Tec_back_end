"""
Custom exception handler for consistent API error responses
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If response is None, it means the exception is not handled by DRF
    if response is None:
        return Response(
            {
                'error': 'server_error',
                'message': 'An unexpected error occurred. Please try again later.',
                'details': {}
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Customize the response format
    custom_response_data = {
        'error': get_error_code(exc),
        'message': get_error_message(response.data),
        'details': response.data if isinstance(response.data, dict) else {'detail': response.data}
    }

    response.data = custom_response_data
    return response


def get_error_code(exc):
    """
    Get a consistent error code based on exception type
    """
    error_codes = {
        'ValidationError': 'validation_error',
        'AuthenticationFailed': 'authentication_failed',
        'NotAuthenticated': 'not_authenticated',
        'PermissionDenied': 'permission_denied',
        'NotFound': 'not_found',
        'MethodNotAllowed': 'method_not_allowed',
        'Throttled': 'rate_limit_exceeded',
    }
    
    exception_name = exc.__class__.__name__
    return error_codes.get(exception_name, 'error')


def get_error_message(data):
    """
    Extract a human-readable error message from response data
    """
    if isinstance(data, dict):
        # If there's a 'detail' key, use that
        if 'detail' in data:
            return str(data['detail'])
        
        # If there are field errors, create a message
        if any(isinstance(v, list) for v in data.values()):
            field_errors = []
            for field, errors in data.items():
                if isinstance(errors, list):
                    field_errors.append(f"{field}: {', '.join(map(str, errors))}")
            return '; '.join(field_errors)
        
        # Otherwise, return the first value
        return str(next(iter(data.values())))
    
    return str(data)