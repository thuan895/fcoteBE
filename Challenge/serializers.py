from dataclasses import field
from Challenge.models import Challenge
from rest_framework import serializers

from Assignment.models import Assignment


class ListChallengeSerializer(serializers.Serializer):
    typeData = serializers.IntegerField(required=True,)
    searchBy = serializers.CharField(required=False, max_length=255)
    groupID = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False,)
    pageNumber = serializers.IntegerField(required=False,)


class ChallengesSerializer(serializers.Serializer):
    class Meta:
        modle = Challenge
        fields = "__all__"

class ChallengeDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True,)
