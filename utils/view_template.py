
from sre_constants import FAILURE, SUCCESS
from django.http import JsonResponse
from Account.serializers import GetProfiledSerializer
from utils.api.api import validate_account
from utils.api.http_status import HTTP_200, HTTP_400, HTTP_401
from rest_framework.decorators import api_view
from utils.response.account import INACTIVE_ACCOUNT, INVALID_INPUT, INVALID_TOKEN


@api_view(['POST'])
def view(request):
    requestData = GetProfiledSerializer(data=request.data)
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
