from rest_framework import serializers
from .models import User, UserManager

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'upi_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # validating password and confirm password while registration
    def validate(self, attrs):
        password= attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field =["id", "email","name"]