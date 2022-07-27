from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, max_length=255, allow_blank=True)
    password = serializers.CharField(
        required=True, max_length=255, allow_blank=True)
    username = serializers.CharField(
        required=True, max_length=255, allow_blank=True)
    firstName = serializers.CharField(
        required=True, max_length=255, allow_blank=True)
    lastName = serializers.CharField(
        required=True, max_length=255, allow_blank=True)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, max_length=255, allow_blank=True)
    password = serializers.CharField(
        required=True, max_length=255, allow_blank=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, max_length=255, allow_blank=True)


class GetProfiledSerializer(serializers.Serializer):
    typeData = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    username = serializers.CharField(
        required=False, max_length=255, allow_blank=True)


class GetImageSerializer(serializers.Serializer):
    path = serializers.CharField(
        required=True, max_length=255, allow_blank=True)


class UpdateProfileSerializer(serializers.Serializer):
    avatar = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    phone = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    birthday = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    gender = serializers.ImageField(required=False)
    organization = serializers.ImageField(required=False)
    city = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    country = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    firstName = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    lastName = serializers.CharField(
        required=False, max_length=255, allow_blank=True)


class GetRankingSerializer(serializers.Serializer):
    typeRanking = serializers.IntegerField(required=True)
    pageSize = serializers.IntegerField(required=False,)
    pageNumber = serializers.IntegerField(required=False,)
