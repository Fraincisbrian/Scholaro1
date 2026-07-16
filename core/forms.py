from django import forms

from academics.models import SchoolClass

from .models import Announcement, Event


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "date", "all_school", "classes", "is_important"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "all_school": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "classes": forms.SelectMultiple(attrs={"class": "form-select", "size": 4}),
            "is_important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {"classes": "Also target specific classes", "all_school": "All School"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group by Stream so this always reflects Class Setup live.
        self.fields["classes"].choices = [
            (stream_label, [(c.id, str(c)) for c in stream_classes])
            for stream_label, stream_classes in SchoolClass.grouped_by_stream()
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "time_label", "audience"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Parent-Teacher Meeting"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time_label": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 9:00 AM - School Ground"}),
            "audience": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. All Classes"}),
        }
        labels = {"time_label": "Time / Venue"}
