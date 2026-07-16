from django.conf import settings
from django.db import models

from academics.models import SchoolClass, Subject


class TimetableEntry(models.Model):
    """
    One cell in a class's weekly timetable grid: a Day + Period slot
    assigned to a Subject (and its Teacher, defaulting to the subject's
    assigned teacher but overridable per slot).
    """

    class Day(models.TextChoices):
        MONDAY = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"

    PERIOD_CHOICES = [
        (1, "1st Period (7:30 - 8:15)"),
        (2, "2nd Period (8:15 - 9:00)"),
        (3, "3rd Period (9:00 - 9:45)"),
        (4, "4th Period (10:00 - 10:45)"),
        (5, "5th Period (10:45 - 11:30)"),
        (6, "6th Period (11:30 - 12:15)"),
        (7, "7th Period (13:00 - 13:45)"),
        (8, "8th Period (13:45 - 14:30)"),
    ]

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="timetable_entries")
    day = models.CharField(max_length=3, choices=Day.choices)
    period = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetable_entries")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="timetable_entries",
    )

    class Meta:
        ordering = ["day", "period"]
        unique_together = ("school_class", "day", "period")
        verbose_name_plural = "Timetable entries"

    def __str__(self):
        return f"{self.school_class} - {self.get_day_display()} P{self.period} - {self.subject}"

    @staticmethod
    def period_label(period):
        return dict(TimetableEntry.PERIOD_CHOICES).get(int(period), f"Period {period}")
