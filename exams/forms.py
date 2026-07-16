from django import forms

from academics.models import SchoolClass

from .models import Exam


class ExamForm(forms.ModelForm):
    classes = forms.ModelMultipleChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=True,
    )

    class Meta:
        model = Exam
        fields = ["name", "term", "academic_year", "date", "classes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mid-Term Exam"}),
            "term": forms.Select(attrs={"class": "form-select"}),
            "academic_year": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2025/2026"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
