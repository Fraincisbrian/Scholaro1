from django import forms
from django.contrib.auth import get_user_model

from .models import SchoolClass, Subject

User = get_user_model()


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["stream", "level", "section", "class_teacher"]
        widgets = {
            "stream": forms.Select(attrs={"class": "form-select", "data-role": "stream-select"}),
            "level": forms.Select(attrs={"class": "form-select", "data-role": "level-select"}),
            "section": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Form 1, F1MM, A"}),
            "class_teacher": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"stream": "Section", "level": "Class Level", "section": "Section / Class Name"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["class_teacher"].queryset = User.objects.exclude(role=User.Role.ADMIN)
        self.fields["class_teacher"].required = False
        self.fields["stream"].choices = [("", "-- Select Section --")] + [
            c for c in self.fields["stream"].choices if c[0]
        ]
        self.fields["level"].choices = [("", "-- Select Level --")] + [
            c for c in self.fields["level"].choices if c[0]
        ]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "teacher"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mathematics"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].queryset = User.objects.exclude(role=User.Role.ADMIN)
        self.fields["teacher"].required = False
