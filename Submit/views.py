
import json
from sre_constants import FAILURE, SUCCESS
from tokenize import group
from django.http import JsonResponse
import requests
from Account.models import Profile
from Assignment.models import Assignment, Language, TestCase, TestCaseElement
from Challenge.models import ChallengeElement
from Group.models import GroupMember
from Submit.models import Submit
from Submit.serializers import SourceCodeSerializer
from utils.api.api import validate_account
from utils.api.http_status import HTTP_200, HTTP_400, HTTP_401
from rest_framework.decorators import api_view
from utils.constants.models import Difficulty, InOutType
from utils.response.common import *
from utils.response.submit import NOT_FOUND_CHALLENGE_ELEMENT


@api_view(['POST'])
def runAssignment(request):
    requestData = SourceCodeSerializer(data=request.data)
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
                testCases = TestCase.objects.filter(
                    assignment=assignment[0], is_private=False)
                language = Language.objects.filter(id=data["language"])[0]
                resultAll = []
                for testCase in testCases:
                    elements = TestCaseElement.objects.filter(
                        test_case=testCase)
                    if elements.exists():
                        input = ""
                        for element in elements.filter(type=InOutType.input):
                            input += str(element.value)+"\n"
                        url = "https://api2.sololearn.com/v2/codeplayground/v2/compile"
                        header = {
                            "Content-Type": "application/json",
                        }
                        payload = {
                            "code": data["sourceCode"],
                            "codeId": None,
                            "input": input,
                            "language": language.code

                        }
                        # result = requests.post(
                        #     url,  data=json.dumps(payload), headers=header)
                        # resultRun = json.loads(result.content)
                        resultRun = {
                            "data": {"output": "10\n"}, "success": True}
                        outputExpec = str(elements.filter(
                            type=InOutType.output)[0].value)
                        outputAct = str(resultRun["data"]["output"])
                        outputAct = outputAct[:len(outputAct)-1]
                        if outputExpec == outputAct:
                            matchExpec = True
                        else:
                            matchExpec = False
                        response = {
                            "testCaseId": testCase.id,
                            "isPassed": matchExpec,
                            "runSuccess": resultRun["success"],
                            "actualOutput": outputAct,
                            "expectedOutput": outputExpec,
                        }
                        resultAll.append(response)
            responseDate = {
                "result": resultAll
            }
            return JsonResponse(responseDate, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@ api_view(['POST'])
def submitAssignment(request):
    requestData = SourceCodeSerializer(data=request.data)
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
                testCases = TestCase.objects.filter(
                    assignment=assignment[0])
                language = Language.objects.filter(id=data["language"])[0]
                resultAll = []
                passed = 0
                failure = 0
                for testCase in testCases:
                    elements = TestCaseElement.objects.filter(
                        test_case=testCase)
                    if elements.exists():
                        input = ""
                        for element in elements.filter(type=InOutType.input):
                            input += str(element.value)+"\n"
                        url = "https://api2.sololearn.com/v2/codeplayground/v2/compile"
                        header = {
                            "Content-Type": "application/json",
                        }
                        payload = {
                            "code": data["sourceCode"],
                            "codeId": None,
                            "input": input,
                            "language": language.code

                        }
                        # result = requests.post(
                        #     url,  data=json.dumps(payload), headers=header)
                        # resultRun = json.loads(result.content)
                        resultRun = {
                            "data": {"output": "10\n"}, "success": True}
                        outputExpec = str(elements.filter(
                            type=InOutType.output)[0].value)
                        outputAct = str(resultRun["data"]["output"])
                        outputAct = outputAct[:len(outputAct)-1]
                        if outputExpec == outputAct:
                            matchExpec = True
                            passed += 1
                        else:
                            matchExpec = False
                            failure += 1
                        if (testCase.is_private):
                            response = {
                                "testCaseId": testCase.id,
                                "isPassed": matchExpec,
                                "runSuccess": resultRun["success"],
                                "actualOutput": None,
                                "expectedOutput": None,
                                "isPrivate": True,
                            }
                        else:
                            response = {
                                "testCaseId": testCase.id,
                                "isPassed": matchExpec,
                                "runSuccess": resultRun["success"],
                                "actualOutput": outputAct,
                                "expectedOutput": outputExpec,
                                "isPrivate": False,
                            }
                        resultAll.append(response)
            if assignment[0].difficulty == Difficulty.Easy:
                score = int(passed*50/len(testCases))
            elif assignment[0].difficulty == Difficulty.Mid:
                score = int(passed*70/len(testCases))
            elif assignment[0].difficulty == Difficulty.High:
                score = int(passed*100/len(testCases))

            challengeElement = ChallengeElement.objects.filter(
                assignment=data["assignmentId"], challenge=data["challengeId"])
            if challengeElement.exists():
                submit = Submit.objects.filter(
                    account=account, challenge_element=challengeElement[0])
                profile = Profile.objects.filter(account=account)[0]
                groupMember = GroupMember.objects.filter(
                    account=account, group=challengeElement[0].challenge.group)[0]
                if submit.exists():
                    accountSubmit = Submit.objects.get(id=submit[0].id)
                    lastScore = submit[0].highest_score
                    if submit[0].highest_score < score:
                        accountSubmit.highest_score = score
                        profile.total_score = profile.total_score - \
                            lastScore + score
                        profile.save()
                        org = profile.organization
                        org.total_score = org.total_score - \
                            lastScore + score
                        org.save()
                        groupMember.total_score = groupMember.total_score - \
                            lastScore + score
                        groupMember.save()
                    accountSubmit.source_code = data["sourceCode"]
                    accountSubmit.counter = submit[0].counter+1
                    groupMember.save()
                    accountSubmit.save()
                else:
                    lang = Language.objects.filter(id=data["language"])[0]
                    submitObj = Submit()
                    submitObj.account = account
                    submitObj.challenge_element = challengeElement[0]
                    submitObj.source_code = data["sourceCode"]
                    submitObj.highest_score = score
                    submitObj.language = lang
                    submitObj.counter = 1
                    submitObj.save()
                    profile.total_assigment = profile.total_assigment+1
                    if assignment[0].difficulty == Difficulty.Easy:
                        profile.assignment_easy = profile.assignment_easy+1
                    elif assignment[0].difficulty == Difficulty.Mid:
                        profile.assignment_medium = profile.assignment_medium+1
                    elif assignment[0].difficulty == Difficulty.High:
                        profile.assignment_hard = profile.assignment_hard+1
                    profile.total_score += score
                    org = profile.organization
                    org.total_score += score
                    groupMember.total_score += score
                    groupMember.save()
                    org.save()
                    profile.save()

                summarizeRespone = {
                    "score": score,
                    "passAll": failure == 0
                }
                responseDate = {
                    "summarize": summarizeRespone,
                    "result": resultAll
                }
                return JsonResponse(responseDate, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_CHALLENGE_ELEMENT, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
