from dataclasses import field
from Challenge.models import Challenge
from rest_framework import serializers

from Assignment.models import Assignment


class ListChallengeSerializer(serializers.Serializer):
    typeData = serializers.IntegerField(required=True)
    searchBy = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    groupID = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    pageNumber = serializers.IntegerField(required=False)
    username = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    status = serializers.IntegerField(required=False)


class ChallengesSerializer(serializers.Serializer):
    class Meta:
        modle = Challenge
        fields = "__all__"


class ChallengeDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class ChallengeElementSerializer(serializers.Serializer):
    assignmentId = serializers.IntegerField(required=True)


class ChallengeCreateSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True, max_length=255, allow_blank=True)
    description = serializers.CharField(
        required=True, max_length=10000, allow_blank=True)
    image = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    groupId = serializers.IntegerField(required=True)
    startAt = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    endAt = serializers.CharField(
        required=False, max_length=255, allow_blank=True)
    element = ChallengeElementSerializer(required=False, many=True)


class ChallengeDeleteSerializer(serializers.Serializer):
    challengeId = serializers.IntegerField(required=True)
