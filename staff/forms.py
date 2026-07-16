from django import forms
from django.contrib.auth import get_user_model

from .models import StaffProfile

User = get_user_model()

STAFF_ROLE_CHOICES = [
    (User.Role.TEACHER, "Teacher"),
    (User.Role.STAFF, "Staff"),
]


class StaffInviteForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(choices=STAFF_ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    designation = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mathematics Teacher"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A staff member with this email already exists.")
        return email


class StaffEditForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(choices=STAFF_ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    designation = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


class AcceptInviteForm(forms.Form):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return cleaned
