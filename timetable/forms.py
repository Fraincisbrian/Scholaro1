from django import forms

from .models import TimetableEntry


class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ["subject", "teacher"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, school_class=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school_class is not None:
            self.fields["subject"].queryset = school_class.subjects.all()
        self.fields["teacher"].required = False
