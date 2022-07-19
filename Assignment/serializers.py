from rest_framework import serializers

from Assignment.models import Assignment


class ListAssignmentSerializer(serializers.Serializer):
    filterByStatus = serializers.CharField(required=False, max_length=255)
    filterByDifficult = serializers.CharField(required=False, max_length=255)
    filterByCurrentAccount = serializers.BooleanField(required=False)
    searchBy = serializers.CharField(required=False, max_length=255)
    pageSize = serializers.IntegerField(required=False,)
    pageNumber = serializers.IntegerField(required=False,)


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"


class AssignmentDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True,)


class CreateAssignmentSettingSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True, max_length=10000)
    difficulty = serializers.IntegerField(required=False,)


class CreateAssignmentLanguageSerializer(serializers.Serializer):
    language = serializers.CharField(required=True, max_length=255)
    timeLimit = serializers.IntegerField(required=False,)


class CreateAssignmentParammeterDetailSerializer(serializers.Serializer):
    order = serializers.IntegerField(required=True,)
    name = serializers.CharField(required=True, max_length=255)
    type = serializers.IntegerField(required=True,)
    description = serializers.CharField(required=True, max_length=255)


class CreateAssignmentParammeterSerializer(serializers.Serializer):
    input = CreateAssignmentParammeterDetailSerializer(
        required=True, many=True)
    output = CreateAssignmentParammeterDetailSerializer(required=True,)


class CreateTestCaseElementDetailSerializer(serializers.Serializer):
    order = serializers.IntegerField(required=True,)
    name = serializers.CharField(required=False, max_length=255)
    value = serializers.CharField(required=True, max_length=255)
    type = serializers.IntegerField(required=True,)


class CreateTestCaseElementSerializer(serializers.Serializer):
    isPrivate = serializers.BooleanField(required=True,)
    order = serializers.IntegerField(required=True,)
    input = CreateTestCaseElementDetailSerializer(required=True, many=True)
    output = CreateTestCaseElementDetailSerializer(required=True,)


class CreateAssignmentSerializer(serializers.Serializer):
    setting = CreateAssignmentSettingSerializer(required=True,)
    language = CreateAssignmentLanguageSerializer(required=False, many=True)
    inputOutput = CreateAssignmentParammeterSerializer(required=True,)
    authorSolution = serializers.CharField(required=False, max_length=10000)
    testCase = CreateTestCaseElementSerializer(required=True, many=True)


class AssignmentDeleteSerializer(serializers.Serializer):
    assignmentId = serializers.IntegerField(required=True,)
