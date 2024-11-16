from django.core.exceptions import ValidationError

def validate_file_type(value):
    allowed_extensions = ['.pptx', '.docx', '.xlsx']
    if not any(value.name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError(f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")