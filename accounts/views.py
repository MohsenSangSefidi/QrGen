from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_utils import send_email
from urllib.parse import urlencode
from django.utils import timezone
from django.conf import settings
from django.views import View

from .forms import (
    RegisterForm,
    LoginForm,
    ChangeUserInfoForm,
    ChangePasswordForm,
    SendEmailForm,
    RestPasswordForm,
)

from .models import UserModel


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        login_form = LoginForm()

        # Get Saving Status From Query Params
        # ( This page have two forms I separate them in to post function and get there status from query params )
        error = request.GET.get("error")
        message = request.GET.get("message")
        created = request.GET.get("created")

        return render(
            request,
            "register_page.html",
            {
                "register_form": register_form,
                "login_form": login_form,
                "error": error,
                "message": message,
                "created": created,
            },
        )

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        login_form = LoginForm()

        # Validate Form Data
        if not register_form.is_valid():
            return render(
                request,
                "register_page.html",
                {
                    "register_form": register_form,
                    "login_form": login_form,
                    "register": True,
                },
            )

        # Save
        register_form.save()

        # Return Result With Query Params ( For changing template tab to the login tab )
        base_url = reverse("register")
        params = {"created": True}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


class LoginView(View):
    def post(self, request, *args, **kwargs):
        """
        This is the post-view for checking the user information and login user after that it redirect to register
        login form and register for are in the same template because of that I separate the post-function
        """

        form = LoginForm(request.POST)

        # Validate Form Data
        if not form.is_valid():
            base_url = reverse("register")
            params = {"error": True, "message": "Invalid Email Address"}
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Get Data From Form
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        # Check User Exist
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Redirect To Register View
            base_url = reverse("register")
            params = {
                "error": True,
                "message": "Account does not exist",
            }  # Send Saving Status
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Check User Password
        if not user.check_password(password):
            # Redirect To Register View
            base_url = reverse("register")
            params = {
                "error": True,
                "message": "Password Incorrect",
            }  # Send Saving Status
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Login User
        login(request, user)

        return redirect(reverse("qr-gen"))


@method_decorator(login_required, name="dispatch")
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        change_info_form = ChangeUserInfoForm(instance=request.user)
        password_form = ChangePasswordForm()

        # User Data
        api_key = request.user.api_key

        # Query Params
        # ( This page have two forms I separate them in to post function and get there status from query params )
        password_success = request.GET.get("password_success")
        info_success = request.GET.get("info_success")
        message = request.GET.get("message")
        info_error = request.GET.get("info_error")
        password_error = request.GET.get("password_error")
        error = request.GET.get("error")

        # User Qrcodes
        qrcodes = request.user.qr_codes.all()

        return render(
            request,
            "dashboard_page.html",
            {
                "change_info_form": change_info_form,
                "password_form": password_form,
                "password_success": password_success,
                "info_success": info_success,
                "message": message,
                "info_error": info_error,
                "password_error": password_error,
                "error": error,
                "api_key": api_key,
                "qrcodes": qrcodes,
                "domain": settings.DEFAULT_DOMAIN,
            },
        )


@method_decorator(login_required, name="dispatch")
class ChangeInfoView(View):
    def post(self, request, *args, **kwargs):
        """
        This post-view for saving the user new information. Request came from dashboard-view template
        """
        user = request.user

        form = ChangeUserInfoForm(request.POST, instance=user)

        if not form.is_valid():
            # Return result with query params
            base_url = reverse("dashboard")
            params = {"info_error": True}
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Save User New Information
        form.save()

        # Return To Dashboard
        base_url = reverse("dashboard")
        params = {"info_success": True, "message": "Info Changed Successfully!"}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(View):
    def post(self, request, *args, **kwargs):
        """
        This post-view for saving the user new password changing from dashboard-view. Request came from dashboard-view template
        """
        form = ChangePasswordForm(request.POST)

        # Validate Form Data
        if not form.is_valid():
            base_url = reverse("dashboard")
            params = {
                "password_error": True,
                "error": "Password must be at least 8 characters long.",
            }
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        user = request.user  # Get User From Request
        # Get Data From Form
        current_password = form.cleaned_data.get("current_password")
        new_password = form.cleaned_data.get("new_password")
        confirm_password = form.cleaned_data.get("confirm_password")

        # Check New_Password & Confirm_Password
        if new_password != confirm_password:
            # Return To Dashboard And Rais Error
            base_url = reverse("dashboard")
            params = {
                "password_error": True,
                "error": "New Password and Confirm Password do not match.",
            }
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Check User Current Password
        if not user.check_password(current_password):
            # Return To Dashboard And Rais Error
            base_url = reverse("dashboard")
            params = {
                "password_error": True,
                "error": "Current Password does not match.",
            }
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Save User New Password
        user.set_password(new_password)
        user.save()

        # Login Again With New Data
        login(request, user)

        # Return To Dashboard
        base_url = reverse("dashboard")
        params = {"password_success": True, "message": "Password Changed Successfully!"}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


class SendEmailView(View):
    """
    SendEmailView is for sending reset-password email to user
    """

    def get(self, request, *args, **kwargs):
        form = SendEmailForm()

        return render(
            request,
            "send_email_page.html",
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = SendEmailForm(request.POST)

        # Validate Form Data
        if not form.is_valid():
            return render(
                request,
                "send_email_page.html",
                {
                    "form": form,
                },
            )

        # Get Data From Form
        email = form.cleaned_data.get("email")

        # Check Account With This Email Exist
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Rais Error
            form.add_error("email", "Email Does Not Exist!")
            return render(
                request,
                "send_email_page.html",
                {
                    "form": form,
                },
            )

        # Set A New Token For User
        user.token = get_random_string(length=100)
        user.token_active_date = timezone.datetime.now() + timezone.timedelta(days=1)
        user.save()

        # Send mail
        link = settings.DEFAULT_DOMAIN + reverse(
            "reset-password", args=[user.token]
        )  # Rest Page Link
        # send_email({"user": user, "link": link}, user.email)

        return render(
            request,
            "send_email_page.html",
            {"form": form, "success": True},
        )


class RestPasswordView(View):
    """
    This view for rendering the rest-password page. Link of this page sending to user with email
    """

    def get(self, request, token, *args, **kwargs):
        form = RestPasswordForm()

        # Get User Object via Token
        try:
            user = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            return redirect(reverse("register"))

        # Check Token Expire Date
        if user.token_active_date < timezone.now():
            return redirect("register")

        return render(
            request,
            "reset_password_page.html",
            {
                "form": form,
            },
        )

    def post(self, request, token, *args, **kwargs):
        form = RestPasswordForm(request.POST)

        # Validate Form Data
        if not form.is_valid():
            return render(
                request,
                "reset_password_page.html",
                {
                    "form": form,
                },
            )

        # Get User Object via Token
        try:
            user = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            return redirect(reverse("register"))

        # Set New Password
        user.set_password(form.cleaned_data.get("new_password"))
        user.save()

        # Login With New Information
        login(request, user)

        # Redirect User To Dashboard
        return redirect(reverse("dashboard"))


# Logout View
@login_required()
def logout_view(request):
    logout(request)

    return redirect(reverse("qr-gen"))
