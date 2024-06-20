from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserForgotPasswordView,
    UserVerifyCodeView,
    UserResetPasswordView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify/", UserVerifyCodeView.as_view(), name="verify"),
    path("forgot-password/", UserForgotPasswordView.as_view(), name="forget_pass"),
    path("reset-pass/<active_code>/", UserResetPasswordView.as_view()),

]