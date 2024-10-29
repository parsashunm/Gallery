from rest_framework import serializers
from django.core.exceptions import ValidationError
#
from .models import User, UserProfile


#


class CreateAccountSerializer(serializers.ModelSerializer):

    pass2 = serializers.CharField(max_length=128, label='Confirm Password', write_only=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'pass2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['pass2']:
            raise serializers.ValidationError('passwords must match')
        return data

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError('phone number must be 11 characters')
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except ValueError as e:
            raise serializers.ValidationError({'error': e})
        except Exception as e:
            raise serializers.ValidationError({'error': e})


class ConfirmOtpCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']
