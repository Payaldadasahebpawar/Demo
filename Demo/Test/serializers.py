from django.forms import ValidationError
from rest_framework import serializers
from .models import Name, UserAccount

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['first_name', 'last_name']

class UserAccountSerializer(serializers.ModelSerializer):
    name = UserNameSerializer()

    class Meta:
        model = UserAccount
        fields = ['email', 'password','name']
        
        
    def create(self, validated_data):
        name_data = validated_data.pop('name')
        name = Name.objects.create(**name_data)
        user = UserAccount.objects.create(name=name, **validated_data)
        return user
        
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
        
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
     
    class Meta:
        model = UserAccount
        fields = ['email','password']

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        
        print(email,password)

        if email and password:
            user = UserAccount.objects.get(email=email)
           
            if user:
                if user.is_active:
                    return user
                else:
                    raise serializers.ValidationError("User is not active.")
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include both username and password.")

        
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()       