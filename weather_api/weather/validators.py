from functools import wraps

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


def validate_latitude(value):
    if value < -90 or value > 90:
        raise ValidationError("Latitude must be in the range of -90 to 90 degrees.")


def validate_longitude(value):
    if value < -180 or value > 180:
        raise ValidationError("Longitude must be in the range of -180 to 180 degrees.")


def validate_coordinates(view_func):
    
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        errors = {}
        exception = False
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        try:
            validate_latitude(float(latitude))
        except ValidationError as e:
            exception = True
            errors['latitude'] = list(e)
        try:
            validate_longitude(float(longitude))
        except ValidationError as e:
            exception = True
            errors['longitude'] = list(e)
        if exception:
            return Response({'error': {'location': errors}}, status=status.HTTP_400_BAD_REQUEST)

        return view_func(*args, **kwargs)
    return _wrapped_view
