
import json
from django.http import JsonResponse
from Assignment.serializers import *
from utils.api.api import paginate_data, validate_account
from utils.api.http_status import *
from utils.response.assignment import *
from utils.response.common import *
from .models import *
from rest_framework.decorators import api_view
from django.db.models import Q


@api_view(['GET'])
def getAssignmentTag(request):
    account = validate_account(request)
    if (account == None):
        return JsonResponse(INVALID_TOKEN, status=HTTP_401)
    if (account.is_active == False):
        return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
    try:
        assignmentTags = AssignmentTag.objects.filter(
            is_active=True).order_by("-id")
        responseData = {}
        listData = []
        for tag in assignmentTags:
            tagData = {"id": tag.id, "title": tag.title}
            listData.append(tagData)
        responseData["assignmentTags"] = listData
        return JsonResponse(responseData, status=HTTP_200)
    except Exception as e:
        return JsonResponse(FAILURE_GET_ASSIGNMENT_TAGS, status=HTTP_400)


@api_view(['GET'])
def getLanguage(request):
    account = validate_account(request)
    if (account == None):
        return JsonResponse(INVALID_TOKEN, status=HTTP_401)
    if (account.is_active == False):
        return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
    try:
        languages = Language.objects.filter(is_active=True).order_by("-id")
        responseData = {}
        listData = []
        for language in languages:
            languageData = {"id": language.id, "title": language.title}
            listData.append(languageData)
        responseData["languages"] = listData
        return JsonResponse(responseData, status=HTTP_200)
    except Exception as e:
        return JsonResponse(FAILURE_GET_LANGUAGES, status=HTTP_400)


@api_view(['POST'])
def getListAssignment(request):
    requestData = ListAssignmentSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            assignments = Assignment.objects.filter(is_active=True)
            if "filterByCreatedByUserID" in data:
                if data["filterByCreatedByUserID"] == str(account.id):
                    assignments = assignments.filter(created_by=account)
                else:
                    author = Account.objects.filter(
                        id=data["filterByCreatedByUserID"])
                    if author.exists():
                        assignments = assignments.filter(
                            created_by=author[0], quality_assurance=True)
                    else:
                        return JsonResponse(NOT_FOUND_USER_FILTER, status=HTTP_400)
            else:
                assignments = assignments.filter(quality_assurance=True)

            if "filterByDifficult" in data:
                if data["filterByDifficult"] == Difficulty.Easy:
                    assignments = assignments.filter(difficulty=1)
                if data["filterByDifficult"] == Difficulty.Mid:
                    assignments = assignments.filter(difficulty=2)
                if data["filterByDifficult"] == Difficulty.High:
                    assignments = assignments.filter(difficulty=3)
            if "searchBy" in data:
                keyword = data["searchBy"]
                assignments = assignments.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword))
            if ("pageSize" in data) and ("pageNumber" in data):
                assignments = paginate_data(
                    assignments, AssignmentSerializer, data["pageSize"], data["pageNumber"])
            responseData = {}
            listData = []
            for assignment in assignments:
                if ("pageSize" in data) and ("pageNumber" in data):
                    assignmentData = {
                        "id": assignment["id"],
                        "title": assignment["title"],
                        "image": assignment["image"],
                        "difficulty": assignment["difficulty"],
                        "score": assignment["score"],
                        "assignment_tag": assignment["assignment_tag"],
                        "total_participant": assignment["total_participant"],
                        "created_by": Account.objects.get(id=assignment["created_by"]).username,
                        "created_at": assignment["created_at"]
                    }
                else:
                    assignmentData = {
                        "id": assignment.id,
                        "title": assignment.title,
                        "image": assignment.image,
                        "difficulty": assignment.difficulty,
                        "score": assignment.score,
                        "assignment_tag": assignment.assignment_tag.id,
                        "total_participant": assignment.total_participant,
                        "created_by": assignment.created_by.username,
                        "created_at": assignment.date()
                    }
                listData.append(assignmentData)
            responseData["assignments"] = listData
            responseData["currentSize"] = len(assignments)
            return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE_GET_ASSIGNMENT, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def getAssignmentDetail(request):
    requestData = AssignmentDetailSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            assignment = Assignment.objects.filter(
                id=data["id"], is_active=True)
            if assignment.exists():
                responseData = {}
                assignmentData = {
                    "id": assignment[0].id,
                    "title": assignment[0].title,
                    "description": assignment[0].description,
                    "sample": assignment[0].sample,
                    # "image": assignment[0].image,
                    "difficulty": assignment[0].difficulty,
                    "total_test_case": assignment[0].total_test_case,
                    "score": assignment[0].score,
                    # "assignment_tag": assignment[0].assignment_tag.id,
                    "character_limit": assignment[0].character_limit,
                    "total_participant": assignment[0].total_participant,
                    "created_by": assignment[0].created_by.username,
                }
                responseData["AssignmentDetail"] = assignmentData
                assignmentLanguages = AssignmentLanguage.objects.filter(
                    assignment=assignment[0])
                assignmentLanguagesResponse = []
                for asmlg in assignmentLanguages:
                    asmlgResponse = {"id": asmlg.id,
                                     "language": asmlg.language.title,
                                     "time_limit": asmlg.time_limit}
                    assignmentLanguagesResponse.append(asmlgResponse)
                responseData["AssignmentLanguages"] = assignmentLanguagesResponse
                parammeters = Parammeter.objects.filter(
                    assignment=assignment[0])
                parammetersResponse = []
                for prm in parammeters:
                    prmResponse = {"id": prm.id,
                                   "assignment": prm.assignment.id,
                                   "order": prm.order,
                                   "type": prm.type,
                                   "name": prm.name,
                                   "data_type": prm.data_type,
                                   "description": prm.description}
                    parammetersResponse.append(prmResponse)
                responseData["Parammeters"] = parammetersResponse
                testCases = TestCase.objects.filter(assignment=assignment[0])
                testCasesResponse = []
                for testCase in testCases:
                    if testCase.is_private and testCase.assignment.created_by != account:
                        testCase = {"id": testCase.id,
                                    "assignment": testCase.assignment.id,
                                    "order": testCase.order,
                                    "is_private": testCase.is_private}
                        testCasesResponse.append(testCase)
                    else:
                        testCaseElements = TestCaseElement.objects.filter(
                            test_case=testCase)
                        testCaseElmList = []
                        for elm in testCaseElements:
                            elmData = {"id": elm.id,
                                       "test_case": elm.test_case.id,
                                       "order": elm.order,
                                       "type": elm.type,
                                       "data_type": elm.data_type,
                                       "value": elm.value}
                            testCaseElmList.append(elmData)
                        testCase = {"id": testCase.id,
                                    "assignment": testCase.assignment.id,
                                    "order": testCase.order,
                                    "element": testCaseElmList,
                                    "is_private": testCase.is_private}
                        testCasesResponse.append(testCase)
                responseData["TestCases"] = testCasesResponse
                return JsonResponse(responseData, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_ASSIGNMENT, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def addAssignment(request):
    requestData = CreateAssignmentSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            if (request.method == 'POST'):
                ##########################
                obj = Assignment()
                obj.title = data["setting"]["name"]
                obj.description = data["setting"]["description"]
                obj.sample = data["authorSolution"]
                difficulty = data["setting"]["difficulty"]
                obj.difficulty = difficulty
                obj.total_test_case = len(data["testCase"])
                if (difficulty == Difficulty.Easy):
                    obj.score = 50
                elif (difficulty == Difficulty.Mid):
                    obj.score = 70
                elif (difficulty == Difficulty.High):
                    obj.score = 100
                else:
                    obj.score = 0
                obj.created_by = account
                obj.save()
                assignment = obj
                ##########################
                for lgg in data["language"]:
                    language = Language.objects.filter(title=lgg["language"])
                    if language.exists():
                        obj = AssignmentLanguage()
                        obj.assignment = assignment
                        obj.language = language[0]
                        obj.time_limit = lgg["time_limit"]
                obj.save()
                ##########################
                for input in data["inputOutput"]["input"]:
                    obj = Parammeter()
                    obj.assignment = assignment
                    obj.order = input["order"]
                    obj.type = InOutType.input
                    obj.name = input["name"]
                    obj.data_type = input["type"]
                    obj.description = input["description"]
                    obj.save()

                output = data["inputOutput"]["output"]
                obj = Parammeter()
                obj.assignment = assignment
                obj.order = output["order"]
                obj.type = InOutType.output
                obj.name = output["name"]
                obj.data_type = output["type"]
                obj.description = output["description"]
                obj.save()
                ##########################
                for testCase in data["testCase"]:
                    obj = TestCase()
                    obj.assignment = assignment
                    obj.order = testCase["order"]
                    obj.is_private = testCase["isPrivate"]
                    obj.save()
                    for elmIn in testCase["input"]:
                        objTCIn = TestCaseElement()
                        objTCIn.test_case = obj
                        objTCIn.type = InOutType.input
                        objTCIn.order = elmIn["order"]
                        objTCIn.data_type = elmIn["type"]
                        objTCIn.value = elmIn["value"]
                        objTCIn.save()
                    objTCOut = TestCaseElement()
                    objTCOut.test_case = obj
                    objTCOut.type = InOutType.output
                    objTCOut.order = elmIn["order"]
                    objTCOut.data_type = elmIn["type"]
                    objTCOut.value = elmIn["value"]
                    objTCOut.save()
                ##########################
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            print(e)
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['GET'])
def getDataType(request):
    account = validate_account(request)
    if (account == None):
        return JsonResponse(INVALID_TOKEN, status=HTTP_401)
    if (account.is_active == False):
        return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
    try:
        responseData = {}
        responseData["Data"] = [
            {
                "Id": 1,
                "Name": "Integer",
                "DefaultValue": "0",
                "Description": "Integer"
            },
            {
                "Id": 2,
                "Name": "Long",
                "DefaultValue": "0",
                "Description": "Long"
            },
            {
                "Id": 3,
                "Name": "Float",
                "DefaultValue": "0",
                "Description": "Float"
            },
            {
                "Id": 4,
                "Name": "Char",
                "DefaultValue": "",
                "Description": "Char"
            },
            {
                "Id": 5,
                "Name": "String",
                "DefaultValue": "\"\"",
                "Description": "String"
            },
            {
                "Id": 6,
                "Name": "Boolean",
                "DefaultValue": "false",
                "Description": "Boolean"
            },
            {
                "Id": 7,
                "Name": "ArrayOfIntegers",
                "DefaultValue": "[1,2,3]",
                "Description": "Array Of Integers"
            },
            {
                "Id": 8,
                "Name": "ArrayOfLongs",
                "DefaultValue": "[1,2,3]",
                "Description": "Array Of Longs"
            },
            {
                "Id": 9,
                "Name": "ArrayOfFloats",
                "DefaultValue": "[1.0,2.0,3.0]",
                "Description": "Array Of Floats"
            },
            {
                "Id": 10,
                "Name": "ArrayOfChars",
                "DefaultValue": "[\"a\",\"b\",\"c\"]",
                "Description": "Array Of Chars"
            },
            {
                "Id": 11,
                "Name": "ArrayOfStrings",
                "DefaultValue": "[\"ab\",\"bc\",\"cd\"]",
                "Description": "Array Of Strings"
            },
            {
                "Id": 12,
                "Name": "ArrayOfBooleans",
                "DefaultValue": "[false,true]",
                "Description": "Array Of Booleans"
            },
            {
                "Id": 13,
                "Name": "MatrixOfIntegers",
                "DefaultValue": "[[1,2],[3,4]]",
                "Description": "Matrix Of Integers"
            },
            {
                "Id": 14,
                "Name": "MatrixOfLongs",
                "DefaultValue": "[[1,2],[3,4]]",
                "Description": "Matrix Of Longs"
            },
            {
                "Id": 15,
                "Name": "MatrixOfFloats",
                "DefaultValue": "[[1.0,2.0],[3.0,4.0]]",
                "Description": "Matrix Of Floats"
            },
            {
                "Id": 16,
                "Name": "MatrixOfChars",
                "DefaultValue": "[[\"a\",\"b\"],[\"c\",\"d\"]]",
                "Description": "Matrix Of Chars"
            },
            {
                "Id": 17,
                "Name": "MatrixOfStrings",
                "DefaultValue": "[[\"aa\",\"bb\"],[\"cc\",\"dd\"]]",
                "Description": "Matrix Of Strings"
            },
            {
                "Id": 18,
                "Name": "MatrixOfBooleans",
                "DefaultValue": "[[false,true],[true,false]]",
                "Description": "Matrix Of Booleans"
            },
            {
                "Id": 19,
                "Name": "Double",
                "DefaultValue": "0.0",
                "Description": "Double"
            },
            {
                "Id": 20,
                "Name": "ArrayOfDoubles",
                "DefaultValue": "[1.0,2.0,3.0]",
                "Description": "Array of Doubles"
            },
            {
                "Id": 21,
                "Name": "MatrixOfDoubles",
                "DefaultValue": "[[1.0,2.0],[3.0,4.0]]",
                "Description": "Matrix of Doubles"
            }
        ]
        return JsonResponse(responseData, status=HTTP_200)
    except Exception as e:
        return JsonResponse(FAILURE, status=HTTP_400)


@api_view(['POST'])
def sampleView(request):
    requestData = ListAssignmentSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            ######### Handle #########

            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
