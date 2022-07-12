from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)
    username = serializers.CharField(required=True, max_length=255)
    firstName = serializers.CharField(required=True, max_length=255)
    lastName = serializers.CharField(required=True, max_length=255)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)


class GetProfiledSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=255)

class GetImageSerializer(serializers.Serializer):
    path = serializers.CharField(required=True, max_length=255)
