
from rest_framework import serializers


class SourceCodeSerializer(serializers.Serializer):
    assignment = serializers.IntegerField(required=True,)
    challenge = serializers.IntegerField(required=True,)
    group = serializers.IntegerField(required=True,)
    sourceCode = serializers.CharField(required=True, max_length=10000)
