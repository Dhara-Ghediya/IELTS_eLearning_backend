import os
from django.core.exceptions import ValidationError

# validation for Audio file's extension and size
ALLOWED_EXTENSIONS = ['mp3', 'wav']
MAX_SIZE_MB = 10 * 1024 * 1024  # 10 MB in bytes

def max_file_size_validator(value):
    if value.size > MAX_SIZE_MB:
        raise ValidationError(f"Audio file size must be less than {MAX_SIZE_MB / (1024 * 1024)} MB.")

# validation for Image file's extension and size
ALLOWED_EXTENSIONS_FOR_IMAGE = ['png', 'jpg', 'jpeg', 'webp']
MAX_SIZE_MB_FOR_IMAGE = 0.05 * 1024 * 1024  # 10 MB in bytes

def max_file_size_validator_for_image(value):
    if value.size > MAX_SIZE_MB_FOR_IMAGE:          
        return False
    else:
        return True
