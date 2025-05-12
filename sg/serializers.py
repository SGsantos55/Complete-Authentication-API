from rest_framework import serializers
from sg.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'df']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validate that both passwords match
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'Password and Confirm Password do not match'})
        return attrs

    # Create the user using your custom manager
    def create(self, validated_data):
        # password = validated_data.pop('password')
        # validated_data.pop('password2')
        return User.objects.create_user( **validated_data)
