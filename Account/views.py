import datetime
import random
import string
import pyrebase
from requests import HTTPError
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
from django.http import HttpResponse
from Group.models import Group, GroupMember

from utils.constants.firebase import FirebaseConfig, downloadImage, uploadFile
from utils.constants.models import ProfileContent, RankingType
from utils.api.api import paginate_data, validate_account
from utils.response.account import *
from utils.response.common import *
from utils.api.http_status import *
from Account.forms import UploadFileForm
from .serializers import *
from .models import *

firebase = pyrebase.initialize_app(FirebaseConfig.config)
authe = firebase.auth()
database = firebase.database()


@api_view(['POST'])
def postsignUp(request):
    requestData = SignUpSerializer(data=request.data)
    if requestData.is_valid():
        data = request.data
        if Account.objects.filter(username=data["username"]).exists():
            return JsonResponse(EXIST_USERNAME, status=HTTP_400)
        try:
            user = authe.create_user_with_email_and_password(
                data["email"], data["password"])
            token = user['idToken']
            account = Account.objects.create(
                email=data["email"], token=token, username=data["username"], first_name=data["firstName"], last_name=data["lastName"])
            account.save()
            profile = Profile()
            profile.account = account
            profile.save()
            group = Group.objects.filter(id=1)
            grpMb = GroupMember()
            grpMb.group = group[0]
            grpMb.account = account
            grpMb.save()
            groupDetail = Group.objects.get(id=1)
            groupDetail.total_member = group[0].total_member + 1
            groupDetail.save()
            return JsonResponse(SUCCESS, status=HTTP_200)
        except HTTPError as e:
            if (e.strerror.find('EMAIL_EXISTS') != -1):
                responseData = EXIST_EMAIL
            elif (e.strerror.find('INVALID_EMAIL') != -1):
                responseData = INVALID_EMAIL
            elif (e.strerror.find('INVALID_PASSWORD') != -1):
                responseData = INVALID_PASSWORD
            else:
                responseData = FAILURE_SIGN_UP
            return JsonResponse(responseData, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def postsignIn(request):
    requestData = SignInSerializer(data=request.data)
    if requestData.is_valid():
        data = request.data
        account = Account.objects.filter(email=data["email"])
        if (not account.exists()):
            return JsonResponse(NOT_EXIST_EMAIL, status=HTTP_400)
        account = account[0]
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            user = authe.sign_in_with_email_and_password(
                data["email"], data["password"])
            session_id = user['idToken']
            account.token = session_id
            account.save()
            request.session['uid'] = str(session_id)

            profile = Profile.objects.filter(account=account)
            dataUser = {
                'userId': account.id,
                'username':account.username,
                'fullName': account.fullname(),
                'avatar': profile[0].avatar
            }
            responseData = {
                'messageEn': 'Login Success',
                'messageVi': '????ng nh???p th??nh c??ng',
                'token': session_id,
                'user': dataUser
            }
            return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE_SIGN_IN, status=HTTP_401)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def postReset(request):
    requestData = ResetPasswordSerializer(data=request.data)
    if requestData.is_valid():
        data = request.data
        try:
            authe.send_password_reset_email(data["email"])
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE_RESET_PASSWORD, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def getProfile(request):
    requestData = GetProfiledSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            if "username" in data and account.username != data["username"]:
                account = Account.objects.filter(username=data["username"])
                account = account[0]
            if "typeData" in data:
                if data["typeData"] == ProfileContent.Profile:
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        profile = profile[0]
                        if profile.organization == None:
                            organization = profile.organization
                        else:
                            organization = profile.organization.title
                        responseData = {
                            'user': {
                                'id': account.id,
                                'username': account.username,
                                'email': account.email,
                                'first_name': account.first_name,
                                'last_name': account.last_name,
                                'created_at': account.created_at,
                                'avatar': profile.avatar,
                                'phone': profile.phone,
                                'birthday': profile.birthday,
                                'gender': profile.gender,
                                'organization': organization,
                                'city': profile.city,
                                'country': profile.country,
                            }
                        }
                        return JsonResponse(responseData, status=HTTP_200)
                    else:
                        return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_400)
                elif data["typeData"] == ProfileContent.All:
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        profile = profile[0]
                        if profile.organization == None:
                            organization = profile.organization
                        else:
                            organization = profile.organization.title
                        responseData = {
                            'user': {
                                'id': account.id,
                                'username': account.username,
                                'email': account.email,
                                'first_name': account.first_name,
                                'last_name': account.last_name,
                                'created_at': account.created_at,
                                'avatar': profile.avatar,
                                'phone': profile.phone,
                                'birthday': profile.birthday,
                                'gender': profile.gender,
                                'organization': organization,
                                'city': profile.city,
                                'country': profile.country,
                                'total_assigment': profile.total_assigment,
                                'total_challenge': profile.total_challenge,
                                'total_group': profile.total_group,
                                'total_score': profile.total_score,
                            },
                            'assignmentCounter': {
                                'assignment_easy': profile.assignment_easy,
                                'assignment_medium': profile.assignment_medium,
                                'assignment_hard': profile.assignment_hard,
                            }
                        }
                        return JsonResponse(responseData, status=HTTP_200)
                    else:
                        return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_400)
                elif data["typeData"] == ProfileContent.Custom:
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        profile = profile[0]
                        if profile.organization == None:
                            organization = profile.organization
                        else:
                            organization = profile.organization.title
                        responseData = {
                            'user': {
                                'userId': account.id,
                                'avatar': profile.avatar,
                                'firstName': account.first_name,
                                'lastName': account.last_name,
                                'username': account.username,
                                'organizationTitle': organization,
                                'city': profile.city,
                                'country': profile.country,
                                'email': account.email,
                                'phone': profile.phone,
                                'gender': profile.gender,
                                'createdAt': account.created_at,
                            },
                            'assignmentCompleted': {
                                'numberAssignmentCompletedFollowHard': profile.assignment_easy,
                                'numberAssignmentCompletedFollowMedium': profile.assignment_medium,
                                'numberAssignmentCompletedFollowEasy': profile.assignment_hard,
                                'totalScore': profile.total_score,
                            }
                        }
                        return JsonResponse(responseData, status=HTTP_200)
                    else:
                        return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_400)
                else:
                    responseData = {
                        'user': {
                            'id': account.id,
                            'username': account.username,
                            'email': account.email,
                            'first_name': account.first_name,
                            'last_name': account.last_name,
                            'created_at': account.created_at,
                        }
                    }
                    return JsonResponse(responseData, status=HTTP_200)
            else:
                responseData = {
                    'user': {
                        'id': account.id,
                        'username': account.username,
                        'email': account.email,
                        'first_name': account.first_name,
                        'last_name': account.last_name,
                        'created_at': account.created_at,
                    }
                }
                return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE_GET_PROFILE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['PUT'])
def putAvatar(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:

            profile = Profile.objects.filter(account=account)
            if profile.exists():
                profile = profile[0]
                date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                path = uploadFile(
                    request.FILES['file'], "media/avatar/"+str(account.id)+date)
                profile.avatar = path
                profile.save()
                return JsonResponse(SUCCESS, status=HTTP_200)
            else:
                return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_200)

        except Exception as e:
            return JsonResponse(FAILURE_UPLOAD_AVATAR, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def getImage(request):
    requestData = GetImageSerializer(data=request.data)
    if requestData.is_valid():
        path = request.data["path"]
        if downloadImage(path):
            image = default_storage.open(path)
            return HttpResponse(image, content_type="image/png")
        else:
            return JsonResponse(FAILURE_GET_IMAGE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['PUT'])
def updateProfile(request):
    requestData = UpdateProfileSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data["user"]
            profile = Profile.objects.get(account=account)
            if "avatar" in data:
                profile.avatar = data["avatar"]
            if "phone" in data:
                profile.phone = data["phone"]
            if "birthday" in data:
                profile.birthday = data["birthday"]
            if "gender" in data:
                profile.gender = data["gender"]
            if "organization" in data:
                organization = Organization.objects.filter(
                    title=data["organization"])
                if organization.exists():
                    profile.organization = organization[0]
            if "city" in data:
                profile.city = data["city"]
            if "country" in data:
                profile.country = data["country"]
            if "firstName" in data:
                account.first_name = data["firstName"]
            if "lastName" in data:
                account.last_name = data["lastName"]
            profile.save()
            account.save()
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def getRanking(request):
    requestData = GetRankingSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            ######### Handle #########
            if data["typeRanking"] == RankingType.User:
                profiles = Profile.objects.all().order_by("-total_score")
                currentUserProfile = Profile.objects.get(account=account)
                currentPosition = list(profiles).index(currentUserProfile) + 1
                top3 = []

                for i in range(0, 3):
                    if profiles[i].organization == None:
                        organization = profiles[i].organization
                    else:
                        organization = profiles[i].organization.title
                    item = {"id": profiles[i].account.id,
                            "order": i+1,
                            "username": profiles[i].account.username,
                            "avatar": profiles[i].avatar,
                            "organization": organization,
                            "total_score": profiles[i].total_score,
                            }
                    top3.append(item)
                rankingList = []
                if ("pageSize" in data) and ("pageNumber" in data) and len(profiles) > 3:
                    profiles = profiles[3:]
                    profiles = paginate_data(
                        profiles, None, data["pageSize"], data["pageNumber"])
                for i in range(0, len(profiles)):

                    if profiles[i].organization == None:
                        organization = profiles[i].organization
                    else:
                        organization = profiles[i].organization.title
                    item = {"id": profiles[i].account.id,
                            "order": i+4,
                            "username": profiles[i].account.username,
                            "avatar": profiles[i].avatar,
                            "organization": organization,
                            "total_score": profiles[i].total_score,
                            }
                    rankingList.append(item)
                if currentUserProfile.organization == None:
                    organization = currentUserProfile.organization
                else:
                    organization = currentUserProfile.organization.title
                current = {"id": currentUserProfile.account.id,
                           "order": currentPosition,
                           "username": currentUserProfile.account.username,
                           "avatar": currentUserProfile.avatar,
                           "organization": organization,
                           "total_score": currentUserProfile.total_score,
                           }

                dataResponse = {
                    "top3": top3,
                    "ranking_list": rankingList,
                    "current_user": current,
                    "currentSize": len(profiles)
                }
            if data["typeRanking"] == RankingType.OrganizationRanking:
                organizations = Organization.objects.all()
                currentUserProfile = Profile.objects.get(account=account)
                organizationRaking = []
                for org in organizations:
                    total = 0
                    profiles = Profile.objects.filter(organization=org)
                    for prf in profiles:
                        total = total + prf.total_score
                    organizationRaking.append(total)
                    org.total_score = total
                    org.save()
                organizations = organizations.order_by("-total_score")
                currentPosition = list(organizations).index(
                    currentUserProfile.organization) + 1
                top3 = []
                for i in range(0, 3):
                    item = {"id": organizations[i].id,
                            "order": i+1,
                            "username": organizations[i].title,
                            "avatar": None,
                            "organization": organizations[i].title,
                            "total_score": organizations[i].total_score,
                            }
                    top3.append(item)
                rankingList = []
                if ("pageSize" in data) and ("pageNumber" in data) and len(organizations) > 3:
                    organizations = organizations[3:]
                    organizations = paginate_data(
                        organizations, None, data["pageSize"], data["pageNumber"])
                for i in range(0, len(organizations)):
                    item = {"id": organizations[i].id,
                            "order": i+4,
                            "username": organizations[i].title,
                            "avatar": None,
                            "organization": organizations[i].title,
                            "total_score": organizations[i].total_score,
                            }
                    rankingList.append(item)

                current = {"id": currentUserProfile.organization.id,
                           "order": currentPosition,
                           "username": currentUserProfile.organization.title,
                           "avatar": None,
                           "organization": currentUserProfile.organization.title,
                           "total_score": currentUserProfile.organization.total_score,
                           }

                dataResponse = {
                    "top3": top3,
                    "ranking_list": rankingList,
                    "current_user": current,
                    "currentSize": len(profiles)
                }
            return JsonResponse(dataResponse, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['GET'])
def signout(request):
    account = validate_account(request)
    if (account == None):
        return JsonResponse(INVALID_TOKEN, status=HTTP_401)
    if (account.is_active == False):
        return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
    try:
        code = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(20))
        account.token = code
        account.save()
        return JsonResponse(SUCCESS, status=HTTP_200)
    except Exception as e:
        return JsonResponse(FAILURE, status=HTTP_400)
