from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from urllib.parse import urlencode
from django.views import View

from .forms import RegisterForm, LoginForm

from .models import UserModel


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        login_form = LoginForm()

        error = request.GET.get('error')
        massage = request.GET.get('massage')
        created = request.GET.get('created')

        return render(
            request, "register_page.html",
            {
                "register_form": register_form,
                'login_form': login_form,
                'error': error,
                'massage': massage,
                'created': created,
            }
        )

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        login_form = LoginForm()

        # Validate Data
        if not register_form.is_valid():
            return render(
                request, "register_page.html",
                {
                    "register_form": register_form,
                    'login_form': login_form,
                    "register": True
                }
            )

        # Save
        register_form.save()

        # Return result with query params
        base_url = reverse("register")
        params = {"created": True}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if not form.is_valid():
            base_url = reverse("register")
            params = {"error": True, 'massage': 'Invalid Email Address'}
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        # Data
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            base_url = reverse("register")
            params = {"error": True, 'massage': 'Account does not exist'}
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        if not user.check_password(password):
            base_url = reverse("register")
            params = {"error": True, 'massage': 'Password Incorrect'}
            query_string = urlencode(params)

            return redirect(f"{base_url}?{query_string}")

        login(request, user)

        return redirect(reverse("qr-gen"))


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'dashboard_page.html'
        )
