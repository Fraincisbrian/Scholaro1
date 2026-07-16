from django.conf import settings
from django.db import models


class Announcement(models.Model):
    """
    Powers 'Recent Announcements' on the dashboard and the full
    Announcements CRUD page. Target audience is modeled as real
    SchoolClass tags (+ an All School flag) so it matches the
    multi-select "Target Audience" picker in the mockup.
    """

    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField()
    is_important = models.BooleanField(default=False)
    all_school = models.BooleanField(default=True, verbose_name="All School")
    classes = models.ManyToManyField(
        "academics.SchoolClass", blank=True, related_name="announcements",
        help_text="Specific classes this announcement also targets.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return self.title

    def audience_labels(self):
        labels = []
        if self.all_school:
            labels.append("All School")
        labels += [str(c) for c in self.classes.all()]
        return labels


class Event(models.Model):
    """Powers 'Upcoming Events' on the dashboard."""

    title = models.CharField(max_length=200)
    date = models.DateField()
    time_label = models.CharField(max_length=100, blank=True, help_text="e.g. '9:00 AM - School Ground'")
    audience = models.CharField(max_length=200, default="All Classes")

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.title
