import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ALLOWED_EXTENSIONS = ['mp3', 'wav']
MAX_SIZE_MB = 10 * 1024 * 1024  # 10 MB in bytes

def max_file_size_validator(value):
    if value.size > MAX_SIZE_MB:
        raise ValidationError(f"Audio file size must be less than {MAX_SIZE_MB / (1024 * 1024)} MB.")
