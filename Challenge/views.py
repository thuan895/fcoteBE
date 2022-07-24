from calendar import c
from datetime import datetime, timedelta
from tokenize import group
from urllib import response
from django.shortcuts import render
import time
from Challenge.serializers import *
from utils.api.api import paginate_data, validate_account
from utils.api.http_status import *
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from utils.constants.models import ChallengeTypeContent, challengeStatus
from utils.response.assignment import NOT_FOUND_USER_FILTER
from utils.response.challenge import *
from utils.response.common import *
from .models import *
from Account.models import Profile
from utils.constants.firebase import FirebaseConfig
from Submit.models import Submit
import pyrebase
from django.db.models import Q
# Create your views here.


@api_view(['POST'])
def getListChallenge(request):
    requestData = ListChallengeSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            ######### Handle #########
            now = (datetime.now()-timedelta(hours=7)
                   ).strftime("%Y-%m-%d %H:%M:%S")
            challenges = Challenge.objects.filter(
                is_active=True).order_by("-id")

            if data["typeData"] == ChallengeTypeContent.Public:
                groupPublic = Group.objects.filter(id=1)
                challenges = challenges.filter(
                    quality_assurance=True, group=groupPublic[0])
            elif data["typeData"] == ChallengeTypeContent.Group and "groupID" in data:
                groupSeleted = Group.objects.filter(id=data["groupID"])
                if groupSeleted.exists():
                    challenges = challenges.filter(group=groupSeleted[0])
                else:
                    return JsonResponse(NOT_FOUND_CHALLENGE, status=HTTP_400)
            elif data["typeData"] == ChallengeTypeContent.Owner:
                challenges = challenges.filter(created_by=account)
            elif data["typeData"] == ChallengeTypeContent.Completed and ("username" not in data):
                submited = Submit.objects.filter(account=account)
                completedChallengeId = []
                for i in submited:
                    if i.challenge_element.challenge not in completedChallengeId:
                        completedChallengeId.append(
                            i.challenge_element.challenge)
                challenges = completedChallengeId
            elif data["typeData"] == ChallengeTypeContent.Completed and ("username" in data):
                author = Account.objects.filter(
                    username=data["username"])
                if author.exists():
                    submited = Submit.objects.filter(account=author[0])
                    completedChallengeId = []
                    for i in submited:
                        if i.challenge_element.challenge not in completedChallengeId:
                            completedChallengeId.append(
                                i.challenge_element.challenge)
                    challenges = completedChallengeId
                else:
                    return JsonResponse(NOT_FOUND_USER_FILTER, status=HTTP_400)
            else:
                return JsonResponse(FAILURE, status=HTTP_400)
            if "searchBy" in data:
                keyword = data["searchBy"]
                challenges = challenges.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword))
            if "status" in data:
                dataAfterStatus = []
                if data["status"] == challengeStatus.NotOpenYet:
                    for challenge in challenges:
                        if now < challenge.dateStart():
                            dataAfterStatus.append(challenge)
                elif data["status"] == challengeStatus.Open:
                    for challenge in challenges:
                        if now >= challenge.dateStart() and now <= challenge.dateEnd():
                            dataAfterStatus.append(challenge)
                elif data["status"] == challengeStatus.Close:
                    for challenge in challenges:
                        if now > challenge.dateEnd():
                            dataAfterStatus.append(challenge)
                challenges = dataAfterStatus
            if ("pageSize" in data) and ("pageNumber" in data):
                challenges = paginate_data(
                    challenges, None, data["pageSize"], data["pageNumber"])
            responseData = {}
            challengeData = []
            for i in challenges:
                if now >= i.dateStart() and now <= i.dateEnd():
                    status = challengeStatus.Open
                elif now < i.dateStart():
                    status = challengeStatus.NotOpenYet
                else:
                    status = challengeStatus.Close
                item = {
                    "challengeId": i.id,
                    "image": i.image,
                    "title": i.title,
                    "decription": i.description,
                    "totalMember": "All",
                    "startAt": i.dateStart(),
                    "endAt": i.dateEnd(),
                    "status": status
                }
                challengeData.append(item)
            responseData["challenges"] = challengeData
            responseData["currentSize"] = len(challenges)
            return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def getDetailChallenge(request):
    requestData = ChallengeDetailSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            challenge = Challenge.objects.filter(id=data["id"])
            if challenge.exists():
                listSubmit = []
                dateStart = (challenge[0].dateStart())
                dateEnd = (challenge[0].dateEnd())
                challenge_Elms = ChallengeElement.objects.filter(
                    challenge=challenge[0])
                accountSubmit = []
                now = (datetime.now()-timedelta(hours=7)
                       ).strftime("%Y-%m-%d %H:%M:%S")
                if now >= dateStart and now <= dateEnd:
                    status = challengeStatus.Open
                elif now < dateEnd:
                    status = challengeStatus.NotOpenYet
                else:
                    status = challengeStatus.Close
                responseChallenge = {
                    "challenge": {
                        "title": challenge[0].title,
                        "description": challenge[0].description,
                        "createdBy": challenge[0].created_by.username,
                        "image": challenge[0].image,
                        "group": challenge[0].group.title,
                        "groupId": challenge[0].group.id,
                        "totalAssignment": challenge[0].total_assignment,
                        "startAt": challenge[0].dateStart(),
                        "endAt": challenge[0].dateEnd(),
                        "status": status,
                    }
                }
                for elm in challenge_Elms:
                    submited = Submit.objects.filter(challenge_element=elm)
                    if submited.exists():
                        for submit in submited:
                            if submit.account not in accountSubmit:
                                accountSubmit.append(submit.account)
                for account in accountSubmit:
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        responseAccount = {
                            "user": {
                                "username": account.username,
                                "city": profile[0].city,
                                "avatar": profile[0].avatar,
                                "organization": profile[0].organization.title,
                            }
                        }
                    else:
                        responseAccount = {
                            "user": {
                                "username": account.username,
                                "city": "-",
                                "avatar": "-",
                                "organization": "-",
                            }
                        }
                    submitAsm = []
                    for chlg_Elm in challenge_Elms:
                        submit = Submit.objects.filter(
                            account=account, challenge_element=chlg_Elm)
                        if submit.exists():
                            end = datetime.strptime(
                                submit[0].dateUpdated(), "%Y-%m-%d %H:%M:%S")
                            start = datetime.strptime(
                                dateStart, "%Y-%m-%d %H:%M:%S")
                            result = int((end - start).total_seconds())
                            durationTime = time.strftime(
                                '%H:%M:%S', time.gmtime(result))
                            sbmAsm = {
                                "highestScore": submit[0].highest_score,
                                "shortestRuntime": submit[0].shortest_runtime,
                                "counter": submit[0].counter,
                                "time": durationTime,
                            }
                            submitAsm.append(sbmAsm)
                        else:
                            sbmAsm = {
                                "highestScore": "-",
                                "shortestRuntime": "-",
                                "counter": "-",
                                "time": "-",
                            }
                            submitAsm.append(sbmAsm)
                    accountSubmitR = {"user": responseAccount,
                                      "submitAssignment": submitAsm}
                    listSubmit.append(accountSubmitR)
                responseData = {}
                responseData["ChallengeDetail"] = responseChallenge
                responseData["challengeSubmit"] = listSubmit
                return JsonResponse(responseData, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_CHALLENGE, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def createChallenge(request):
    requestData = ChallengeCreateSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            group = Group.objects.filter(id=data["groupId"])
            if group.exists():
                data = request.data
                chlg = Challenge()
                chlg.title = data["title"]
                chlg.description = data["description"]
                chlg.created_by = account
                chlg.image = data["image"]
                chlg.group = group[0]
                chlg.total_assignment = len(data["element"])
                chlg.start_at = data["startAt"]
                chlg.end_at = data["endAt"]
                chlg.save()

                for asm in data["element"]:
                    asmObj = Assignment.objects.filter(id=asm["assignmentId"])
                    if asmObj.exists():
                        chlgElm = ChallengeElement()
                        chlgElm.challenge = chlg
                        chlgElm.assignment = asmObj[0]
                        chlgElm.save()
                    else:
                        return JsonResponse(NOT_FOUND_ASSIGNMENT, status=HTTP_400)
                return JsonResponse(SUCCESS, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def deleteChallenge(request):
    requestData = ChallengeDeleteSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            challenge = Challenge.objects.filter(id=data["challengeId"])
            if challenge.exists():
                challenge = challenge[0]
                if challenge.created_by == account:
                    challenge.delete()
                    return JsonResponse(SUCCESS, status=HTTP_200)
                else:
                    return JsonResponse(NOT_OWNER_CHALLENGE, status=HTTP_400)
            else:
                return JsonResponse(NOT_FOUND_CHALLENGE, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
