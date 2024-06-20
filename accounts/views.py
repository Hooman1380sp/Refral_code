from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.cache import cache
from .utils import Send_Otp_Code, Send_Otp_Code_Forgot_Link
# from .permissions import IsOwnerAndAuthenticated
import random
from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserForgotPasswordSerializer,
    OtpCodeSerializer,
    UserResetPasswordSerializer,
)


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    """

    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        print(vd)
        result = cache.get(vd['email'])
        if result:
            return Response(data={"message": "email already request, user should wait to ask again"})
        random_code = random.randint(1000, 9999)
        values = {"random_code": str(random_code),
                  "password": vd["password"],
                  "referral_code": vd.get("referral_code", None)}
        cache.set(key=vd["email"], value=values, timeout=60 * 4)
        cache.close()
        Send_Otp_Code(email=vd['email'], message=f"{random_code} Active Code ")
        return Response(data={"message": "ok"}, status=status.HTTP_302_FOUND)


class UserVerifyCodeView(APIView):
    serializer_class = OtpCodeSerializer
    """
    Verify view just got otp code and register user with session
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        email = vd["email"]
        user_cache = cache.get(email)
        if user_cache is None:
            return Response(data={"message": "code Instance is None"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        code = ser_data.validated_data.get("code")
        if code == user_cache["random_code"]:
            user = User.objects.create_user(email=email,
                                            password=user_cache["password"],
                                            referral_code=user_cache["referral_code"])
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            user.save()
            return Response(data={"message": "register user is successful",
                                  "JWT_Token_Access": str(access_token), "JWT_Token_Refresh": str(refresh_token)},
                            status=status.HTTP_201_CREATED)
        return Response(data={"message": "code is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    """
    page login view
    """

    def post(self, request):

        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_email = ser_data.validated_data.get("email")
        user_password = ser_data.validated_data.get("password")
        user: User = User.objects.filter(email=user_email).first()
        if user is not None:
            if not user.is_active:
                return Response({"message": "Is Not Active Your email"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user_email == user.email:
                if user.check_password(user_password) or user.password == user_password:
                    access_token = AccessToken.for_user(user)
                    refresh_token = RefreshToken.for_user(user)
                    return Response({"message": "login is successful",
                                     "JWT_Token_Access": str(access_token),
                                     "JWT_Token_Refresh": str(refresh_token)},
                                    status=status.HTTP_202_ACCEPTED)
                return Response({"message": "password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "email is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message": "we can.t find any user with your Specifications"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)


class UserForgotPasswordView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = UserForgotPasswordSerializer
    """
    page forget password
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_email = ser_data.validated_data.get("email")
        user = User.objects.filter(email__iexact=user_email).first()
        if user is not None:
            random_str = get_random_string(86)
            cache.set(key=random_str, value=str(user_email), timeout=60 * 4)
            cache.close()
            Send_Otp_Code_Forgot_Link(to=user_email, random_str=random_str)
            return Response(data=ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "This Number is wrong "}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserResetPasswordView(APIView):
    serializer_class = UserResetPasswordSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    """
    page reset password!
    """

    def post(self, request, active_code):
        user_cache = cache.get(active_code)
        print(user_cache)
        print(type(user_cache))
        user: User = User.objects.filter(email__iexact=user_cache).first()
        print(user)
        if user is not None:
            print(user.email)
            ser_data = UserResetPasswordSerializer(instance=user, data=request.data)
            ser_data.is_valid(raise_exception=True)
            user_password = ser_data.validated_data.get("password")
            user.set_password(user_password)
            user.save()
            cache.delete(active_code)
            cache.close()
            return Response(data={"message": "password change is successful"}, status=status.HTTP_301_MOVED_PERMANENTLY)
        return Response({"message": "A User With an unregistered email"}, status=status.HTTP_404_NOT_FOUND)
