
from django.core.exceptions import ValidationError
   
ALLOWED_FILE_TYPES = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']


def validate_file_type(file):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise ValidationError("Only pptx, docx, and xlsx file types are allowed.")