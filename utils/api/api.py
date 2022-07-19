from Account.models import Account
from rest_framework.authentication import get_authorization_header


def validate_account(request):
    token = get_authorization_header(request).split()
    if len(token) > 0:
        token = str(token[1]).split("'")[1]
        account = Account.objects.filter(token=token)
        if account.exists():
            return account[0]
    return None


def paginate_data(query_set, object_serializer=None, limit=10, offset=0):
    offset -= 1
    if limit < 0 or limit > 250:
        limit = 10
    if offset < 0:
        offset = 0
    results = query_set[offset*limit:offset*limit + limit]
    if object_serializer:
        results = object_serializer(results, many=True).data
    return results
