from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name", "roll_number", "date_of_birth", "gender",
            "school_class", "profile_photo", "address",
            "father_name", "mother_name", "primary_phone", "secondary_phone", "parent_email",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "roll_number": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "profile_photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "father_name": forms.TextInput(attrs={"class": "form-control"}),
            "mother_name": forms.TextInput(attrs={"class": "form-control"}),
            "primary_phone": forms.TextInput(attrs={"class": "form-control"}),
            "secondary_phone": forms.TextInput(attrs={"class": "form-control"}),
            "parent_email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "school_class": "Class Assignment",
            "parent_email": "Email",
        }
