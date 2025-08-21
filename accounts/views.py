from django.shortcuts import render, redirect, reverse
from urllib.parse import urlencode
from django.views import View

from .forms import RegisterForm


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()

        return render(request, "register_page.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        # Validate Data
        if not form.is_valid():
            return render(
                request, "register_page.html", {"form": form, "register": True}
            )

        # Save
        form.save()

        # Return result with query params
        base_url = reverse("register")
        params = {"created": True}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")
