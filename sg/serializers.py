from rest_framework import serializers
from sg.models import User
from rest_framework import status
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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
        # status=status.HTTP_201_CREATED
        
   
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']     

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
        
class ChangeUserPasswordSerializer(serializers.Serializer):
     password= serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
     password2= serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
     class Meta:
         fields=['password','password2']
         
     def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError({'password':'Password and Confirm Password do not match'})
        user.set_password(password)
        user.save()
        return attrs     
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']    
    
    
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():

            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:8000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link',link)
            #Send Email
            
            return attrs
            
            
        else:
            raise serializers.ValidationError("You are not a Registered User")
        
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields=['password','password2']
        
    def validate(self, attrs):
      try:
          password=attrs.get('password')
          password2=attrs.get('password2')
          uid=self.context.get('uid')
          token=self.context.get('token')
          if password != password2:
            raise serializers.ValidationError({'password':'Password and Confirm Password do not match'})
          id = urlsafe_base64_decode(uid)
          user = User.objects.get(id=id)
          if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Token is not valid or expired')
          user.set_password(password)
          user.save()
          return attrs  
      except DjangoUnicodeDecodeError as identifier:
          PasswordResetTokenGenerator().check_token(user, token)
          raise serializers.ValidationError('Token is not valid or expired')
        
    
           