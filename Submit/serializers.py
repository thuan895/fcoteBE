
from rest_framework import serializers


class SourceCodeSerializer(serializers.Serializer):
    assignmentId = serializers.IntegerField(required=True)
    challengeId = serializers.IntegerField(required=True)
    sourceCode = serializers.CharField(
        required=True, max_length=10000, allow_blank=True)
    language = serializers.IntegerField(required=True)
