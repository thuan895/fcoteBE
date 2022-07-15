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
    type = serializers.CharField(required=False, max_length=255)
    username = serializers.CharField(required=False, max_length=255)


class GetImageSerializer(serializers.Serializer):
    path = serializers.CharField(required=True, max_length=255)


class UpdateProfileSerializer(serializers.Serializer):
    avatar = serializers.CharField(required=False, max_length=255)
    phone = serializers.CharField(required=False, max_length=255)
    birthday = serializers.CharField(required=False, max_length=255)
    gender = serializers.ImageField(required=False)
    organization = serializers.ImageField(required=False)
    city = serializers.CharField(required=False, max_length=255)
    country = serializers.CharField(required=False, max_length=255)
    first_name = serializers.CharField(required=False, max_length=255)
    last_name = serializers.CharField(required=False, max_length=255)
    email = serializers.CharField(required=False, max_length=255)


class GetRankingSerializer(serializers.Serializer):
    typeRanking = serializers.IntegerField(required=True)
    pageSize = serializers.IntegerField(required=False,)
    pageNumber = serializers.IntegerField(required=False,)
