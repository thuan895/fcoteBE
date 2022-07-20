
from rest_framework import serializers


class SourceCodeSerializer(serializers.Serializer):
    assignmentId = serializers.IntegerField(required=True,)
    challengeId = serializers.IntegerField(required=True,)
    groupId = serializers.IntegerField(required=True,)
    sourceCode = serializers.CharField(required=True, max_length=10000)
    language = serializers.CharField(required=True, max_length=255)
