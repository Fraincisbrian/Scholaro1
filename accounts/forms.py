from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms


class SchoolWiseAuthenticationForm(AuthenticationForm):
    """Adds Bootstrap styling + placeholder text matching the design mockup."""

    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email address", "autofocus": True}),
    )


class StyledSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autofocus": True}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
