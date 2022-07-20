
import json
from sre_constants import FAILURE, SUCCESS
from django.http import JsonResponse
import requests
from Assignment.models import Assignment, Language, TestCase, TestCaseElement
from Submit.serializers import SourceCodeSerializer
from utils.api.api import validate_account
from utils.api.http_status import HTTP_200, HTTP_400, HTTP_401
from rest_framework.decorators import api_view
from utils.constants.models import InOutType
from utils.response.common import *


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
                        print(input)
                        result = requests.post(
                            url,  data=json.dumps(payload), headers=header)
                        resultRun = json.loads(result.content)
                        print(resultRun)
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
                            "success": matchExpec,
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
            print(e)
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
                        print(input)
                        result = requests.post(
                            url,  data=json.dumps(payload), headers=header)
                        resultRun = json.loads(result.content)
                        print(resultRun)
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
                            "success": matchExpec,
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
