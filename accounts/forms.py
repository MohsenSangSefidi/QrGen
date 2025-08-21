from django.core.exceptions import ValidationError
from django import forms

from .models import UserModel


class RegisterForm(forms.ModelForm):
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "id": "signupName",
                "class": "form-control",
                "placeholder": "Enter your full name",
            }
        ),
        label="",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "signupEmail",
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        ),
        label="",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "signupPassword",
                "class": "form-control",
                "placeholder": "Create a password",
            }
        ),
        label="",
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "signupConfirmPassword",
                "class": "form-control",
                "placeholder": "Confirm your password",
            }
        ),
        label="",
    )

    class Meta:
        model = UserModel
        fields = ("nickname", "email", "password", "re_password")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Check if email already exists
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Basic validation
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password and re_password and password != re_password:
            self.add_error("re_password", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user
