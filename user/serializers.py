from rest_framework import serializers
from .models import CustomUser,FileUpload

class CustomUserSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('username','password','email')
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=CustomUser(username=validated_data['username'],email=validated_data['email'])
        user.is_active=False
        user.save()
        return user
    
