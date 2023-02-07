from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email is None:
            raise serializers.ValidationError("Email can not be left empty")
        
        if password is None:
            raise serializers.ValidationError("Password can not be left empty")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with specified email already exists")
        
        return attrs
    