from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    DashboardView,
    ChangeInfoView,
    ChangePasswordView,
    logout_view,
    SendEmailView,
    RestPasswordView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("send-email/", SendEmailView.as_view(), name="send-email"),
    path(
        "reset-password/<str:token>", RestPasswordView.as_view(), name="reset-password"
    ),
    path("logout/", logout_view, name="logout"),
    # Only Post View
    path("change-info/", ChangeInfoView.as_view(), name="change-info"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
