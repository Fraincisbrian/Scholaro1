from django.conf import settings
from django.db import models


class SchoolClass(models.Model):
    """
    A single class, grouped under a Stream (Technical or Grammar). This is
    the shared building block that Students, Attendance, Fees, Timetable,
    and Announcements all reference.

    Class Level depends on the Stream:
      Technical -> TVEE Intermediate Level, TVEE Advanced Level
      Grammar   -> GCE Ordinary Level, GCE Advanced Level

    Section is the specific class within that level (e.g. "Form 1", "F1MM", "A").
    """

    class Stream(models.TextChoices):
        TECHNICAL = "technical", "Technical"
        GRAMMAR = "grammar", "Grammar"

    TECHNICAL_LEVELS = [
        ("tvee_intermediate", "TVEE Intermediate Level"),
        ("tvee_advanced", "TVEE Advanced Level"),
    ]
    GRAMMAR_LEVELS = [
        ("gce_ordinary", "GCE Ordinary Level"),
        ("gce_advanced", "GCE Advanced Level"),
    ]
    LEVEL_CHOICES = TECHNICAL_LEVELS + GRAMMAR_LEVELS
    LEVELS_BY_STREAM = {
        Stream.TECHNICAL: TECHNICAL_LEVELS,
        Stream.GRAMMAR: GRAMMAR_LEVELS,
    }

    stream = models.CharField(max_length=20, choices=Stream.choices)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES)
    section = models.CharField(
        max_length=30, blank=True,
        help_text="The specific class, e.g. Form 1, F1MM, A.",
    )
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_taught",
    )

    class Meta:
        ordering = ["stream", "level", "section"]
        unique_together = ("stream", "level", "section")
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        label = self.get_level_display()
        return f"{label} - {self.section}" if self.section else label

    @property
    def student_count(self):
        return self.students.count()

    @classmethod
    def grouped_by_stream(cls, queryset=None):
        """
        Returns [(stream_label, classes_in_that_stream_queryset), ...] for
        any Stream that currently has classes. Used everywhere a class
        picker needs to group choices the same way Class Setup does,
        instead of one flat unsorted list — so newly added classes always
        show up correctly organized, without each app reimplementing this.
        """
        qs = queryset if queryset is not None else cls.objects.all()
        groups = []
        for value, label in cls.Stream.choices:
            stream_classes = qs.filter(stream=value)
            if stream_classes.exists():
                groups.append((label, stream_classes))
        return groups


class Subject(models.Model):
    """A subject taught in a given class, assigned to a teacher."""

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="subjects_taught",
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("school_class", "name")

    def __str__(self):
        return f"{self.name} ({self.school_class})"


