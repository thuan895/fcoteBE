import datetime
import profile
import pyrebase
from requests import HTTPError
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
from django.http import HttpResponse

from utils.constants.firebase import FirebaseConfig, downloadImage, uploadFile
from utils.constants.models import ProfileContent
from utils.api.api import validate_account
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
                'fullName': account.fullname(),
                'avatar': profile[0].avatar
            }
            responseData = {
                'messageEn': 'Login Success',
                'messageVi': 'Đăng nhập thành công',
                'token': session_id,
                'user': dataUser
            }
            return JsonResponse(responseData, status=HTTP_200)
        except Exception as e:
            print(e)
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
            if "type" in data:
                print(data)
                if data["type"] == ProfileContent.Profile:
                    print('thuan1')
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        profile = profile[0]
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
                                'organization': profile.organization.title,
                                'city': profile.city,
                                'country': profile.country,
                            }
                        }
                        return JsonResponse(responseData, status=HTTP_200)
                    else:
                        return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_200)
                elif data["type"] == ProfileContent.All:
                    print('thuan2')
                    profile = Profile.objects.filter(account=account)
                    if profile.exists():
                        profile = profile[0]
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
                                'organization': profile.organization.title,
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
                        return JsonResponse(NOT_EXIST_PROFILE, status=HTTP_200)
                else:
                    print('thuan3')
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
                    print(responseData)
                    return JsonResponse(responseData, status=HTTP_200)
            else:
                print('thuan3')
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
                print(responseData)
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
            if "first_name" in data:
                account.first_name = data["first_name"]
            if "last_name" in data:
                account.last_name = data["last_name"]
            if "email" in data:
                account.email = data["email"]
            profile.save()
            account.save()
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
