from datetime import datetime, timedelta
from tokenize import group
from django.shortcuts import render

from Challenge.serializers import *
from utils.api.api import paginate_data, validate_account
from utils.api.http_status import *
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from utils.constants.models import ChallengeTypeContent
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
                    if i.challenge not in completedChallengeId:
                        completedChallengeId.append(i.challenge)
                challenges = completedChallengeId
            elif data["typeData"] == ChallengeTypeContent.Completed and ("username" in data):
                author = Account.objects.filter(
                    username=data["username"])
                if author.exists():
                    submited = Submit.objects.filter(account=author[0])
                    completedChallengeId = []
                    for i in submited:
                        if i.challenge not in completedChallengeId:
                            completedChallengeId.append(i.challenge)
                    challenges = completedChallengeId
                else:
                    return JsonResponse(NOT_FOUND_USER_FILTER, status=HTTP_400)
            else:
                return JsonResponse(FAILURE, status=HTTP_400)
            if "searchBy" in data:
                keyword = data["searchBy"]
                challenges = challenges.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword))
            if ("pageSize" in data) and ("pageNumber" in data):
                challenges = paginate_data(
                    challenges, None, data["pageSize"], data["pageNumber"])
            responseData = {}
            challengeData = []
            for i in challenges:
                item = {
                    "challengeId": i.id,
                    "image": i.image,
                    "title": i.title,
                    "decription": i.description,
                    "totalMember": "All",
                    "startAt": i.dateStart(),
                    "endAt": i.dateEnd()
                }
                challengeData.append(item)
            responseData["challenges"] = challengeData
            responseData["currentSize"] = len(challenges)
            return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            print(e)
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


# @api_view(['POST'])
# def getDetailChallenge(request):
#     requestData = ChallengeDetailSerializer(data=request.data)
#     if requestData.is_valid():
#         account = validate_account(request)
#         if (account == None):
#             return JsonResponse(INVALID_TOKEN, status=HTTP_401)
#         if (account.is_active == False):
#             return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
#         try:
#             data = request.data
#             challenge = Challenge.objects.filter(id=data["id"])
#             if challenge.exists():
#                 submited = Submit.objects.filter(challenge = challenge)

#                 responseData = {

#                 }
#             else:
#                 return JsonResponse(NOT_FOUND_CHALLENGE, status=HTTP_400)
#             return JsonResponse(SUCCESS, status=HTTP_200)
#         except Exception as e:
#             return JsonResponse(FAILURE, status=HTTP_400)
#     else:
#         return JsonResponse(INVALID_INPUT, status=HTTP_400)
