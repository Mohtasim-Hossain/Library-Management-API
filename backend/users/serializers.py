from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer to represent the User model."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'current_borrowed_books']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        # Create a new user with the provided data
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', User.MEMBER)  # Default role is MEMBER
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style = {'input_type' : 'password'})

    def validate(self, data):
        # Validate login credentials
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError("Incorrect username or password.")
    
    def get_tokens(self, user):
        """Generate JWT tokens for the user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
