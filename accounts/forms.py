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


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "loginEmail",
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
                "id": "loginPassword",
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        )
    )

    class Meta:
        fields = ("email", "password")


class ChangeUserInfoForm(forms.ModelForm):
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "id": "firstName",
                "class": "form-control",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "email",
                "class": "form-control",
            }
        ),
        disabled=True,
    )

    class Meta:
        model = UserModel
        fields = ("nickname", "email")


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "currentPassword",
                "class": "form-control",
            }
        )
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "newPassword",
                "class": "form-control",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "confirmPassword",
                "class": "form-control",
            }
        )
    )

    class Meta:
        fields = ("current_password", "new_password", "confirm_password")

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")

        # Basic validation
        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        return new_password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")

        # Basic validation
        if len(confirm_password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        return confirm_password


class SendEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "email",
                "name": "email",
                "class": "form-control",
                "placeholder": "your.email@example.com",
            }
        ),
        label="",
    )

    class Meta:
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("This email address is not registered!?")

        return email


class RestPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "newPassword",
                "class": "form-control",
                "placeholder": "Enter your new password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "confirmPassword",
                "class": "form-control",
                "placeholder": "Confirm your new password",
            }
        )
    )

    class Meta:
        fields = ("new_password", "confirm_password")

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")

        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data
