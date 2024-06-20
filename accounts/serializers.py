from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "referral_code")
        extra_kwargs = {
            "password": {"required": True, "write_only": True, "style": {"input_type": "password"}},
            "email": {"required": True},
            "referral_code": {"required": False}
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("email is duplicate")
        return value

    def validate_referral_code(self, value):
        if User.objects.filter(user_referral_code=value).exists():
            return value
        raise serializers.ValidationError("referral_code wrong")


class OtpCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4)

    class Meta:
        model = User
        fields = ["email", "code"]
        # extra_kwargs = {
        #     "phone_number": {"required": True, "min_length": 11, "max_length": 13},
        # }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("email is duplicate")
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"required": True, "write_only": True, "style": {"input_type": "password"}},
            # "phone_number": {"max_length": 11},
        }


class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)
