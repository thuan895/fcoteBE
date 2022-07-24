
import json
from django.http import JsonResponse
from Assignment.serializers import *
from Challenge.models import Challenge, ChallengeElement
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
            if "filterByCurrentAccount" in data:
                if data["filterByCurrentAccount"]:
                    assignments = assignments.filter(created_by=account)
                else:
                    assignments = assignments.filter(quality_assurance=True)
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
                    assignments, None, data["pageSize"], data["pageNumber"])
            responseData = {}
            listData = []
            for assignment in assignments:
                assignmentData = {
                    "id": assignment.id,
                    "title": assignment.title,
                    "image": assignment.image,
                    "difficulty": assignment.difficulty,
                    "score": assignment.score,
                    # "assignment_tag": assignment.assignment_tag.id,
                    "totalParticipant": assignment.total_participant,
                    "createdBy": assignment.created_by.username,
                    "createdAt": assignment.date()
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
                    # "sample": assignment[0].sample,
                    # "image": assignment[0].image,
                    "difficulty": assignment[0].difficulty,
                    "totalTestCase": assignment[0].total_test_case,
                    "score": assignment[0].score,
                    # "assignment_tag": assignment[0].assignment_tag.id,
                    "characterLimit": assignment[0].character_limit,
                    "totalParticipant": assignment[0].total_participant,
                    "createdBy": assignment[0].created_by.username,
                }
                responseData["detail"] = assignmentData
                assignmentLanguages = AssignmentLanguage.objects.filter(
                    assignment=assignment[0])
                assignmentLanguagesResponse = []
                for asmlg in assignmentLanguages:
                    asmlgResponse = {"id": asmlg.language.id,
                                     "language": asmlg.language.title,
                                     "timeLimit": asmlg.time_limit}
                    assignmentLanguagesResponse.append(asmlgResponse)
                responseData["languages"] = assignmentLanguagesResponse
                parammeters = Parammeter.objects.filter(
                    assignment=assignment[0]).order_by("id")
                parammetersResponse = []
                input = []
                output = {}
                for prm in parammeters:
                    if prm.type == InOutType.input:
                        prmResponse = {"id": prm.id,
                                       "assignment": prm.assignment.id,
                                       "order": prm.order,
                                       "type": prm.type,
                                       "name": prm.name,
                                       "dataType": prm.data_type,
                                       "description": prm.description}
                        input.append(prmResponse)
                    else:
                        output = {"id": prm.id,
                                  "assignment": prm.assignment.id,
                                  "order": prm.order,
                                  "type": prm.type,
                                  "name": prm.name,
                                  "dataType": prm.data_type,
                                  "description": prm.description}
                parammetersResponse = {
                    "input": input,
                    "output": output,
                }
                responseData["parameters"] = parammetersResponse
                testCases = TestCase.objects.filter(assignment=assignment[0])
                testCasesResponse = []
                for testCase in testCases:
                    if testCase.is_private and testCase.assignment.created_by != account:
                        testCase = {"id": testCase.id,
                                    "assignment": testCase.assignment.id,
                                    "order": testCase.order,
                                    "input": [],
                                    "output": {},
                                    "isPrivate": testCase.is_private}
                        testCasesResponse.append(testCase)
                    else:
                        testCaseElements = TestCaseElement.objects.filter(
                            test_case=testCase)
                        testCaseElmList = {}
                        input = []
                        output = {}
                        for elm in testCaseElements:
                            variableName = parammeters[list(
                                testCaseElements).index(elm)].name
                            if elm.type == InOutType.input:
                                elmData = {"id": elm.id,
                                           "testCase": elm.test_case.id,
                                           "order": elm.order,
                                           "type": elm.type,
                                           "dataType": elm.data_type,
                                           "name": variableName,
                                           "value": elm.value}
                                input.append(elmData)
                            else:
                                output = {"id": elm.id,
                                          "testCase": elm.test_case.id,
                                          "order": elm.order,
                                          "type": elm.type,
                                          "dataType": elm.data_type,
                                          "name": variableName,
                                          "value": elm.value}
                        testCase = {"id": testCase.id,
                                    "assignment": testCase.assignment.id,
                                    "order": testCase.order,
                                    "input": input,
                                    "output": output,
                                    "isPrivate": testCase.is_private}
                        testCasesResponse.append(testCase)
                responseData["testCases"] = testCasesResponse
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
                challengeGlobal = Challenge.objects.filter(id=1)
                challengeElm = ChallengeElement()
                challengeElm.challenge = challengeGlobal[0]
                challengeElm.assignment = assignment
                challengeElm.save()
                ##########################
                for lgg in data["language"]:
                    language = Language.objects.filter(title=lgg["language"])
                    if language.exists():
                        obj = AssignmentLanguage()
                        obj.assignment = assignment
                        obj.language = language[0]
                        obj.time_limit = lgg["timeLimit"]
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
        data = DataType
        responseData = {}
        list = []
        for i in data:
            type = {'name': str(i.name).replace("Of", " Of "), "value": i}
            list.append(type)
        responseData["dataType"] = list
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


@api_view(['POST'])
def deleteAssignment(request):
    requestData = AssignmentDeleteSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            assignment = Assignment.objects.filter(id=data["assignmentId"])
            if assignment.exists():
                assignment = assignment[0]
                if assignment.created_by == account:
                    assignment.delete()
                    return JsonResponse(SUCCESS, status=HTTP_200)
                else:
                    return JsonResponse(NOT_OWNER_ASSIGNMENT, status=HTTP_400)
            else:
                return JsonResponse(NOT_FOUND_ASSIGNMENT, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
