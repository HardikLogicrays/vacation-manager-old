from .serializers import (
    HolidayCreateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    HolidayGetSerializer,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User, Holiday
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from .decorators import token_authentication_check


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# Create your views here.


class CreateUserView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

            response = {
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,
                "msg": "Employee Created Successfully.",
            }
            return Response(response, status=response["status"])

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors,
        }
        return Response(response, status=response["status"])


class LoginUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            check_user = authenticate(email=data["email"], password=data["password"])

            if check_user:
                token, _ = Token.objects.get_or_create(user=check_user)

                response = {
                    "token": token.key,
                    "status": status.HTTP_200_OK,
                    "msg": "Employee Login Successfully.",
                }
                return Response(response, status=response["status"])
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "errors": "Email or Password not match.",
            }
            return Response(response, status=response["status"])

        response = {"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}
        return Response(response, status=response["status"])


class LogoutUserView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    @token_authentication_check
    def post(self, request, *args, **kwargs):
        if kwargs["token_user"]:
            try:
                delete_token = Token.objects.get(user=kwargs["token_user"])
            except:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "errors": {"error": "Token not exist."},
                }
                return Response(response, response["status"])
            delete_token.delete()
            response = {"status": status.HTTP_200_OK, "msg": "Logout Successfully."}
            return Response(response, status=response["status"])


class HolidayView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    @token_authentication_check
    def get(self, request, *args, **kwargs):

        params = request.query_params

        from .validators import date_validator

        if "start_date" in params and "end_date" in params:
            date_check = date_validator(
                start_dt=params["start_date"], end_dt=params["end_date"]
            )

            if type(date_check) == dict:
                return Response(date_check, status=status.HTTP_400_BAD_REQUEST)

            user_data = Holiday.objects.filter(
                email=kwargs["token_user"],
                start_date=params["start_date"],
                end_date=params["end_date"],
            )
            serializer = HolidayGetSerializer(user_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user_data = Holiday.objects.all().filter(email=kwargs["token_user"])

        serializer = HolidayGetSerializer(user_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # CREATE HOLIDAY REQUEST

    @token_authentication_check
    def post(self, request, *args, **kwargs):

        if kwargs["token_user"]:
            request.user = kwargs["token_user"]

            serializer = HolidayCreateSerializer(
                data=request.data,
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {"status": status.HTTP_200_OK, "data": serializer.data}
                return Response(response, status=response["status"])
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "errors": serializer.errors,
                }
                return Response(response, status=response["status"])
        else:
            return Response("error")
