
from sre_constants import SUCCESS
from django.http import JsonResponse
from Account.serializers import GetProfiledSerializer
from utils.api.api import validate_account
from utils.api.http_status import HTTP_200, HTTP_400, HTTP_401
from utils.response.account import FAILURE_GET_PROFILE, INACTIVE_ACCOUNT, INVALID_INPUT, INVALID_TOKEN


def view(request):
    requestData = GetProfiledSerializer(data=request.data)
    if requestData.is_valid():
        account = validate_account(request)
        if (account == None):
            return JsonResponse(INVALID_TOKEN, status=HTTP_401)
        if (account.is_active == False):
            return JsonResponse(INACTIVE_ACCOUNT, status=HTTP_400)
        try:
        
            ######### Handle #########
            
            return JsonResponse(SUCCESS, status=HTTP_200)
        except Exception as e:
            return JsonResponse(FAILURE_GET_PROFILE, status=HTTP_400)
    else:
        return JsonResponse(INVALID_INPUT, status=HTTP_400)