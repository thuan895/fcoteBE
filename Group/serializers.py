from rest_framework import serializers


class GroupListSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(required=False,)
    pageNumber = serializers.IntegerField(required=False,)


class GroupDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True,)


class CreateGroupSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True, max_length=10000)
    image = serializers.CharField(required=False, max_length=255)


class GroupDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True,)

class JoinGroupSerializer(serializers.Serializer):
    joinCode = serializers.CharField(required=True, max_length=255)
