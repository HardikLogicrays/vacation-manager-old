
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response


def token_authentication_check(func):

    def check_token_request(self, request):

        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.split(" ")[1]
        except:
            response = {
                "errors": {
                    "token": "Token required.",
                    "status": status.HTTP_401_UNAUTHORIZED
                }
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        try:
            check_user = Token.objects.get(key=token)
        except:
            response = {
                "errors": {
                    "token": "Token not matched.",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return func(self, request, token_user=check_user.user)

    return check_token_request
