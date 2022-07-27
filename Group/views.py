import random
import string
from Account.models import Profile
from Group.serializers import *
from utils.api.api import paginate_data, validate_account
from utils.api.http_status import *
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from utils.response.challenge import *
from utils.response.common import *
from utils.response.group import *
from .models import *
from django.db.models import Q
# Create your views here.


@api_view(['POST'])
def getListGroup(request):
    requestData = GroupListSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            groupGlobal = Group.objects.get(id=1)
            groupMember = GroupMember.objects.filter(
                ~Q(group=groupGlobal), account=account)
            if groupMember.exists():
                if ("pageSize" in data) and ("pageNumber" in data):
                    groupMember = paginate_data(
                        groupMember, None, data["pageSize"], data["pageNumber"])

                listGrp = []
                for group in groupMember:
                    gr = {
                        "id": group.group.id,
                        "title": group.group.title,
                        "totalMember": group.group.total_member,
                        "joinCode": group.group.join_code,
                        "createdBy": group.group.created_by.username,
                        "image": group.group.image,
                    }
                    listGrp.append(gr)

                responseData = {
                    "groups": listGrp,
                    "currentSize": len(listGrp)
                }
                return JsonResponse(responseData, status=HTTP_200)

            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)

        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def detailGroup(request):
    requestData = GroupDetailSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            group = Group.objects.filter(id=data["id"])
            if group.exists():
                groupDetail = {
                    "id": group[0].id,
                    "title": group[0].title,
                    "joinCode": group[0].join_code,
                    "totalMember": group[0].total_member,
                    "isOwner":  group[0].created_by == account,
                }
                groupMember = GroupMember.objects.filter(group=group[0])
                if groupMember.exists():
                    if ("pageSize" in data) and ("pageNumber" in data):
                        groupMember = paginate_data(
                            groupMember, None, data["pageSize"], data["pageNumber"])
                    listGrpMb = []
                    for grpM in groupMember:
                        profile = Profile.objects.filter(account=grpM.account)
                        member = {
                            "id": grpM.account.id,
                            "username": grpM.account.username,
                            "avatar": profile[0].avatar,
                            "totalCompleted": grpM.total_completed,
                            "totalMissing": grpM.total_missing,
                            "totalScore": grpM.total_score,
                        }
                        listGrpMb.append(member)
                    responseData = {
                        "groupDetail": groupDetail,
                        "member": listGrpMb,
                        "currentSize": len(groupMember)
                    }
                    return JsonResponse(responseData, status=HTTP_200)
                else:
                    return JsonResponse(EMPTY_MEMBER, status=HTTP_400)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def createGroup(request):
    requestData = CreateGroupSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            code = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(6))
            findGroup = Group.objects.filter(join_code=code)
            while findGroup.exists():
                code = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(6))
                findGroup = Group.objects.filter(join_code=code)
            data = request.data
            grp = Group()
            grp.title = data["title"]
            grp.description = data["description"]
            grp.join_code = code
            grp.created_by = account
            grp.image = data["image"]
            grp.total_member = 1
            grp.save()
            member = GroupMember()
            member.group = grp
            member.account = account
            member.save()
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def deleteGroup(request):
    requestData = GroupDeleteSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            group = Group.objects.filter(id=data["id"])
            if group.exists():
                if (group[0].created_by == account):
                    group.delete()
                else:
                    return JsonResponse(NOT_OWNER_GROUP, status=HTTP_400)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)

            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def joinGroup(request):
    requestData = JoinGroupSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            group = Group.objects.filter(join_code=data["joinCode"])

            if group.exists():
                mb = GroupMember.objects.filter(
                    group=group[0], account=account)
                if mb.exists():
                    return JsonResponse(JOINED_GROUP, status=HTTP_400)
                grpMb = GroupMember()
                grpMb.group = group[0]
                grpMb.account = account
                grpMb.save()
                groupDetail = Group.objects.get(id=group[0].id)
                groupDetail.total_member = group[0].total_member + 1
                groupDetail.save()
                return JsonResponse(SUCCESS, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def outMember(request):
    requestData = outMemberSerializer(data=request.data)
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
                member = GroupMember.objects.filter(
                    group=group[0], account=account)
                member.delete()
                groupSelected = group[0]
                sl = group[0].total_member
                groupSelected.total_member = sl - 1
                groupSelected.save()
                return JsonResponse(SUCCESS, status=HTTP_200)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def kickMember(request):
    requestData = kickMemberSerializer(data=request.data)
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
                group = group[0]
                if group.created_by == account:
                    member = Account.objects.filter(id=data["memberId"])
                    if member.exists():
                        groupMember = GroupMember.objects.filter(
                            group=group, account=member[0])
                        groupMember.delete()
                        groupSelected = group
                        sl = group.total_member
                        groupSelected.total_member = sl - 1
                        groupSelected.save()
                        return JsonResponse(SUCCESS, status=HTTP_200)
                    else:
                        return JsonResponse(NOT_GROUP_MEMBER, status=HTTP_400)
                else:
                    return JsonResponse(NOT_OWNER_GROUP, status=HTTP_400)
            else:
                return JsonResponse(NOT_FOUND_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)


@api_view(['POST'])
def updateGroup(request):
    requestData = UpdateGroupSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
            data = request.data
            group = Group.objects.filter(id=data["groupId"])
            grp = group[0]
            if grp.created_by == account:
                if "title" in data:
                    grp.title = data["title"]
                if "description" in data:
                    grp.description = data["description"]
                grp.save()
                return JsonResponse(SUCCESS, status=HTTP_200)
            else:
                return JsonResponse(NOT_OWNER_GROUP, status=HTTP_400)
        except Exception as e:
            return JsonResponse(FAILURE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)
