from rest_framework import serializers
from .models import CustomUser,FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('id', 'file', 'uploaded_by', 'created_at', 'updated_at')