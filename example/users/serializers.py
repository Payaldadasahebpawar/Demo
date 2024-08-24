from django.forms import ValidationError
from rest_framework import serializers
from .models import UserProfile, UserAccount

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class UserAccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
     
    class Meta:
        model = UserAccount
        fields = ['email', 'password']
              
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if any(char.isupper() for char in value):
            raise ValidationError("Email address should not contain uppercase letters.")
    
        return value  
    
    def validate_password(self, value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("The password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one number.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?' for char in value):
            raise serializers.ValidationError("The password must contain at least one special symbol.")

        return value    
