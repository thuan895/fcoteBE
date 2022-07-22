from rest_framework import serializers


class GroupListSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(required=False)
    pageNumber = serializers.IntegerField(required=False)
    searchBy = serializers.CharField(
        required=False, max_length=255, allow_blank=True)


class GroupDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class CreateGroupSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True, max_length=255, allow_blank=True)
    description = serializers.CharField(
        required=True, max_length=10000, allow_blank=True)
    image = serializers.CharField(
        required=False, max_length=255, allow_blank=True)


class GroupDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class JoinGroupSerializer(serializers.Serializer):
    joinCode = serializers.CharField(
        required=True, max_length=255, allow_blank=True)


class outMemberSerializer(serializers.Serializer):
    groupId = serializers.IntegerField(required=True)
